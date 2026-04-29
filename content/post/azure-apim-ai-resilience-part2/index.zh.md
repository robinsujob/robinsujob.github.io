---
slug: "azure-apim-ai-resilience-part2"
title: "使用 API Management 网关构建 Azure AI 韧性架构（二）— Retry 行为的可观测性与告警"
date: 2026-04-29
weight: 1
description: "通过 Application Insights Diagnostic Logs 实现完整的 Retry 可观测性——记录每次重试失败、通过 KQL 还原重试链路、配置自动化告警，全程无需修改任何 Policy 代码。"
image: images/cover.png
categories:
  - Azure
tags:
  - Azure
  - API Management
  - AI
  - Application Insights
  - 可观测性
  - KQL
  - 告警
  - 企业架构
---

在上一篇文章《使用 API Management 网关构建 Azure AI 韧性架构》中，我们通过 Azure API Management 构建了一套面向多个 Microsoft Foundry 资源的韧性网关架构——Backend Load Balancing Pool 实现负载均衡，`retry` 策略在后端返回 4xx/5xx 错误时自动切换到健康实例。这套机制让客户端几乎感知不到后端故障的存在。

但"感知不到"恰恰是运维人员面临的挑战：**Retry 机制在保护客户端的同时，也隐藏了中间失败的细节。** 当请求经过 3 次 Retry 最终成功返回 200 时，运维人员无从知晓前两次失败的原因——是 429 限流？是 404 部署未找到？还是 500 服务端错误？哪个后端出了问题？错误 Body 里说了什么？

本文将在上篇架构的基础上，通过 **Application Insights Diagnostic Logs** 实现 Retry 过程的完整可观测性，**无需修改任何 Policy 代码**，帮助开发和运维人员：

- 📋 **记录每次 Retry 失败的详细信息** — 包括失败的后端地址、HTTP 状态码、错误响应 Body 以及 APIM 请求 ID
- 🔍 **通过 KQL 查询还原完整的 Retry 链路** — 用 operation_Id 关联同一请求的所有重试记录
- 🔔 **配置自动告警** — 当 Retry 失败次数超过阈值时，通过邮件及时通知运维团队

### 1. 架构概览

本文在上篇 APIM + Foundry 韧性架构之上，增加了 Application Insights 可观测性层。无需修改现有的 APIM Policy 和 Backend 配置，仅通过 Diagnostic Logs 配置即可实现 Retry 过程的完整监控与告警。

**本文新增组件：**

| 组件 | 角色 |
|------|------|
| **Application Insights** | 接收 APIM 原生 telemetry（`requests` / `dependencies` / `exceptions`），记录每次 Retry 的后端调用详情 |
| **Log Alert** | 基于 KQL 查询自动触发告警通知，当失败次数超过阈值时通知运维 |
| **Action Group** | 定义告警动作（邮件/SMS/Webhook） |

核心设计理念：

- **零代码改动** — 无需修改任何 Policy，完全通过 APIM Diagnostic Logs 配置实现
- **原生 Telemetry** — APIM 的 `dependencies` 表自动记录每次 `forward-request` 调用（包括 Retry 中间失败），配合 Backend Response 的 Headers to log 和 Body bytes 配置，可捕获错误详情和 Foundry 请求 ID
- **Retry 全链路可见** — 同一请求的所有 Retry 尝试共享相同的 `operation_Id`，可在 KQL 中轻松还原完整重试链路
- **主动告警** — 通过 Log Alert 规则自动检测失败趋势，及时通知运维团队

接下来，我们将按以下步骤完成整个 Retry 可观测性方案的搭建：

| 章节 | 操作 | 目标 |
|------|------|------|
| 2 | 创建 Application Insights | 搭建日志存储和查询基础设施 |
| 3 | 绑定 APIM Logger | 将 APIM 与 App Insights 关联 |
| 4 | 配置 API Diagnostic Logs | 启用目标 API 的 App Insights 日志，配置 Verbosity、Backend Response Headers 和 Body |
| 5 | 验证数据 | 在 App Insights 中确认 dependencies 表的 Retry 记录 |
| 6 | 配置告警规则 | 创建 Log Alert + Action Group，自动邮件通知 |

### 2. 创建 Application Insights 实例

在 APIM 同订阅、同区域中创建一个 workspace-based 的 Application Insights 实例，用于接收 APIM 的 telemetry 数据。

##### 2-1) 在 Azure Portal 顶部搜索栏中输入 Application Insights，选择 **Application Insights** 服务

![](images/2-1-search-application-insights.png)

##### 2-2) 点击 **+ Create**，填写以下关键配置并完成创建

![](images/2-2-create-app-insights.png)

| 配置项 | 建议值 | 说明 |
|--------|-------|------|
| Subscription | 与 APIM 相同 | 保持在同一订阅下便于管理 |
| Resource group | `apim-ai-hub` | 与 APIM 同一资源组 |
| Name | `ai-hub-app-insight` | 指定一个Application Insights的实例名称 |
| Region | `Japan East` | 与 APIM 同一区域，减少数据传输延迟 |
| Workspace | 默认 | 系统自动创建 Log Analytics workspace，或者选用一个您自己创建的日志空间 |

> **📝 说明：**
>
> Application Insights 是 workspace-based 的，底层数据存储在 Log Analytics workspace 中。创建时会自动关联一个 workspace，无需手动创建。

### 3. 绑定 APIM Logger

将上一步创建的 Application Insights 实例与 APIM 关联，使 APIM 能够将 telemetry 数据发送到 App Insights。

##### 3-1) 进入 APIM 实例 → 左侧 **Monitoring** → **Application Insights** → 点击 **+ Add**

![](images/3-1-bind-apim-logger.png)

| 配置项 | 建议值 | 说明 |
|--------|-------|------|
| Application Insights instance | `ai-hub-app-insight` | 选择刚创建的Application Insights实例 |
| ☐ Use as default and enable basic logging for all APIs | **不勾选** | 勾选后此 Logger 将作为全局默认，对所有 API 启用基础日志。高流量时（>1000 req/s）会降低 40-50% 吞吐量。建议在 Step 4 中按 API 单独启用 |
| ☐ Add availability monitor | **不勾选** | 勾选后 App Insights 会定期验证 APIM 网关端点是否响应，结果显示在 App Insights 的 Availability 面板中。本文场景不需要 |

### 4. 配置 API Diagnostic Logs

对目标 AI API 启用 Application Insights 日志，配置采样率、错误记录、Backend Response 等参数。

##### 4-1) 进入 APIM → APIs → 选择目标 API → 切换到 **Settings** 标签 → 向下滚动到 **Diagnostic Logs** 区域，点击Enable

![](images/4-1-api-settings-diagnostic-logs.png)

##### 4-2) 选择 **Application Insights** 标签页，勾选 **Enable**，按以下参数配置

![](images/4-2-diagnostic-logs-config.png)

| 配置项 | 建议值 | 说明 |
|--------|-------|------|
| **Destination** | `ai-hub-app-insight` | 选择已绑定的 App Insights 实例。⚠️ 如果显示 "No App Insights were configured"，需先回到 Step 3 绑定 Logger |
| **Sampling (%)** | `100` | 采样比例，100 为全量记录（生产环境可调为 25-50） |
| **Always log errors** | ✅ Enable | 确保错误请求不被采样过滤，即使 Sampling < 100% 也会记录所有 4xx/5xx |
| **Log client IP address** | ✅ Enable | 记录调用方 IP，排障时有用 |
| **Support custom metrics** | 不勾选 | 仅在使用 `emit-metric` 策略时需要，本文不使用 |
| **Verbosity** | ⚠️ `Information` | 控制原生 telemetry 的记录级别，**建议选 Information 或 Verbose**（见下方说明） |
| **Correlation protocol** | `W3C` | 新标准，支持跨服务分布式追踪，用 `traceparent` 头关联前后端请求 |

**Verbosity 设置说明：**

> **❗ 重要：**
>
> **Verbosity 建议设为 `Information` 或 `Verbose`，不选 `Error`。**
>
> **Verbosity 控制了整个请求链路的日志级别**——最终成功请求（200）被视为 information 级别，失败请求（4xx/5xx）被视为 error 级别。

| Verbosity | 最终请求成功（200） | 最终请求失败（4xx/5xx） |
|-----------|-------------------|----------------------|
| **Information** ✅ | ✅ `requests` 记录 + ✅ 所有 `dependencies` 记录（含 Retry 中间失败） | ✅ `requests` 记录 + ✅ 所有 `dependencies` 记录 |
| **Error** ❌ | ❌ **不记录任何内容**（request 和 dependencies 全部丢失） | ✅ `requests` 记录 + ✅ 关联的 `dependencies` 记录 |

> **⚠️ 注意：**
>
> **Verbosity=Error的情况下：** 如果 3 次 Retry 中有 2 次失败（404）但最终第 3 次成功（200），整个请求链路**不会出现在任何表中**——包括那 2 次中间失败的 dependency 记录也会丢失。这对 Retry 可观测性会成为盲区。
>
> 选择 `Information` 可确保无论最终结果成功还是失败，所有 Retry 过程都被完整记录。

**Additional settings — Backend Response 配置：**

这是实现 Retry 可观测性的关键配置。勾选 **Backend Response**，配置 Headers to log 和 Body bytes，APIM 会在 `dependencies` 表的 `Properties` 字段中附带这些信息。

| 配置项 | 建议值 | 说明 |
|--------|-------|------|
| **Headers to log** | `apim-request-id` | 记录 Foundry 返回的请求追踪 ID，用于向微软提 support ticket 时定位后端请求 |
| **Body bytes to log** | `1024` | 记录响应 Body 前 1KB，捕获错误 JSON 详情（如 `DeploymentNotFound`、`Too Many Requests` 等）|

> **📝 说明：**
>
> Headers to log 和 Body bytes 对**所有被采样的请求**生效（含成功请求），不区分成功/失败。这些数据会出现在 App Insights 的两个表中：
> - **`requests` 表** — 记录最终返回给客户端的请求（前端视角）
> - **`dependencies` 表** — 记录每次 `forward-request` 调用（后端视角，**含 Retry 中间的每次尝试**）
>
> 其中 `dependencies` 表是 Retry 可观测性的核心数据源。

点击 **Save** 完成配置。

> **⚠️ 注意：**
>
> Save 后配置需要**数分钟**传播到 APIM 网关实例。如果立即测试看不到数据，请等待 5 分钟后再进行查看。

### 5. 验证数据

配置完成后，发送几个会触发 Retry 的测试请求（例如调用一个不存在的模型部署），等待约 5 分钟后在 Application Insights 中验证数据。

##### 5-1) 进入 Application Insights → Monitoring → ① Logs，② 切换到 Tables 视图，③ 在 Application Insights 分类下找到 `dependencies` 表并点击 Run

![](images/5-1-dependencies-retry-records.png)

`dependencies` 表会为 `retry` 块内的**每次 `forward-request` 调用**生成一条独立记录——包括 Retry 中间失败的尝试和最终成功的请求。右侧结果中可以看到多条记录指向不同的后端（如 `ai-hub-swedencentral-02`、`ai-hub-eastus2-01` 等），它们属于同一请求的 Retry 链路。

##### 5-2) 展开单条记录，查看详细字段和 customDimensions

![](images/5-2-dependency-custom-dimensions.png)

展开后可以看到 dependency 记录的完整信息，其中高亮标注的关键排障字段：

| 字段 | 说明 |
|------|------|
| **`target`** | 请求的后端完整地址 |
| **`resultCode`** | HTTP 状态码 |
| `duration` | 调用耗时 |
| `success` | 是否成功 |
| **`Response-Body`** | 正确/错误响应 JSON 详情 |
| **`Response-apim-request-id`** | Foundry 端请求 ID（每次 Retry 不同），可用于提交排查工单用 |

> **💡 提示：**
>
> 使用 `operation_Id` 可以将同一请求的所有 Retry 记录串联起来，还原完整的重试链路。`Response-apim-request-id` 则可用于向微软提交 support ticket 时定位具体的后端请求。

### 6. 配置告警规则

当 Retry 失败次数超过阈值时，通过邮件自动通知运维团队。告警规则在 **Application Insights** 上创建（不是 APIM）。

##### 6-1) 在 Logs 页面编写 KQL 查询并验证

进入 Application Insights → Monitoring → **Logs**，① 新建一个查询标签页，② 切换到 **KQL mode**，③ 输入以下查询并 ④ 点击 **Run** 验证结果：

![](images/6-1-kql-query-in-logs.png)

```KQL
dependencies
| where success == false
| where resultCode in ("429", "500", "502", "503", "504") or toint(resultCode) >= 400
| summarize FailureCount = count()
```

根据需要调整状态码过滤条件：

| 场景 | 过滤条件 |
|------|---------|
| 所有失败 | `where success == false` |
| 仅限流（429） | `where resultCode == "429"` |
| 仅 5xx 服务端错误 | `where toint(resultCode) >= 500` |
| 429 + 5xx | `where resultCode == "429" or toint(resultCode) >= 500` |
| 排除 404 | `where success == false and resultCode != "404"` |

确认查询返回了预期的 FailureCount 数值。

##### 6-2) 点击右上角 **`...`** 菜单 → **+ New alert rule**

![](images/6-2-new-alert-rule.png)

系统会自动将当前 KQL 查询带入 Alert rule 的 Condition 配置中。

##### 6-3) 在 Condition 标签页中确认查询和 Measurement 配置

![](images/6-3-alert-condition-measurement.png)

截图中标注了三个关键配置：

| 标注 | 配置项 | 值 | 说明 |
|------|--------|-----|------|
| ① | **Search query** | 上一步的 KQL（自动带入） | 包含 `success == false` + 状态码过滤 + `summarize FailureCount = count()` |
| ② | **Measure** | `FailureCount` | ⚠️ 必须选 `FailureCount`（从 KQL 的 summarize 自动识别）。如果默认显示 `Table rows`，需手动切换 |
| ③ | **Aggregation granularity** | `3 hours` | 聚合粒度，将该时间范围内的 FailureCount 汇总为一个数据点进行评估 |

##### 6-4) 向下滚动配置 Alert logic

![](images/6-4-alert-logic-threshold.png)

| 配置项 | 值 | 说明 |
|--------|-----|------|
| Threshold type | **Static** | 使用固定阈值 |
| Operator | **Greater than** | 当 FailureCount 超过阈值时触发 |
| Threshold value | `10` | 按业务容忍度调整 |
| Frequency of evaluation | `15 minutes` | 每 15 分钟评估一次 |

> **📝 说明：**
>
> 📊 下方 **Preview** 图表会显示的 FailureCount 趋势和阈值线（虚线），帮助你判断阈值设置是否合理。图中蓝色实线超过虚线阈值线的区域即为会触发告警的时段。
>
> 💰 预估月费约 **$0.50 USD**（取决于评估频率）。

点击 **Next: Actions >** 进入下一步。

##### 6-5) 在 Actions 标签页中配置告警动作

如果 Portal 显示 **Use quick actions (preview)** 选项（新版 UI），可以直接在此页面完成 Action Group 创建，无需单独创建：

![](images/6-5-quick-actions-preview.png)

| 标注 | 配置项 | 说明 |
|------|--------|------|
| ① | **Use quick actions (preview)** | 选择此项，Portal 会自动创建 Action Group |
| ② | **Quick actions 面板** | 填写 Action group name、Display name，勾选 Email 并输入邮箱 → **Save** |
| ③ | **Email subject** | 自定义告警邮件标题，如 `AI Hub Retry Alert` |

> **📝 说明：**
>
> 如果 Portal 未显示 quick actions 选项（旧版 UI），则选择 **Use action groups** → **+ Create action group**，按以下 6-6 ~ 6-8 步骤手动创建。

##### 6-6) 填写 Action Group 基本信息

![](images/6-6-action-group-basics.png)

| 配置项 | 值 | 说明 |
|--------|-----|------|
| Region | **Global** | Action Group 建议选 Global |
| Action group name | `ai-hub-retry-alert-action` | 唯一标识 |
| Display name | `AI-Hub-Retry` | 限 12 字符，显示在通知中 |

##### 6-7) 切换到 Notifications 标签页，配置邮件通知

![](images/6-7-action-group-notifications.png)

| 配置项 | 值 | 说明 |
|--------|-----|------|
| Notification type | **Email/SMS message/Push/Voice** | 选择通知方式 |
| Name | 通知接收人名字                   | 通知接收人标识 |
| Email | ✅ 勾选并填写邮箱 | 告警邮件接收地址 |

> **📝 说明：**
>
> Actions 标签页中可以配置更丰富的自动化动作（Automation Runbook、Azure Function、Logic App、Webhook 等），本文暂不使用，直接跳过即可。
>
> ![](images/6-8-action-group-actions.png)

##### 6-8) 切换到 Review + create 标签页，确认配置并点击 **Create**

![](images/6-8-action-group-review-create.png)

创建完成后，你会收到一封 Azure 确认邮件，提示已加入 Action Group：

![](images/6-8-action-group-email-confirm.png)

##### 6-9) 返回 Alert rule 的 Actions 页面，确认 Action Group 已关联，填写邮件主题

![](images/6-9-alert-actions-email-subject.png)

在 **Email subject** 中填写自定义的告警邮件标题，例如 `AI Hub Retry Alert`。

##### 6-10) 切换到 Details 标签页，填写 Alert rule 基本信息

![](images/6-10-alert-details.png)

| 配置项 | 值 | 说明 |
|--------|-----|------|
| Severity | **2 - Warning** | 告警严重级别 |
| Alert rule name | `AI-Hub-Alert` | 告警规则名称 |
| Region | `Japan East` | 与 App Insights 同一区域 |
| Identity | **Default** | 使用默认身份 |

##### 6-11) 切换到 Review + create 确认所有配置，点击 **Create** 完成创建

![](images/6-11-alert-review-create.png)

##### 6-12) 验证告警邮件

创建完成后约 15 分钟，当 FailureCount 超过阈值（10）时，会收到告警邮件：

![](images/6-12-alert-email-notification.png)

邮件中包含关键信息：

| 字段 | 值 | 说明 |
|------|-----|------|
| Alert name | `AI-Hub-Alert` | 触发的告警规则名称 |
| Severity | Warning | 告警级别 |
| Metric value | 15 | 实际 FailureCount |
| Threshold | 10 | 配置的阈值 |
| Fired time | 具体时间 (UTC) | 告警触发时间 |

点击邮件中的 **View alert details** 可直接跳转到 Azure Portal 查看详情；**View search results** 可查看触发告警的 KQL 查询结果。

##### 6-13) （可选）调优告警参数

告警规则创建后，进入 Application Insights → Monitoring → **Alerts** → **Alert rules** → 选择对应规则 → 点击 **Edit** 按钮：

![](images/6-13-alert-edit-button.png)

在编辑页面的 **Details 标签页 → Advanced options** 中进一步调优：

![](images/6-13-alert-advanced-mute.png)

| 配置项 | 说明 | 建议值 |
|--------|------|--------|
| **Mute actions** | 触发后进入静默期，期间不再重复发送通知 | ✅ 勾选 |
| **Mute actions for** | 静默时长，在此期间即使条件持续满足也不再通知 | `3 hours`（按需调整） |
| **Automatically resolve alerts** | 当条件不再满足时自动将告警状态从 Fired 变为 Resolved | 按需勾选 |

> **💡 提示：**
>
> 如果评估频率为 15 分钟且未配置 Mute，告警条件持续满足时**每 15 分钟会发送一封通知邮件**。配置 Mute 后，触发一次告警后在静默期内不再重复通知，避免邮件轰炸。
>
> 此外还可以在编辑页面中调整 **Aggregation granularity（聚合粒度）**、**Threshold value（阈值）**、**Frequency of evaluation（评估频率）** 等参数，优化告警灵敏度。

### 7. 附录：进阶 KQL 查询与客户端 IP 配置（可选）

#### 7-1) 开启客户端真实 IP 记录

Application Insights **默认不存储客户端 IP 地址**（隐私保护），`client_IP` 字段会显示为 `0.0.0.0`。如果需要记录真实 IP 用于排障，需通过 CLI 关闭 IP 脱敏：

```bash
az resource update \
  --resource-group <resource-group> \
  --name <app-insights-name> \
  --resource-type "Microsoft.Insights/components" \
  --set properties.DisableIpMasking=true
```

> **⚠️ 注意：**
>
> 关闭 IP 脱敏后会记录真实客户端 IP 地址，请确认符合您组织的隐私合规要求。
>
> 📖 参考：Geolocation and IP address handling: https://learn.microsoft.com/azure/azure-monitor/app/ip-collection

#### 7-2) 关联客户端 IP 与 Retry 失败记录

`dependencies` 表本身没有客户端 IP（它记录的是 APIM → 后端的出站调用）。需要通过 `operation_Id` 与 `requests` 表 JOIN 获取：

```kusto
dependencies
| where timestamp > ago(1h)
| where success == false
| join kind=leftouter (
    requests 
    | project operation_Id, req_client_IP = client_IP
  ) on operation_Id
| project timestamp, target, resultCode, 
         ClientIP = req_client_IP,
         ErrorBody = tostring(customDimensions["Response-Body"]),
         APIMRequestId = tostring(customDimensions["Response-apim-request-id"]),
         operation_Id
| order by timestamp desc
```

> **📝 说明：**
>
> `requests` 和 `dependencies` 表都有 `client_IP` 字段，但含义不同：
> - **`requests.client_IP`** — 调用 APIM 的客户端 IP（真实客户端）
> - **`dependencies.client_IP`** — APIM 网关的出站 IP（不是客户端）
>
> JOIN 时需通过重命名（如 `req_client_IP`）避免字段冲突。

#### 7-3) 更多实用 KQL 查询

**按 operation_Id 还原完整 Retry 链路（含成功的那次）：**

```kusto
dependencies
| where timestamp > ago(1h)
| summarize CallCount = count(),
            Backends = make_list(target),
            StatusCodes = make_list(resultCode),
            Durations = make_list(duration)
  by operation_Id
| where CallCount > 1
| order by CallCount desc
```

**失败趋势图：**
```kusto
dependencies
| where timestamp > ago(24h)
| where success == false
| summarize FailureCount = count() by bin(timestamp, 5m), target
| render timechart
```

**告警用（按后端 + 状态码分组）：**
```kusto
dependencies
| where timestamp > ago(2h)
| where success == false
| summarize FailureCount = count() by target, resultCode
| where FailureCount > 0
```

### 总结

通过本文的实践，我们在上篇的韧性网关架构基础上完成了 Retry 可观测性的全链路搭建：

| 能力 | 实现方式 |
|------|---------|
| **每次 Retry 失败记录** | APIM 原生 `dependencies` 表自动记录每次 `forward-request` 调用 |
| **错误 Body 记录** | Backend Response Body bytes=1024，错误 JSON 详情出现在 Properties 中 |
| **请求追踪 ID** | `operation_Id`（跨 Retry 不变）+ `Response-apim-request-id`（Foundry 端 ID）|
| **调用耗时** | 原生 `DurationMs` 字段，精确到毫秒 |
| **KQL 查询** | 支持按后端、状态码、时间维度聚合分析 |
| **自动告警** | Log Alert 规则 + Action Group 邮件通知 |

对于已经部署了上篇韧性架构的用户，本文**无需修改任何 Policy 代码**——仅通过 APIM 的 Diagnostic Logs 配置（绑定 App Insights + **Verbosity 设为 Information** + 启用 Backend Response Headers/Body），即可获得完整的 Retry 可观测性。

这些被 Retry 机制隐藏的错误，现在都清晰地记录在 Application Insights 的 `dependencies` 表中，等待运维人员的检视和处理。

### 参考文档

| 文档 | 链接 |
|------|------|
| How to integrate Azure API Management with Azure Application Insights | https://learn.microsoft.com/azure/api-management/api-management-howto-app-insights |
| Diagnostic - Create Or Update REST API | https://learn.microsoft.com/rest/api/apimanagement/diagnostic/create-or-update |
| Application Insights telemetry data model | https://learn.microsoft.com/azure/azure-monitor/app/data-model-complete |
| Geolocation and IP address handling (IP masking) | https://learn.microsoft.com/azure/azure-monitor/app/ip-collection |
| Subscriptions in Azure API Management | https://learn.microsoft.com/azure/api-management/api-management-subscriptions |
| Tutorial: Create a log search alert for an Azure resource | https://learn.microsoft.com/azure/azure-monitor/alerts/tutorial-log-alert |
| Create and manage action groups | https://learn.microsoft.com/azure/azure-monitor/alerts/action-groups |
| Kusto Query Language (KQL) overview | https://learn.microsoft.com/azure/data-explorer/kusto/query/ |
| Performance implications and log sampling | https://learn.microsoft.com/azure/api-management/api-management-howto-app-insights#performance-implications-and-log-sampling |
| Azure Monitor pricing | https://azure.microsoft.com/pricing/details/monitor/ |
