---
slug: "api-gateway-cors-configuration"
title: "API Gateway CORS Configuration Guide"
date: 2024-10-28
description: "Complete guide to configuring CORS for AWS API Gateway."
image: images/cors-flow.png
categories:
  - AWS
tags:
  - api-gateway
  - cors
  - serverless
---

> Original article: [Amazon API Gateway CORS Configuration - AWS Blog](https://aws.amazon.com/cn/blogs/china/amazon-api-gateway-cross-origin-resource-sharing-configuration/)

CORS, or Cross-Origin Resource Sharing, is an HTTP header-based mechanism that allows servers to indicate which external origins can access their resources. It helps browsers safely make cross-origin requests while still protecting users through the same-origin policy.

[Amazon API Gateway](https://aws.amazon.com/cn/api-gateway/) is a fully managed service for creating, publishing, maintaining, monitoring, and securing APIs at any scale. Because API Gateway is commonly used as the front door for backend services, configuring CORS correctly is a frequent requirement.

This article explains how to configure CORS in Amazon API Gateway REST API and HTTP API, including the differences between the two products and the special handling required when authorization is enabled.

## How CORS Works

CORS mainly relies on these HTTP headers:

- **Origin**: Indicates the request origin.
- **Access-Control-Allow-Origin**: Specifies which origins can access the resource.
- **Access-Control-Allow-Methods**: Lists the HTTP methods allowed to access the resource.
- **Access-Control-Allow-Headers**: Indicates which custom request headers are allowed.
- **Access-Control-Allow-Credentials**: Indicates whether credentials such as cookies are allowed.
- **Access-Control-Max-Age**: Indicates how long preflight results can be cached.

CORS requests are usually divided into two categories:

- **Simple requests**: No preflight is needed.
- **Non-simple requests**: A browser sends an OPTIONS preflight request before the actual request.

For non-simple requests, the flow is as follows:

![Complete CORS Request Flow](images/cors-config-1.png)

1. Client application initiates the request
2. Browser sends a preflight request
3. Server returns a preflight response
4. Browser sends the actual request
5. Server returns the actual response
6. Client receives the actual response

## Introduction to API Gateway

Amazon API Gateway supports multiple API styles and backend integration types. In this article we focus on two RESTful products: **REST API** and **HTTP API**.

### REST API vs HTTP API

Both are API Gateway products, but they differ in capability and operating model.

#### Features

REST API unique features include:

- API key support
- Per-client throttling
- Request validation
- AWS WAF integration
- Private API endpoints

HTTP API is designed with a more minimal feature set:

- Automatic deployment
- Default stage support

#### Performance and Pricing

Because HTTP API is more streamlined, it generally offers lower latency and lower cost.

## Configuring CORS in API Gateway

### REST API CORS Configuration

In a REST API, you usually configure CORS on specific resources and methods. In this example, a POST method under `/` is integrated with Lambda.

![REST API Resource Configuration](images/cors-config-2.png)

To enable CORS for that method, go back to the resource overview page and click **Enable CORS**.

![Enable CORS Button](images/cors-config-3.png)

Then configure allowed methods, headers, and origins. OPTIONS is enabled by default so API Gateway can answer preflight requests.

![CORS Configuration Page](images/cors-config-4.png)

After saving, the POST method integration response shows the configured CORS headers.

![Integration Response Header Mapping](images/cors-config-5.png)

API Gateway also creates an OPTIONS method automatically. It uses mock integration to return a 200 response together with the required preflight headers.

![OPTIONS Method Configuration](images/cors-config-6.png)

When tested from an allowed origin, both the preflight request and the actual request return the expected CORS headers.

![Preflight Request Response](images/cors-config-7.png)

![Actual Request Response](images/cors-config-8.png)

For non-root paths, you can also check CORS when creating the resource so that API Gateway creates the OPTIONS method for you.

![Check CORS When Creating Resource](images/cors-config-9.png)

That automatically created OPTIONS method is permissive by default. If you need tighter access control, edit it manually.

![Edit OPTIONS Method](images/cors-config-10.png)

Even if you check CORS while creating the resource, you still need to configure the specific business methods, such as POST.

![Configure CORS Headers for Specific Methods](images/cors-config-11.png)

#### CORS Configuration with Authorization

If your REST API uses Lambda authorizers or Cognito authorizers, enable authorization only on the methods that require it. Do **not** enable authorization on the OPTIONS method, otherwise preflight requests will fail with 401.

![Enable Authorization for POST Method](images/cors-config-12.png)

![OPTIONS Authorization Error](images/cors-config-13.png)

![Do Not Authorize OPTIONS](images/cors-config-14.png)

### HTTP API CORS Configuration

HTTP API CORS configuration is simpler. Once CORS is enabled, API Gateway automatically handles browser preflight requests and adds the necessary CORS headers to backend responses.

Go to the HTTP API page, click **CORS** in the left navigation bar, and then click **Configure**.

![HTTP API CORS Configuration Entry](images/cors-config-15.png)

Enter the allowed origins, headers, and methods. You can also optionally configure exposed headers, max age, and credentials.

![HTTP API CORS Configuration Page](images/cors-config-16.png)

After saving, you will not see an OPTIONS route configuration in the console.

![HTTP API Routes Page](images/cors-config-17.png)

Testing a cross-origin POST request confirms that both the preflight OPTIONS request and the actual request are handled correctly.

![HTTP API CORS Test Results](images/cors-config-18.png)

#### CORS Configuration with Authorization

HTTP API supports Lambda, JWT, and IAM authorization. In most cases, preflight requests are handled automatically. The main exception is an authorized **ANY** route. In that case, the preflight request may be handled by the ANY route instead of the built-in CORS logic, causing a 401 response.

![Authorized ANY Method](images/cors-config-19.png)

![ANY Method 401 Error](images/cors-config-20.png)

There are two practical solutions:

1. **Recommended**: Create explicit routes for the methods you need, such as POST, instead of using ANY.
2. Create an unauthorized OPTIONS route on the same path and attach any backend integration so it can answer preflight requests.

![Create Route for Specific Method](images/cors-config-21.png)

![Create Unauthorized OPTIONS Route](images/cors-config-22.png)

## Summary

REST API and HTTP API support CORS in different ways:

| Type | CORS Configuration Method | Configuration Features | Authorization Notes |
|---|---|---|---|
| REST API | Configure CORS on specific routes with **Enable CORS** | OPTIONS method and headers are visible in the console | Do not enable authorization for OPTIONS |
| HTTP API | Configure CORS from the left-side **CORS** page | Preflight handling is automatic and hidden | Avoid ANY, or add an unauthorized OPTIONS route |

## Related Resources

- [Enable CORS for CloudFront](https://aws.amazon.com/cn/blogs/china/several-solutions-to-cloudfront-cross-domain-problem-cors/)
- [Enable CORS for Lambda Function URLs](https://aws.amazon.com/cn/blogs/china/several-solutions-to-cloudfront-cross-domain-problem-cors/)
- [Enable CORS for S3 Static Website Hosting](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/cors.html)

## Authors

- **Fangyi Li** - AWS Solutions Architect, specializing in serverless architecture.
- **Siyu Zhang** - AWS Solutions Architect, specializing in e-commerce solutions.
- **Zhe Su** - AWS Solutions Architect, focusing on cloud-native and container architecture.
