---
slug: "api-gateway-cors-configuration"
title: "API Gateway CORS Configuration Guide"
date: 2024-10-28
description: "Complete guide to configuring CORS for AWS API Gateway."
image: /images/posts/api-gateway-cors/cors-flow.png
categories:
  - AWS
tags:
  - api-gateway
  - cors
  - serverless
---

> 原文链接：[Amazon API Gateway 跨域请求（CORS）配置 - 亚马逊AWS官方博客](https://aws.amazon.com/cn/blogs/china/amazon-api-gateway-cross-origin-resource-sharing-configuration/)

CORS，全称为跨源资源共享（Cross-Origin Resource Sharing），是一种基于 HTTP 标头的机制，允许服务器标示哪些外部源（域、协议或端口）可以访问其资源。CORS 可以解决同源策略带来的不便，同源策略是浏览器的一种安全机制，它限制网页从不同的来源加载资源，以防止恶意网站窃取敏感数据。然而，这种限制也阻碍了合法的跨域请求。复杂的应用程序通常会在其客户端代码中引用第三方API和资源，当客户端域与服务器域不匹配时就需要 CORS。通过 CORS，浏览器能够安全地进行跨源数据传输，从而突破同源策略的限制。CORS 允许客户端浏览器在任何数据传输之前,先向第三方服务器检查请求是否被授权。由于 CORS 配置的复杂性，开发人员往往将跨域访问的权限设置得过大，比如在允许访问的标头中使用 "*" 来允许全部访问，这会对应用的安全性造成损害。

CORS, or Cross-Origin Resource Sharing, is an HTTP header-based mechanism that allows servers to indicate which external origins (domains, protocols, or ports) can access their resources. CORS addresses the inconveniences of the same-origin policy—a browser security mechanism that restricts web pages from loading resources from different origins to prevent malicious websites from stealing sensitive data. However, this restriction also blocks legitimate cross-origin requests. Complex applications often reference third-party APIs and resources in their client-side code, and CORS is needed when the client domain doesn't match the server domain. Through CORS, browsers can safely perform cross-origin data transfers, breaking through same-origin policy restrictions. CORS allows client browsers to check with third-party servers whether a request is authorized before any data transfer. Due to the complexity of CORS configuration, developers often set cross-origin access permissions too broadly—for example, using "*" in allowed headers to permit all access—which can compromise application security.

[Amazon API Gateway](https://aws.amazon.com/cn/api-gateway/) 是一项帮助开发人员轻松管理任意规模的 API 的全托管服务，常被用于后端服务的管理与路由。因此，在 API Gateway 上配置 CORS 是一个很常见的需要。在 Amazon API Gateway 中，不同类型的 API 对于 CORS 有不同的配置方式，这增加了 CORS 配置的复杂度。

[Amazon API Gateway](https://aws.amazon.com/cn/api-gateway/) is a fully managed service that helps developers easily manage APIs at any scale, commonly used for backend service management and routing. Therefore, configuring CORS on API Gateway is a very common requirement. In Amazon API Gateway, different types of APIs have different CORS configuration methods, which adds to the complexity of CORS configuration.

本文将介绍如何在 Amazon API Gateway 的 REST API 和 HTTP API 中进行跨源资源共享设置，其中将重点介绍 REST API 和 HTTP API 在跨源资源共享配置上的不同之处，以及在开启了授权验证（authorization）的情况下怎么配置跨源资源共享。通过阅读本文，您将掌握 Amazon API Gateway 中跨源资源共享的配置技巧，从而实现满足最小权限原则的跨域访问配置。

This article will explain how to configure Cross-Origin Resource Sharing in Amazon API Gateway's REST API and HTTP API, with a focus on the differences between REST API and HTTP API CORS configurations, and how to configure CORS when authorization is enabled. After reading this article, you will master CORS configuration techniques in Amazon API Gateway to achieve cross-origin access configurations that meet the principle of least privilege.

## CORS 原理 / How CORS Works

CORS 是一种基于 HTTP 标头的机制，服务器通过使用标头信息来限制访问。CORS 的工作主要依赖于以下几个关键的 HTTP 标头：

CORS is an HTTP header-based mechanism where servers use header information to restrict access. CORS primarily relies on the following key HTTP headers:

- **Origin**：指示请求来源。/ Indicates the request origin.
- **Access-Control-Allow-Origin**：指定哪些源可以访问资源。/ Specifies which origins can access the resource.
- **Access-Control-Allow-Methods**：列出允许访问资源的 HTTP 方法。/ Lists the HTTP methods allowed to access the resource.
- **Access-Control-Allow-Headers**：指示允许使用的自定义请求头。/ Indicates which custom request headers are allowed.
- **Access-Control-Allow-Credentials**：指示是否允许发送凭据（如 Cookies）。/ Indicates whether credentials (such as Cookies) are allowed.
- **Access-Control-Max-Age**：指示预检请求结果可以被缓存多长时间。/ Indicates how long preflight request results can be cached.

根据请求的复杂程度，CORS 将其分为两类：

Based on request complexity, CORS divides requests into two categories:

- **简单请求 / Simple requests**：不需要预检。这类请求使用 GET/POST/HEAD 方法，并且只使用特定的安全头（如 Accept、Content-Type）。/ No preflight needed. These requests use GET/POST/HEAD methods and only use specific safe headers (such as Accept, Content-Type).
- **非简单请求 / Non-simple requests**：需要预检。除简单请求外的跨域请求都算是非简单请求。在发送实际请求之前，浏览器会先发送一个 OPTIONS 请求，以确认服务器是否允许该实际请求。/ Preflight required. Any cross-origin request that isn't a simple request is considered non-simple. Before sending the actual request, the browser first sends an OPTIONS request to confirm whether the server allows the actual request.

对于非简单请求，服务器依赖浏览器发送 CORS 预检或 OPTIONS 请求。一个完整的请求过程如下：

For non-simple requests, the server relies on the browser sending a CORS preflight or OPTIONS request. A complete request process is as follows:

![CORS 完整请求流程 / Complete CORS Request Flow](/images/posts/api-gateway-cors/cors-config-1.png)

非简单请求的 CORS 完整过程：

The complete CORS process for non-simple requests:

1. 客户端应用程序发起请求 / Client application initiates the request
2. 浏览器发送预检请求（preflight request）/ Browser sends a preflight request
3. 服务器返回预检响应（preflight response）/ Server returns a preflight response
4. 浏览器发送实际的请求 / Browser sends the actual request
5. 服务器返回实际的响应 / Server returns the actual response
6. 客户端接收到实际的响应 / Client receives the actual response

## API Gateway 介绍 / Introduction to API Gateway

[Amazon API Gateway](https://aws.amazon.com/cn/api-gateway/) 是一项完全托管的服务，可以帮助开发人员轻松创建、发布、维护、监控和保护任意规模的 API。在您不需要维护其底层基础设施的情况下，API Gateway 能接受和处理成千上万个并发 API 调用。API Gateway 支持 RESTful 和 WebSocket 两种类型的 API，且支持多种类型的后端集成，如容器化服务、无服务器工作负载、HTTP 端点等。

Amazon API Gateway is a fully managed service that helps developers easily create, publish, maintain, monitor, and secure APIs at any scale. Without requiring you to maintain the underlying infrastructure, API Gateway can accept and process thousands of concurrent API calls. API Gateway supports both RESTful and WebSocket API types, and supports multiple backend integration types such as containerized services, serverless workloads, and HTTP endpoints.

### REST API 与 HTTP API 的简介与区别 / REST API vs HTTP API

REST API 和 HTTP API 都是 Amazon API Gateway 的 RESTful API 类型产品。它们的区别如下。

Both REST API and HTTP API are RESTful API products of Amazon API Gateway. Their differences are as follows.

#### 功能上 / Features

REST API 的特有功能包括：/ REST API unique features include:

- 支持 API 密钥 / API key support
- 支持每客户端节流 / Per-client throttling
- 支持请求验证 / Request validation
- 可以与 AWS WAF 集成 / AWS WAF integration
- 支持私有 API 端点 / Private API endpoints

HTTP API 的设计初衷是仅保留最简化的功能：/ HTTP API is designed with minimal features:

- 自动部署 / Automatic deployment
- 支持 default stage / Default stage support

#### 性能与价格上 / Performance & Pricing

由于 HTTP API 的功能更精简，因此它提供更快的速度和更低的价格。

Since HTTP API has streamlined features, it offers faster speed and lower pricing.

## 在 API Gateway 中配置跨域访问 / Configuring CORS in API Gateway

若需要在 Amazon API Gateway 中解决跨域问题，皆需通过 CORS 配置来执行。API Gateway 会自动通过 OPTIONS 方法，并尝试将 CORS 标头添加到现有的方法集成响应中。在 Amazon API Gateway 中，REST API 与 HTTP API 的跨域配置方式会有所不同。

To resolve cross-origin issues in Amazon API Gateway, CORS configuration is required. API Gateway automatically handles OPTIONS methods and attempts to add CORS headers to existing method integration responses. In Amazon API Gateway, the CORS configuration methods differ between REST API and HTTP API.

### REST APIs 跨域访问配置 / REST API CORS Configuration

以下图为例，REST API 中有一个默认的 / 资源，我们在 / 资源下创建了一个 POST 方法，集成了 Lambda 函数作为后端服务。

As shown below, the REST API has a default / resource, and we created a POST method under the / resource, integrated with a Lambda function as the backend service.

![REST API 资源配置](/images/posts/api-gateway-cors/cors-config-2.png)

如果想要为 / 资源下的 POST 方法配置跨域访问，我们需要回到资源的简介页面，点击启用 CORS。

To configure CORS for the POST method under the / resource, we need to go back to the resource overview page and click Enable CORS.

![启用 CORS 按钮](/images/posts/api-gateway-cors/cors-config-3.png)

在启用 CORS 页面，首先配置访问控制允许的方法。为了正确的响应 preflight 请求，OPTIONS 方法已被默认开启。我们勾选需要配置跨域访问的 POST 方法。随后，我们配置访问控制允许的标头和来源，具体允许的值取决于您的后端应用。配置好后点击保存。

On the Enable CORS page, first configure the allowed methods. The OPTIONS method is enabled by default to properly respond to preflight requests. We select the POST method that needs CORS configuration. Then we configure the allowed headers and origins—the specific allowed values depend on your backend application. Click Save after configuration.

![CORS 配置页面](/images/posts/api-gateway-cors/cors-config-4.png)

保存之后，在 POST 方法的集成响应页面可以看到，标头映射中，Access-Control-Allow-Origin 的映射值为上一步配置的访问控制允许的来源。

After saving, on the POST method's integration response page, you can see that in the header mapping, the Access-Control-Allow-Origin mapping value is the allowed origin configured in the previous step.

![集成响应标头映射](/images/posts/api-gateway-cors/cors-config-5.png)

在资源列表我们还可以看到，在启用 CORS 之后，API Gateway 为我们自动创建了 OPTIONS 方法，该方法用于正确响应 preflight 请求。OPTIONS 方法的集成类型为模拟集成，模拟集成会为请求返回一个 200 的状态码，并且返回 preflight 响应的所有相关标头。

In the resource list, we can also see that after enabling CORS, API Gateway automatically created an OPTIONS method for properly responding to preflight requests. The OPTIONS method's integration type is Mock integration, which returns a 200 status code and all relevant preflight response headers.

![OPTIONS 方法配置](/images/posts/api-gateway-cors/cors-config-6.png)

在配置的访问控制允许的来源端点上测试跨域 POST 请求，可以看到，对于 preflight 请求和实际请求，REST API 都返回了相应的标头。

Testing a cross-origin POST request on the configured allowed origin endpoint shows that the REST API returns the appropriate headers for both the preflight request and the actual request.

![Preflight 请求响应](/images/posts/api-gateway-cors/cors-config-7.png)

![实际请求响应](/images/posts/api-gateway-cors/cors-config-8.png)

对于非根路径，也可以在创建资源时直接勾选 CORS（跨源资源共享），这样 API Gateway 会自动在这个资源下创建一个 OPTIONS 方法处理 preflight 请求。

For non-root paths, you can also check CORS (Cross-Origin Resource Sharing) when creating a resource, so API Gateway will automatically create an OPTIONS method under this resource to handle preflight requests.

![创建资源时勾选 CORS](/images/posts/api-gateway-cors/cors-config-9.png)

需要注意的是，使用这种方法创建的 OPTIONS 方法默认会接受来自所有源、所有方法的跨域请求，如果需要缩小权限可以点击右上角的编辑进行修改。

Note that the OPTIONS method created this way will accept cross-origin requests from all origins and all methods by default. If you need to narrow the permissions, you can click Edit in the upper right corner to modify.

![编辑 OPTIONS 方法](/images/posts/api-gateway-cors/cors-config-10.png)

在创建资源时勾选 CORS（跨源资源共享）后，依旧要在资源简介页面的右上角点击启用 CORS，为具体的请求方法（如 POST）配置跨域相关的标头。

After checking CORS when creating a resource, you still need to click Enable CORS in the upper right corner of the resource overview page to configure CORS-related headers for specific request methods (such as POST).

![为具体方法配置 CORS 标头](/images/posts/api-gateway-cors/cors-config-11.png)

#### 附加授权的跨域配置场景 / CORS Configuration with Authorization

您可以为您的 REST API 集成 Lambda 授权方或者 Cognito 授权方。开启授权时，请注意只为需要的方法开启授权，不要为 OPTIONS 方法开启授权，否则将导致 preflight 请求（未授权）出现 401 错误。

You can integrate Lambda authorizers or Cognito authorizers for your REST API. When enabling authorization, note that you should only enable it for the methods that need it—do not enable authorization for the OPTIONS method, as this will cause 401 errors for preflight requests (which are unauthorized).

![为 POST 方法开启授权](/images/posts/api-gateway-cors/cors-config-12.png)

*为 POST 方法开启授权 / Enable authorization for the POST method*

![如果为 OPTIONS 方法开启授权，preflight 请求会出现错误](/images/posts/api-gateway-cors/cors-config-13.png)

*如果为 OPTIONS 方法开启授权，preflight 请求会出现错误 / If authorization is enabled for the OPTIONS method, preflight requests will fail*

![不要为 OPTIONS 方法开启授权](/images/posts/api-gateway-cors/cors-config-14.png)

*不要为 OPTIONS 方法开启授权 / Do not enable authorization for the OPTIONS method*

### HTTP APIs 跨域访问配置 / HTTP API CORS Configuration

在这一章节中，我们依旧以为 / 资源下的 POST 方法配置跨域访问为例，展示如何为 HTTP API 配置跨域访问。

In this section, we continue using the example of configuring CORS for the POST method under the / resource to demonstrate how to configure CORS for HTTP API.

HTTP API 的 CORS 配置相对简单，因为您一旦为您的 HTTP API 开启跨域访问，API Gateway 会自动响应浏览器发来的 preflight 请求，并且自动为您的后端返回添加 CORS 相关的标头。您无法在您的 API 资源中看到 API Gateway 自动响应 preflight 请求的 OPTIONS 方法的配置，也看不到 POST 方法的响应标头的配置。

HTTP API CORS configuration is relatively simple because once you enable CORS for your HTTP API, API Gateway automatically responds to preflight requests from browsers and automatically adds CORS-related headers to your backend responses. You won't be able to see the OPTIONS method configuration for API Gateway's automatic preflight responses in your API resources, nor the response header configuration for the POST method.

以下为开启 HTTP API 跨域访问的详细步骤。

Below are the detailed steps for enabling HTTP API CORS.

进入 HTTP API 的页面，在左侧导航栏中点击 CORS，随后在右上角点击配置。

Navigate to the HTTP API page, click CORS in the left navigation bar, then click Configure in the upper right corner.

![HTTP API CORS 配置入口](/images/posts/api-gateway-cors/cors-config-15.png)

在配置 CORS 的页面，依次输入访问控制允许的来源、标头、方法。根据您的需要，您也可以选择性地配置访问控制公开标头、访问控制最长期限、访问控制允许凭证。配置完成后，点击右下角保存。

On the CORS configuration page, enter the allowed origins, headers, and methods. Optionally, you can also configure exposed headers, max age, and allow credentials. Click Save in the lower right corner after configuration.

![HTTP API CORS 配置页面](/images/posts/api-gateway-cors/cors-config-16.png)

配置好后，我们在 HTTP API 的路由页面看不到 OPTIONS 方法的配置。

After configuration, we cannot see the OPTIONS method configuration on the HTTP API routes page.

![HTTP API 路由页面](/images/posts/api-gateway-cors/cors-config-17.png)

在 HTTP API 允许的跨域访问来源端点上测试跨域 POST 请求，可以看到，preflight 的 OPTIONS 请求和实际的 POST 请求都能得到正确响应。这是因为 API Gateway 替我们完成了 HTTP API 对 preflight 请求的响应和 CORS 相关的标头的添加。

Testing a cross-origin POST request on the HTTP API's allowed origin endpoint shows that both the preflight OPTIONS request and the actual POST request receive correct responses. This is because API Gateway handles the HTTP API's preflight request responses and CORS header additions for us.

![HTTP API CORS 测试结果](/images/posts/api-gateway-cors/cors-config-18.png)

#### 附加授权的跨域配置场景 / CORS Configuration with Authorization

类似于 REST API，HTTP API 支持通过 Lambda、JWT、IAM 三种授权方为特定的方法授权。如果您想为集成了授权方的 HTTP API 开启跨域访问，在大多数情况下，HTTP API 会自动为您处理 preflight 请求。因此，您无需进行特殊配置。唯一的例外是，当您创建了授权的 ANY 方法时，preflight 请求也会由 ANY 方法而不会由 HTTP API 处理。而 preflight 请求中不包含授权信息，因此授权的 ANY 方法不会返回正确的状态码和跨域标头，preflight 请求会出现 401 错误。

Similar to REST API, HTTP API supports authorization through Lambda, JWT, and IAM authorizers for specific methods. If you want to enable CORS for an HTTP API with integrated authorizers, in most cases HTTP API will automatically handle preflight requests for you, requiring no special configuration. The only exception is when you create an authorized ANY method—in this case, preflight requests will be handled by the ANY method instead of HTTP API. Since preflight requests don't include authorization information, the authorized ANY method won't return the correct status code and CORS headers, resulting in 401 errors.

![授权的 ANY 方法](/images/posts/api-gateway-cors/cors-config-19.png)

![ANY 方法导致的 401 错误](/images/posts/api-gateway-cors/cors-config-20.png)

这种情况下，有两种解决方法：

In this case, there are two solutions:

**（推荐方法）** 根据需要为每种方法和资源创建一个特定的路由，尽量避免使用 ANY 方法。比如，在本文的例子中，我只需要为 POST 方法创建路由。

**(Recommended)** Create a specific route for each method and resource as needed, and avoid using the ANY method. For example, in this article's case, you only need to create a route for the POST method.

![为特定方法创建路由](/images/posts/api-gateway-cors/cors-config-21.png)

在同一资源路径下创建一个无需授权的 OPTIONS 方法路由，并为 OPTIONS 方法添加一个任意后端集成。这样无授权的 OPTIONS 路由会捕捉 preflight 请求。

Create an unauthorized OPTIONS method route under the same resource path, and add any backend integration for the OPTIONS method. This way, the unauthorized OPTIONS route will capture preflight requests.

![创建无授权的 OPTIONS 路由](/images/posts/api-gateway-cors/cors-config-22.png)

## 总结 / Summary

本文介绍了 Amazon API Gateway 中 REST API 和 HTTP API 的跨域访问配置方式，并特别介绍了开启授权的情况下两种 API 要如何设置才能保证 preflight 请求被正确响应。

This article covered the CORS configuration methods for REST API and HTTP API in Amazon API Gateway, with special attention to how both API types should be configured to ensure preflight requests are properly handled when authorization is enabled.

两种 API 的跨域访问配置方式区别如下：

The differences between the two API types' CORS configurations are as follows:

| API 类型 / Type | 跨域配置方法 / CORS Configuration Method | 配置特点 / Configuration Features | 授权注意事项 / Authorization Notes |
|---|---|---|---|
| REST API | 可以为特定路由配置跨域，在该路由下点击启用 CORS / Configure CORS for specific routes by clicking Enable CORS | 可以看到 OPTIONS 方法及其响应标头设置 / OPTIONS method and response header settings are visible | 不要为 OPTIONS 方法开启授权 / Do not enable authorization for OPTIONS method |
| HTTP API | 点击左侧导航栏的 CORS 进入配置页面 / Click CORS in the left navigation bar | preflight 请求由 API Gateway 自动响应，控制台中看不到配置 / Preflight handled automatically, not visible in console | 避免使用 ANY 方法，如必须使用则另外创建无授权的 OPTIONS 方法 / Avoid ANY method; if necessary, create an unauthorized OPTIONS method |

## 相关资源 / Related Resources

若要为其他亚马逊云科技的资源开启 CORS，可参考：

For enabling CORS on other AWS resources, refer to:

- [为 CloudFront 开启 CORS / Enable CORS for CloudFront](https://aws.amazon.com/cn/blogs/china/several-solutions-to-cloudfront-cross-domain-problem-cors/)
- [为 Lambda 函数 URL 开启 CORS / Enable CORS for Lambda Function URLs](https://aws.amazon.com/cn/blogs/china/several-solutions-to-cloudfront-cross-domain-problem-cors/)
- [为托管静态网站的 S3 开启 CORS / Enable CORS for S3 Static Website Hosting](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/cors.html)

## 本篇作者 / Authors

- **李方怡** - 亚马逊云科技解决方案架构师，负责基于亚马逊云科技的云计算方案架构的设计和技术咨询，在无服务器领域有丰富经验。/ AWS Solutions Architect, specializing in serverless architecture.
- **张司雨** - 亚马逊云科技解决方案架构师，负责亚马逊云科技云计算方案咨询和设计，在电商行业有丰富的经验。/ AWS Solutions Architect, specializing in e-commerce solutions.
- **苏喆** - 亚马逊云科技解决方案架构师，致力于亚马逊云科技服务在电商、教育以及开发者群体中的推广。/ AWS Solutions Architect, focusing on cloud-native and container architecture.
