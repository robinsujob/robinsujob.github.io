---
slug: "api-gateway-cors-configuration"
title: "API Gateway 跨域访问（CORS）配置指南"
date: 2024-10-28
description: "全面介绍 AWS API Gateway 中 REST API 和 HTTP API 的 CORS 配置方法，以及开启授权时的注意事项。"
categories:
  - AWS
tags:
  - api-gateway
  - cors
  - serverless
---


CORS，全称为跨源资源共享，是一种基于 HTTP 标头的机制，用来声明哪些外部源可以访问服务器资源。它用于在浏览器同源策略的基础上，安全地放开合法的跨域访问。

[Amazon API Gateway](https://aws.amazon.com/cn/api-gateway/) 是一项全托管服务，可帮助开发者轻松创建、发布、维护、监控和保护任意规模的 API。由于它常被用作后端服务的统一入口，因此在 API Gateway 上配置 CORS 是一个非常常见的需求。

本文将介绍如何在 Amazon API Gateway 的 REST API 和 HTTP API 中配置跨域访问，并重点说明两者在 CORS 配置上的差异，以及开启授权后的处理要点。

## CORS 原理

CORS 主要依赖以下几个 HTTP 标头：

- **Origin**：指示请求来源。
- **Access-Control-Allow-Origin**：指定哪些来源可以访问资源。
- **Access-Control-Allow-Methods**：列出允许访问资源的 HTTP 方法。
- **Access-Control-Allow-Headers**：指示允许使用的自定义请求头。
- **Access-Control-Allow-Credentials**：指示是否允许携带 Cookie 等凭据。
- **Access-Control-Max-Age**：指示预检结果可缓存的时长。

按照请求复杂度，CORS 请求通常分为两类：

- **简单请求**：不需要预检。
- **非简单请求**：浏览器会先发送一次 OPTIONS 预检请求，再发送实际请求。

对于非简单请求，完整流程如下：

![CORS 完整请求流程](images/cors-config-1.png)

1. 客户端应用发起请求
2. 浏览器发送预检请求
3. 服务器返回预检响应
4. 浏览器发送实际请求
5. 服务器返回实际响应
6. 客户端接收实际响应

## API Gateway 介绍

Amazon API Gateway 支持多种 API 风格和多种后端集成类型。本文重点关注两种 REST 风格产品：**REST API** 和 **HTTP API**。

### REST API 与 HTTP API 的区别

两者都属于 API Gateway 产品，但在能力和使用方式上有所不同。

#### 功能差异

REST API 的特有能力包括：

- 支持 API 密钥
- 支持每客户端节流
- 支持请求验证
- 可以与 AWS WAF 集成
- 支持私有 API 端点

HTTP API 的设计更加轻量，主要包括：

- 自动部署
- 支持默认 stage

#### 性能与价格

由于 HTTP API 功能更精简，因此通常延迟更低、价格也更低。

## 在 API Gateway 中配置 CORS

### REST API 的 CORS 配置

在 REST API 中，通常需要针对具体资源和方法配置 CORS。以下示例中，在 `/` 资源下创建了一个 POST 方法，并将其集成到 Lambda 后端。

![REST API 资源配置](images/cors-config-2.png)

要为该方法开启跨域访问，可回到资源概览页面，点击 **Enable CORS**。

![启用 CORS 按钮](images/cors-config-3.png)

随后配置允许的方法、标头和来源。为了正确响应预检请求，OPTIONS 方法会默认开启。

![CORS 配置页面](images/cors-config-4.png)

保存后，可以在 POST 方法的集成响应中看到相应的 CORS 标头配置。

![集成响应标头映射](images/cors-config-5.png)

启用 CORS 后，API Gateway 还会自动创建一个 OPTIONS 方法来响应预检请求。该方法使用模拟集成，返回 200 状态码以及预检所需的相关标头。

![OPTIONS 方法配置](images/cors-config-6.png)

在允许的来源上测试跨域 POST 请求时，预检请求和实际请求都会返回正确的 CORS 标头。

![Preflight 请求响应](images/cors-config-7.png)

![实际请求响应](images/cors-config-8.png)

对于非根路径，也可以在创建资源时直接勾选 CORS，这样 API Gateway 会自动在该资源下创建 OPTIONS 方法。

![创建资源时勾选 CORS](images/cors-config-9.png)

需要注意，这种方式自动创建的 OPTIONS 方法默认较为宽松，通常会接受所有来源和所有方法的跨域请求。如果需要更严格的权限控制，需要手动编辑。

![编辑 OPTIONS 方法](images/cors-config-10.png)

即使在创建资源时勾选了 CORS，仍然需要为具体业务方法（例如 POST）继续配置对应的 CORS 标头。

![为具体方法配置 CORS 标头](images/cors-config-11.png)

#### 开启授权时的 CORS 配置

如果 REST API 集成了 Lambda 授权方或 Cognito 授权方，请只在真正需要授权的方法上开启授权。**不要**为 OPTIONS 方法开启授权，否则预检请求会返回 401。

![为 POST 方法开启授权](images/cors-config-12.png)

![如果为 OPTIONS 方法开启授权，preflight 请求会出现错误](images/cors-config-13.png)

![不要为 OPTIONS 方法开启授权](images/cors-config-14.png)

### HTTP API 的 CORS 配置

HTTP API 的 CORS 配置更加简单。只要为 HTTP API 开启了 CORS，API Gateway 就会自动处理浏览器的预检请求，并自动为后端响应补充相关跨域标头。

进入 HTTP API 页面后，在左侧导航栏点击 **CORS**，然后点击右上角的 **Configure**。

![HTTP API CORS 配置入口](images/cors-config-15.png)

接着填写允许的来源、标头和方法。根据需要，还可以配置公开标头、最大缓存时间以及是否允许携带凭据。

![HTTP API CORS 配置页面](images/cors-config-16.png)

保存后，在 HTTP API 的路由页面中看不到显式的 OPTIONS 方法配置。

![HTTP API 路由页面](images/cors-config-17.png)

在 HTTP API 上测试跨域 POST 请求时，可以看到 preflight 的 OPTIONS 请求和实际的 POST 请求都能得到正确响应。

![HTTP API CORS 测试结果](images/cors-config-18.png)

#### 开启授权时的 CORS 配置

HTTP API 支持 Lambda、JWT 和 IAM 授权。大多数情况下，预检请求会由 HTTP API 自动处理，不需要额外配置。唯一需要特别注意的是授权的 **ANY** 路由：这时预检请求可能会落到 ANY 路由上，而不是走 HTTP API 内置的 CORS 逻辑，从而导致 401。

![授权的 ANY 方法](images/cors-config-19.png)

![ANY 方法导致的 401 错误](images/cors-config-20.png)

这种情况下，有两种常见解决方案：

1. **推荐方式**：为实际需要的方法分别创建明确路由，例如只为 POST 创建路由，避免使用 ANY。
2. 在同一路径下额外创建一个无需授权的 OPTIONS 路由，并为其配置任意后端集成，用于专门响应预检请求。

![为特定方法创建路由](images/cors-config-21.png)

![创建无授权的 OPTIONS 路由](images/cors-config-22.png)

## 总结

REST API 和 HTTP API 在 CORS 配置方式上存在明显差异：

| 类型 | 跨域配置方法 | 配置特点 | 授权注意事项 |
|---|---|---|---|
| REST API | 在具体路由上点击 **Enable CORS** | 可以看到 OPTIONS 方法和响应标头配置 | 不要为 OPTIONS 方法开启授权 |
| HTTP API | 在左侧导航栏点击 **CORS** 统一配置 | 预检由系统自动处理，控制台中看不到显式配置 | 避免使用 ANY，必要时额外创建无授权 OPTIONS 路由 |

## 相关资源

- [为 CloudFront 开启 CORS](https://aws.amazon.com/cn/blogs/china/several-solutions-to-cloudfront-cross-domain-problem-cors/)
- [为 Lambda 函数 URL 开启 CORS](https://aws.amazon.com/cn/blogs/china/several-solutions-to-cloudfront-cross-domain-problem-cors/)
- [为托管静态网站的 S3 开启 CORS](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/cors.html)



---

> 原文链接：[Amazon API Gateway 跨域请求（CORS）配置 - 亚马逊AWS官方博客](https://aws.amazon.com/cn/blogs/china/amazon-api-gateway-cross-origin-resource-sharing-configuration/)

