---
slug: "china-cloudfront-ssl-plugin-v2"
title: "China CloudFront SSL Plugin V2 - One-Stop Free SSL Certificate Management"
date: 2025-08-19
description: "A comprehensive SSL certificate management solution for China region CloudFront distributions."
image: images/architecture.png
categories:
  - AWS
tags:
  - cloudfront
  - ssl
  - serverless
  - china
---


In today's digital age, website security is paramount. In 2023, we released China CloudFront SSL Plugin for free SSL integration with CloudFront in China region. Now we're pleased to announce V2.

## Core Upgrades

V2 introduces three core upgrades making certificate management simpler, safer, and more efficient.

### 1. Multi-Project Management

- **V1**: Each stack managed one project only
- **V2**: Single stack manages multiple projects

### 2. Graphical Interface

- **V1**: Manual API request construction via Swagger UI
- **V2**: Intuitive GUI with button clicks

### 3. Security Auth

- **V1**: No API security validation
- **V2**: Access Key authentication required

### Retained Features

While bringing new features, we retained the most popular characteristics:

✓ **Cost** — Serverless, pay-per-use, auto-renewal every 30 days

✓ **Automation** — Seamless CloudFront integration, auto certificate replacement, EventBridge scheduling

✓ **Transparency** — Email notifications, graphical dashboard, multi-project monitoring

✓ **Open Source** — All code open source, supports customization

## Architecture

Built on serverless architecture with one-click CloudFormation deployment.

![Architecture](images/architecture.png)

**Core Components**: Let's Encrypt + Certbot + Lambda + API Gateway

**Storage**: DynamoDB (status) + S3 (backup) + IAM SSL (CloudFront association)

**Automation**: SNS (notifications) + EventBridge (scheduled renewal, default 30 days)

## Deployment Demo

### Create Stack

Deploy the main stack via CloudFormation template in 3-5 minutes with a stack name and Access Key.

![Create Stack](images/new-stack.gif)

### Create Certificate Project

Create certificate projects in the GUI for domain sets. Supports multiple domains, configurable email and renewal intervals (30 days recommended). System auto-deploys sub-stacks.

![Create Project](images/create-project.gif)

### Attach to CloudFront

Certificates auto-upload to IAM SSL storage. Select in CloudFront console. Subsequent renewals replace seamlessly without manual intervention.

![Attach SSL](images/attach-ssl.gif)

### Update Project

Update domain lists and intervals anytime; each change triggers re-issuance. Auto-handles certificate updates and cleanup.

![Update Project](images/update-project.gif)

### Re-issue Certificate

Manual certificate update control for fault recovery, emergency updates, or testing. Re-executes the full certificate lifecycle.

![Re-issue](images/recert.gif)

- Deploy: [One-click Deploy V2](https://console.amazonaws.cn/cloudformation/home?#/stacks/create/template?templateURL=https://aws-cn-getting-started.s3.cn-northwest-1.amazonaws.com.cn/china-cloudfront-ssl-plugin_v2/ChinaCloudFrontSslPluginStackV2.template.json)
- Tutorial: [V2 Tutorial](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/)

## Summary

V2 delivers a more convenient certificate solution through multi-project architecture, graphical UI, and enhanced security.

## Resources

- [V2 Tutorial](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/)
- [GitHub V2](https://github.com/aws-samples/sample-China-CloudFront-SSL-Plugin-V2)
- [GitHub V1](https://github.com/aws-samples/China-CloudFront-SSL-Plugin)
- [CloudFront China Differences](https://docs.amazonaws.cn/aws/latest/userguide/cloudfront.html#feature-diff)
- [IAM SSL Certificate Management](https://docs.amazonaws.cn/IAM/latest/UserGuide/id_credentials_server-certs.html)
- [Let's Encrypt Docs](https://letsencrypt.org/docs/)
- [Certbot Docs](https://certbot.eff.org/pages/about)
- [Contact Us](mailto:china-cloudfront-ssl-plugin@amazon.com)

---

Original: [AWS Blog](https://aws.amazon.com/cn/blogs/china/china-cloudfront-ssl-plugin-v2-a-one-stop-certificate-solution-for-cloudfront-in-china-region/) | [GitHub](https://github.com/aws-samples/sample-China-CloudFront-SSL-Plugin-V2)

