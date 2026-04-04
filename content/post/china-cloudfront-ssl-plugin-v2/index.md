---
slug: "china-cloudfront-ssl-plugin-v2"
title: "China CloudFront SSL Plugin V2 - One-Stop Free SSL Certificate Management"
date: 2025-08-19
description: "A comprehensive SSL certificate management solution for China region CloudFront distributions."
image: images/architecture-v2.png
categories:
  - AWS
tags:
  - CloudFront
  - SSL
  - Serverless
  - China
---

In today's digital age, website security is paramount. SSL certificates, as a critical tool for protecting data transmission, have always been a key concern for developers and operations teams. In 2023, we released the China CloudFront SSL Plugin to facilitate the integration of free SSL certificates with CloudFront in the China region. We have continued to iterate on our solution. Now, we are pleased to announce the official release of the second generation of the China CloudFront SSL Plugin.

### Major Upgrades

China CloudFront SSL Plugin V2 introduces three core upgrades, making certificate management simpler, safer, and more efficient.

#### 1. Breaking Through the Single-Project Limitation with Unified Multi-Project Management

In this new version, we have completely restructured the project management architecture:

- **Before (V1)**: Each stack could only manage a single project's domain set. Managing multiple projects required deploying multiple stacks.

- **After (V2)**: A single stack can now manage domain sets for multiple projects, significantly simplifying operations.

#### 2. A Brand-New Interactive Experience — No More Complex Operations

To improve the user experience, we have completely redesigned the management interface:

- **Before (V1)**: An API management page built on Swagger UI that required manually constructing and sending API requests.

- **After (V2)**: An intuitive graphical user interface where all operations can be completed with simple button clicks, greatly lowering the barrier to entry.

#### 3. Enhanced Security Mechanisms for Safer Operations

Security has been comprehensively strengthened:

- **Before (V1)**: External APIs lacked effective security validation mechanisms.

- **After (V2)**: An Access Key verification mechanism has been introduced — all API operations now require authentication, ensuring secure and controlled access.

While introducing these new capabilities, we have preserved and reinforced the most popular features of the solution:

✓ **Cost Advantage**

- Fully serverless architecture with pay-per-invocation pricing
- Certificate renewal triggers every 30 days by default
- Only minimal storage and logging costs

✓ **Operational Automation**

- Seamless integration with CloudFront
- Automatic replacement of associated CloudFront certificates after renewal
- Scheduled automatic renewal via Amazon EventBridge

✓ **Operational Transparency**

- Comprehensive email notification mechanism covering the entire certificate lifecycle
- Intuitive graphical dashboard for real-time certificate status monitoring
- Unified multi-project management and monitoring

✓ **Open Source**

- All code is provided as open source
- Supports customization on top of the source code
- Easy to extend for enterprise-specific requirements

These upgrades not only enhance the user experience but also provide more powerful support for China CloudFront certificate management. Whether managing certificates for a single website or multiple projects, V2 can handle it with ease.

## Architecture

As a certificate management solution for CloudFront in the China region, we designed a complete architecture based on serverless services, with automated deployment via Amazon CloudFormation templates.

![Architecture](images/architecture-v2.png)

**1. Core Components:**

- **Let's Encrypt**: A free, open, and automated certificate authority that provides free SSL certificate support for the solution
- **Certbot**: A free open-source tool for automated certificate acquisition, deployment, and renewal
- **Amazon Lambda**: The core compute component responsible for running the certificate issuance program, frontend interface, and certificate management API
- **Amazon API Gateway**: Provides a secure certificate management API interface — all operations require Access Key verification

**2. Storage & Database:**

- **Amazon DynamoDB**: A serverless database dedicated to storing project certificate issuance status and error information
- **Amazon S3**: Used for storing backup SSL certificates, supporting certificate download and backup management
- **IAM SSL Certificate Storage**: Dedicated storage for SSL certificates associated with CloudFront — a special requirement for the China region

**3. Automation & Notifications:**

- **Amazon SNS**: Sends email notifications about certificate issuance status, ensuring operations teams are promptly informed
- **Amazon EventBridge**: Triggers certificate renewal on a schedule, defaulting to automatic renewal every 30 days

## Deployment Demo

#### Create Management Stack

Creating the management stack is the first step in deploying China CloudFront SSL Plugin V2. Using an Amazon CloudFormation template, you can deploy the main stack — including Lambda functions, API Gateway, DynamoDB, and other core components — with a single click. During deployment, you need to specify a stack name and an Access Key as the API Gateway security key, ensuring only authorized users can access the certificate management features. The entire deployment process takes approximately 3–5 minutes, after which you will receive an access link to the certificate management frontend.

![Create Stack](images/new-stack.gif)

#### Create Certificate Project

Creating a certificate project is the core step in using China CloudFront SSL Plugin V2. In the graphical management interface, you can easily create new certificate projects to request free Let's Encrypt SSL certificates for specified domain sets. Each project supports multiple domains (comma-separated), and you can configure the notification email address and automatic renewal interval (30 days recommended). Once a project is created, the system automatically deploys a dedicated sub-stack containing a certificate issuance Lambda function and an EventBridge scheduling rule for automated certificate management.

![Create Project](images/create-project.gif)

#### Attach the Auto-Issued Certificate to CloudFront

Attaching the auto-issued certificate to CloudFront is the key step for enabling HTTPS access. After a certificate is successfully issued, the system automatically uploads it to IAM SSL certificate storage. You can then find and select the corresponding certificate in the CloudFront console's distribution settings. Under "Alternate Domain Names and SSL Certificate," enter the domain name for which you requested the certificate, then select the corresponding certificate from the custom SSL certificate dropdown to complete the binding. Once bound, subsequent automatic certificate renewals will seamlessly replace the certificate in CloudFront without any manual intervention.

![Attach SSL](images/attach-ssl.gif)

#### Update Certificate Project (Domains / Auto-Renewal Interval)

The update certificate project feature allows you to flexibly adjust project configurations to adapt to business changes. By selecting a project and clicking the "Modify Project" button, you can update the domain list and adjust the SSL certificate auto-renewal interval. Each project modification triggers a new certificate issuance, ensuring configuration changes take effect immediately. The system automatically handles CloudFront certificate updates and old certificate cleanup — the entire process is transparent to the user and reliably secure.

![Update Project](images/update-project.gif)

#### Re-issue Certificate / Force Certificate Update

The re-issue certificate feature gives you manual control over certificate updates. When certificate issuance fails or you need an immediate certificate update, you can select the corresponding certificate from the certificate list and click the "Re-issue" button to manually trigger the certificate update process. The system re-executes the full certificate request, validation, issuance, and CloudFront update workflow, and notifies you of the result via email. This feature is particularly useful for fault recovery, emergency updates, or testing scenarios, ensuring your SSL certificates are always up to date.

![Re-issue](images/recert.gif)

To experience the full feature set, please refer to our solution page for deployment.

Deploy: [One-Click Deploy China CloudFront SSL Plugin V2](https://console.amazonaws.cn/cloudformation/home?#/stacks/create/template?templateURL=https://aws-cn-getting-started.s3.cn-northwest-1.amazonaws.com.cn/china-cloudfront-ssl-plugin_v2/ChinaCloudFrontSslPluginStackV2.template.json)

Tutorial: [China CloudFront SSL Plugin V2 Full Tutorial](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/)

## Summary

China CloudFront SSL Plugin V2 delivers a more convenient and comprehensive certificate solution for CloudFront users in the China region through its brand-new multi-project management architecture, intuitive graphical interface, and enhanced security mechanisms.

## Resources and Documentation

### Tutorials & Deployment

- [China CloudFront SSL Plugin V2 Full Tutorial](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/)

  Detailed deployment and usage guide with complete step-by-step instructions and troubleshooting

- [One-Click Deploy V2](https://console.amazonaws.cn/cloudformation/home?#/stacks/create/template?templateURL=https://aws-cn-getting-started.s3.cn-northwest-1.amazonaws.com.cn/china-cloudfront-ssl-plugin_v2/ChinaCloudFrontSslPluginStackV2.template.json)

  Deploy the latest version directly via CloudFormation template

### Open Source Repositories

- [China CloudFront SSL Plugin V2](https://github.com/aws-samples/sample-China-CloudFront-SSL-Plugin-V2)

  Complete V2 source code, supporting custom development and contributions

- [China CloudFront SSL Plugin V1](https://github.com/aws-samples/China-CloudFront-SSL-Plugin)

  First-generation source code for comparison and reference

- [Email the Solution Team](mailto:china-cloudfront-ssl-plugin@amazon.com)

  Contact the China CloudFront SSL Plugin solution team directly for professional support

- [ICP Filing Guide](https://www.amazonaws.cn/support/icp/)

  Required ICP filing process for website deployment in the China region

### Related AWS Service Documentation

- [Amazon CloudFront China Region Feature Differences](https://docs.amazonaws.cn/aws/latest/userguide/cloudfront.html#feature-diff)

  Understand the special requirements and limitations of CloudFront in the China region

- [IAM SSL Certificate Management](https://docs.amazonaws.cn/IAM/latest/UserGuide/id_credentials_server-certs.html)

  Official documentation for China region CloudFront SSL certificate storage

- [Amazon Route 53 Domain Migration](https://www.amazonaws.cn/getting-started/tutorials/migrate-domain-to-amazon-route53/)

  Detailed steps for migrating domain resolution to Route 53

- [Amazon CloudFront Deployment Guide](https://aws.amazon.com/cn/blogs/china/divert-website-access-traffic-from-ec2-to-amazon-cloudfront/)

  CloudFront Deployment Mini-Guide — Deploying Free Certificates with China Region CloudFront and SSL Plugin

### Other Technical References

- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

  Learn about how the Let's Encrypt certificate authority works and its limitations

- [Certbot Documentation](https://certbot.eff.org/pages/about)

  Detailed usage instructions for the Certbot tool

- [Amazon Route 53 DNS Validation](https://certbot-dns-route53.readthedocs.io/en/stable/)

  Technical documentation for the Route 53 DNS validation plugin

### Contact Us

- [Contact AWS Technical Support](https://webchat-aws.clink.cn/chat.html?accessId=35d2504b-57b6-4093-97fd-81a6198bbbfa&language=zh_CN)

  Get official professional technical support and answers

- [Email the Solution Team](mailto:china-cloudfront-ssl-plugin@amazon.com)

  Contact the China CloudFront SSL Plugin solution team directly for professional support

---

> Original: [AWS Blog](https://aws.amazon.com/cn/blogs/china/china-cloudfront-ssl-plugin-v2-a-one-stop-certificate-solution-for-cloudfront-in-china-region/) | [GitHub](https://github.com/aws-samples/sample-China-CloudFront-SSL-Plugin-V2)
