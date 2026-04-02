---
slug: "china-cloudfront-ssl-plugin-v2"
title: "China CloudFront SSL Plugin V2 - One-Stop Free SSL Certificate Management for China CloudFront"
date: 2025-08-19
description: "A comprehensive SSL certificate management solution for China region CloudFront distributions."
image: /images/posts/cloudfront-ssl-v2/architecture.png
categories:
  - AWS
tags:
  - cloudfront
  - ssl
  - serverless
  - china
---

> Original: [AWS Blog](https://aws.amazon.com/cn/blogs/china/china-cloudfront-ssl-plugin-v2-a-one-stop-certificate-solution-for-cloudfront-in-china-region/) | [GitHub](https://github.com/aws-samples/sample-China-CloudFront-SSL-Plugin-V2)

在当今数字时代，网站安全至关重要。SSL 证书作为保护网站数据传输安全的重要工具，其管理和更新一直是开发运维人员关注的焦点。在 2023 年我们发布了 China CloudFront SSL Plugin 方便中国区 CloudFront 与免费 SSL 证书的集成。现在，我们很高兴地宣布第二代版本正式发布。

*In today's digital age, website security is paramount. In 2023, we released China CloudFront SSL Plugin for free SSL integration with CloudFront in China region. Now we're pleased to announce V2.*

## 全新升级，更强大的功能 / Core Upgrades

V2 带来了三大核心升级，让证书管理更简单、更安全、更高效。

*V2 introduces three core upgrades making certificate management simpler, safer, and more efficient.*

### 1. 多项目统一管理 / Multi-Project Management

- **V1**：每个堆栈仅支持单个项目，多项目需部署多个堆栈 / Each stack managed one project only
- **V2**：单一堆栈统一管理多个项目 / Single stack manages multiple projects

### 2. 图形化界面 / Graphical Interface

- **V1**：Swagger UI，需手动构造 API 请求 / Manual API request construction
- **V2**：直观 GUI，按钮点击完成操作 / Intuitive GUI with button clicks

### 3. 安全认证 / Security Auth

- **V1**：外部 API 缺乏安全校验 / No API security validation
- **V2**：Access Key 验证机制 / Access Key authentication required

### 保留的核心特性 / Retained Features

*While bringing new features, we retained the most popular characteristics:*

✓ **成本优势 / Cost** — 无服务器架构，按调用计费，证书每30天自动更新，极少存储费用 / Serverless, pay-per-use, auto-renewal every 30 days

✓ **运营自动化 / Automation** — CloudFront 无缝集成，证书自动替换，EventBridge 定时更新 / Seamless integration, auto replacement, EventBridge scheduling

✓ **运维透明 / Transparency** — 邮件通知全生命周期，图形化控制面板，多项目监控 / Email notifications, graphical dashboard, multi-project monitoring

✓ **代码开源 / Open Source** — 所有代码开源，支持定制开发 / All code open source, supports customization

## 技术架构 / Architecture

基于无服务器架构，通过 CloudFormation 一键部署。

*Built on serverless architecture with one-click CloudFormation deployment.*

![Architecture](/images/posts/cloudfront-ssl-v2/architecture.png)

**核心组件 / Core Components**: Let's Encrypt + Certbot + Lambda + API Gateway

**存储 / Storage**: DynamoDB (状态/status) + S3 (备份/backup) + IAM SSL (CloudFront 关联/association)

**自动化 / Automation**: SNS (邮件通知/notifications) + EventBridge (定时更新/scheduled renewal, 默认30天/default 30 days)

## 部署演示 / Deployment Demo

### 创建管理堆栈 / Create Stack

通过 CloudFormation 模板一键部署主堆栈（Lambda、API Gateway、DynamoDB），指定堆栈名称和 Access Key，3-5 分钟完成。

*Deploy the main stack via CloudFormation template in 3-5 minutes with a stack name and Access Key.*

![Create Stack](/images/posts/cloudfront-ssl-v2/new-stack.gif)

### 创建证书项目 / Create Certificate Project

在 GUI 中创建证书项目，为域名集合申请 Let's Encrypt 证书。支持多域名（逗号分隔），可设邮箱通知和更新间隔（推荐30天）。系统自动部署子堆栈。

*Create certificate projects in the GUI for domain sets. Supports multiple domains, configurable email and renewal intervals (30 days recommended). System auto-deploys sub-stacks.*

![Create Project](/images/posts/cloudfront-ssl-v2/create-project.gif)

### 附加证书到 CloudFront / Attach to CloudFront

证书颁发后自动上传到 IAM SSL 存储，在 CloudFront 控制台选择即可。后续自动更新无缝替换，无需手动干预。

*Certificates auto-upload to IAM SSL storage. Select in CloudFront console. Subsequent renewals replace seamlessly without manual intervention.*

![Attach SSL](/images/posts/cloudfront-ssl-v2/attach-ssl.gif)

### 更新证书项目 / Update Project

可随时更新域名列表和更新间隔，每次修改触发新证书颁发。系统自动处理 CloudFront 证书更新和旧证书清理。

*Update domain lists and intervals anytime; each change triggers re-issuance. Auto-handles certificate updates and cleanup.*

![Update Project](/images/posts/cloudfront-ssl-v2/update-project.gif)

### 重新颁发证书 / Re-issue Certificate

手动控制证书更新，适用于故障恢复、紧急更新或测试。系统重新执行完整的证书申请、验证、颁发和 CloudFront 更新流程。

*Manual certificate update control for fault recovery, emergency updates, or testing. Re-executes the full certificate lifecycle.*

![Re-issue](/images/posts/cloudfront-ssl-v2/recert.gif)

- 部署链接 / Deploy: [一键部署 V2](https://console.amazonaws.cn/cloudformation/home?#/stacks/create/template?templateURL=https://aws-cn-getting-started.s3.cn-northwest-1.amazonaws.com.cn/china-cloudfront-ssl-plugin_v2/ChinaCloudFrontSslPluginStackV2.template.json)
- 完整教程 / Tutorial: [V2 教程](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/)

## 总结 / Summary

V2 通过多项目管理架构、图形化界面和增强安全机制，为中国区 CloudFront 用户提供更便捷的证书解决方案。

*V2 delivers a more convenient certificate solution through multi-project architecture, graphical UI, and enhanced security.*

## 资源 / Resources

- [V2 教程 / Tutorial](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/)
- [GitHub V2](https://github.com/aws-samples/sample-China-CloudFront-SSL-Plugin-V2)
- [GitHub V1](https://github.com/aws-samples/China-CloudFront-SSL-Plugin)
- [CloudFront 中国区差异 / China Differences](https://docs.amazonaws.cn/aws/latest/userguide/cloudfront.html#feature-diff)
- [IAM SSL 证书管理 / Certificate Management](https://docs.amazonaws.cn/IAM/latest/UserGuide/id_credentials_server-certs.html)
- [Let's Encrypt 文档 / Docs](https://letsencrypt.org/zh-cn/docs/)
- [Certbot 文档 / Docs](https://certbot.eff.org/pages/about)
- [联系我们 / Contact](mailto:china-cloudfront-ssl-plugin@amazon.com)
