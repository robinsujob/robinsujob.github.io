---
slug: "api-gateway-cors-configuration"
title: "API Gateway 跨域访问（CORS）配置指南"
date: 2024-10-28
description: "全面介绍 Amazon API Gateway 中 REST API 和 HTTP API 的 CORS 配置方法，以及开启授权时的注意事项。"
categories:
  - AWS
tags:
  - api-gateway
  - cors
  - serverless
---

CORS，全称为跨源资源共享（Cross-Origin Resource Sharing），是一种基于 HTTP 标头的机制，允许服务器标示哪些外部源（域、协议或端口）可以访问其资源。CORS 可以解决同源策略带来的不便，同源策略是浏览器的一种安全机制，它限制网页从不同的来源加载资源，以防止恶意网站窃取敏感数据。然而，这种限制也阻碍了合法的跨域请求。复杂的应用程序通常会在其客户端代码中引用第三方 API 和资源，当客户端域与服务器域不匹配时就需要 CORS。通过 CORS，浏览器能够安全地进行跨源数据传输，从而突破同源策略的限制。CORS 允许客户端浏览器在任何数据传输之前，先向第三方服务器检查请求是否被授权。由于 CORS 配置的复杂性，开发人员往往将跨域访问的权限设置得过大，比如在允许访问的标头中使用 "*" 来允许全部访问，这会对应用的安全性造成损害。

[Amazon API Gateway](https://aws.amazon.com/cn/api-gateway/?nc1=h_ls) 是一项帮助开发人员轻松管理任意规模的 API 的全托管服务，常被用于后端服务的管理与路由。因此，在 API Gateway 上配置 CORS 是一个很常见的需要。在 Amazon API Gateway 中，不同类型的 API 对于 CORS 有不同的配置方式，这增加了 CORS 配置的复杂度。

本文将介绍如何在 Amazon API Gateway 的 [REST API](https://docs.aws.amazon.com/zh_cn/apigateway/latest/developerguide/how-to-cors.html) 和 [HTTP API](https://docs.aws.amazon.com/zh_cn/apigateway/latest/developerguide/http-api-cors.html) 中进行跨源资源共享设置，其中将重点介绍 REST API 和 HTTP API 在跨源资源共享配置上的不同之处，以及在开启了授权验证（authorization）的情况下怎么配置跨源资源共享。通过阅读本文，您将掌握 Amazon API Gateway 中跨源资源共享的配置技巧，从而实现满足[最小权限原则](https://docs.aws.amazon.com/zh_cn/wellarchitected/latest/framework/sec_permissions_least_privileges.html)的跨域访问配置。

## CORS 原理

CORS 是一种基于 HTTP 标头的机制，服务器通过使用标头信息来限制访问。CORS 的工作主要依赖于以下几个[关键的 HTTP 标头](https://developer.mozilla.org/zh-CN/docs/Glossary/CORS#cors_%E6%A0%87%E5%A4%B4)：

- **Origin**：指示请求来源。
- **Access-Control-Allow-Origin**：指定哪些源可以访问资源。
- **Access-Control-Allow-Methods**：列出允许访问资源的 HTTP 方法。
- **Access-Control-Allow-Headers**：指示允许使用的自定义请求头。
- **Access-Control-Allow-Credentials**：指示是否允许发送凭据（如 Cookies）。
- **Access-Control-Max-Age**：指示预检请求结果可以被缓存多长时间。

根据请求的复杂程度，CORS 将其分为两类：

- **简单请求**：不需要预检。这类请求使用 GET/POST/HEAD 方法，并且只使用特定的安全头（如 Accept、Content-Type）。
- **非简单请求**：需要预检。除简单请求外的跨域请求都算是非简单请求。在发送实际请求之前，浏览器会先发送一个 OPTIONS 请求，以确认服务器是否允许该实际请求。这种预检机制可以防止未经授权的跨域操作对服务器数据产生副作用。

对于非简单请求，服务器依赖浏览器发送 [CORS 预检](https://developer.mozilla.org/zh-CN/docs/Glossary/Preflight_request)或 OPTIONS 请求。一个完整的请求过程如下：

![CORS 完整请求流程](images/cors-config-1.png)

非简单请求的 CORS 完整过程：

- 客户端应用程序发起请求
- 浏览器发送预检请求（preflight request）
- 服务器返回预检响应（preflight response）
- 浏览器发送实际的请求
- 服务器返回实际的响应
- 客户端接收到实际的响应

## API Gateway 介绍

[Amazon API Gateway](https://aws.amazon.com/cn/api-gateway/?nc1=h_ls) 是一项完全托管的服务，可以帮助开发人员轻松创建、发布、维护、监控和保护任意规模的 API。在您不需要维护其底层基础设施的情况下，API Gateway 能接受和处理成千上万个并发 API 调用。API Gateway 支持 RESTful 和 WebSocket 两种类型的 API，且支持多种类型的后端集成，如容器化服务、无服务器工作负载、HTTP 端点等。API Gateway 的其他关键功能还包括流量管理、CORS 支持、授权和访问控制、限制、监控，以及 API 版本管理等。

### REST API 与 HTTP API 的简介与区别

REST API 和 HTTP API 都是 Amazon API Gateway 的 RESTful API 类型产品。它们的区别如下。

#### 功能上

REST API 的特有功能包括：

- 支持 API 密钥
- 支持每客户端节流
- 支持请求验证
- 可以与 AWS WAF 集成
- 支持私有 API 端点

HTTP API 的设计初衷是仅保留最简化的功能。其特点包括：

- 自动部署
- 支持 default stage

#### 性能与价格上

由于 HTTP API 的功能更精简，因此它提供更快的速度和更低的价格。

## 在 API Gateway 中配置跨域访问

若需要在 Amazon API Gateway 中解决跨域问题，皆需通过 CORS 配置来执行。API Gateway 会自动通过 OPTIONS 方法，并尝试将 CORS 标头添加到现有的方法集成响应中，这将帮助您执行预检请求并进行实际响应。在 Amazon API Gateway 中，REST API 与 HTTP API 的跨域配置方式会有所不同。

### REST APIs 跨域访问配置

- 以下图为例，REST API 中有一个默认的 / 资源，我们在 / 资源下创建了一个 POST 方法，集成了 Lambda 函数作为后端服务。

![REST API 资源配置](images/cors-config-2.png)

- 如果想要为 / 资源下的 POST 方法配置跨域访问，我们需要回到资源的简介页面，点击启用 CORS。

![启用 CORS 按钮](images/cors-config-3.png)

- 在启用 CORS 页面，首先配置访问控制允许的方法。为了正确的响应 preflight 请求，OPTIONS 方法已被默认开启。我们勾选需要配置跨域访问的 POST 方法。随后，我们配置访问控制允许的标头和来源，具体允许的值取决于您的后端应用。配置好后点击保存。

![CORS 配置页面](images/cors-config-4.png)

- 保存之后，在 POST 方法的集成响应页面可以看到，标头映射中，Access-Control-Allow-Origin 的映射值为上一步配置的访问控制允许的来源。

![集成响应标头映射](images/cors-config-5.png)

- 在资源列表我们还可以看到，在启用 CORS 之后，API Gateway 为我们自动创建了 OPTIONS 方法，该方法用于正确响应 preflight 请求。OPTIONS 方法的集成类型为模拟集成，模拟集成会为请求返回一个 200 的状态码，并且返回 preflight 响应的所有相关标头，标头的映射值由第 3 步中的设置决定。

![OPTIONS 方法配置](images/cors-config-6.png)

- 在第 3 步中配置的访问控制允许的来源端点上测试跨域 POST 请求，可以看到，对于 preflight 请求和实际请求，REST API 都返回了相应的标头。

![Preflight 请求响应](images/cors-config-7.png)

![实际请求响应](images/cors-config-8.png)

- 对于非根路径，也可以在创建资源时直接勾选 CORS（跨源资源共享），这样 API Gateway 会自动在这个资源下创建一个 OPTIONS 方法处理 preflight 请求。

![创建资源时勾选 CORS](images/cors-config-9.png)

需要注意的是，使用这种方法创建的 OPTIONS 方法默认会接受来自所有源、所有方法的跨域请求，如果需要缩小权限可以点击右上角的编辑进行修改。

![编辑 OPTIONS 方法](images/cors-config-10.png)

在创建资源时勾选 CORS（跨源资源共享）后，依旧要在资源简介页面的右上角点击启用 CORS（具体方法同步骤 3），为具体的请求方法（如 POST）配置跨域相关的标头。

![为具体方法配置 CORS 标头](images/cors-config-11.png)

#### 附加授权的跨域配置场景

您可以为您的 REST API 集成 [Lambda 授权方](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html) 或者 [Cognito 授权方](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html)。开启授权时，请注意只为需要的方法开启授权，不要为 OPTIONS 方法开启授权，否则将导致 preflight 请求（未授权）出现 401 错误。

![为 POST 方法开启授权](images/cors-config-12.png)

为 POST 方法开启授权

![如果为 OPTIONS 方法开启授权，preflight 请求会出现错误](images/cors-config-13.png)

如果为 OPTIONS 方法开启授权，preflight 请求会出现错误

![不要为 OPTIONS 方法开启授权](images/cors-config-14.png)

不要为 OPTIONS 方法开启授权

### HTTP APIs 跨域访问配置

在这一章节中，我们依旧以为 / 资源下的 POST 方法配置跨域访问为例，展示如何为 HTTP API 配置跨域访问。

HTTP API 的 CORS 配置相对简单，因为您一旦为您的 HTTP API 开启跨域访问，API Gateway 会自动响应浏览器发来的 preflight 请求，并且自动为您的后端返回添加 CORS 相关的标头。您无法在您的 API 资源中看到 API Gateway 自动响应 preflight 请求的 OPTIONS 方法的配置，也看不到 POST 方法的响应标头的配置。

以下为开启 HTTP API 跨域访问的详细步骤。

- 进入 HTTP API 的页面，在左侧导航栏中点击 CORS，随后在右上角点击配置。

![HTTP API CORS 配置入口](images/cors-config-15.png)

- 在配置 CORS 的页面，依次输入访问控制允许的来源、标头、方法。在我们的例子中，我们需要允许 POST 方法的访问。根据您的需要，您也可以选择性地配置访问控制公开标头、访问控制最长期限、访问控制允许凭证。配置完成后，点击右下角保存。

![HTTP API CORS 配置页面](images/cors-config-16.png)

- 配置好后，我们在 HTTP API 的路由页面看不到 OPTIONS 方法的配置。

![HTTP API 路由页面](images/cors-config-17.png)

- 在 HTTP API 允许的跨域访问来源端点上测试跨域 POST 请求，可以看到，preflight 的 OPTIONS 请求和实际的 POST 请求都能得到正确响应。这是因为 API Gateway 替我们完成了 HTTP API 对 preflight 请求的响应和 CORS 相关的标头的添加。

![HTTP API CORS 测试结果](images/cors-config-18.png)

#### 附加授权的跨域配置场景

类似于 REST API，HTTP API 支持通过 [Lambda](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html)，[JWT](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html)，[IAM](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control-iam.html) 三种授权方为特定的方法授权。如果您想为集成了授权方的 HTTP API 开启跨域访问，在大多数情况下，HTTP API 会自动为您处理 preflight 请求。因此，您无需进行特殊配置，按照上述步骤即可为集成了授权方的 HTTP API 开启跨域访问。唯一的例外是，当您创建了授权的 ANY 方法时（如下图），则需要注意，这种情况下，preflight 请求也会由 ANY 方法而不会由 HTTP API 处理。而 preflight 请求中不包含授权信息，因此授权的 ANY 方法不会返回正确的状态码和跨域标头，preflight 请求会出现 401 错误。

![授权的 ANY 方法](images/cors-config-19.png)

![ANY 方法导致的 401 错误](images/cors-config-20.png)

这种情况下，有两种解决方法：

- （推荐方法）根据需要为每种方法和资源创建一个特定的路由，尽量避免使用 ANY 方法。比如，在本文的例子中，我只需要为 POST 方法创建路由。

![为特定方法创建路由](images/cors-config-21.png)

- 在同一资源路径下创建一个无需授权的 OPTIONS 方法路由，并为 OPTIONS 方法添加一个任意后端集成（如下图）。这样无授权的 OPTIONS 路由会捕捉 preflight 请求。

![创建无授权的 OPTIONS 路由](images/cors-config-22.png)

## 总结

本文介绍了 Amazon API Gateway 中 REST API 和 HTTP API 的跨域访问配置方式，并特别介绍了开启授权的情况下两种 API 要如何设置才能保证 preflight 请求被正确响应。两种 API 的跨域访问配置方式区别如下：

| API 类型 | 跨域访问配置方法 | 跨域访问配置特点 | 授权方法跨域访问注意事项 |
|---|---|---|---|
| REST API | 可以为 REST API 特定路由配置跨域，具体方法为在该路由下点击右上角启用 CORS 对跨域访问进行配置。 | 可以在所配置的路由下看到用于响应 preflight 请求的 OPTIONS 方法及其响应的标头设置。可以在允许跨域访问的方法下看到其响应中跨域标头的设置。 | 不要为 OPTIONS 方法开启授权。 |
| HTTP API | 可以为整个 HTTP API 配置跨域，具体方法点击左侧导航栏的 CORS 进入跨域访问的配置页面。 | preflight 请求由 API Gateway 自动响应，在控制台中看不到自动响应的 OPTIONS 方法的配置。跨域访问的标头由 API Gateway 自动添加，在允许跨域访问的方法下也看不到其响应中跨域标头的设置。 | 尽量避免使用 ANY 方法，如果必须使用，则另外创建一个不需要授权的 OPTIONS 方法用于 preflight 请求的响应。 |

## 相关资源

- [为 CloudFront 开启 CORS](https://aws.amazon.com/cn/blogs/china/several-solutions-to-cloudfront-cross-domain-problem-cors/)
- [为 Lambda 函数 URL 开启 CORS](https://aws.amazon.com/cn/blogs/china/several-solutions-to-cloudfront-cross-domain-problem-cors/)
- [为托管静态网站的 S3 开启 CORS](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/cors.html)

---

> 原文链接：[Amazon API Gateway 跨域请求（CORS）配置 - 亚马逊AWS官方博客](https://aws.amazon.com/cn/blogs/china/amazon-api-gateway-cross-origin-resource-sharing-configuration/)
