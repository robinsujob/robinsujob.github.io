
---
slug: "cloudfront-ssl-plugin-deployment-guide"
title: "China CloudFront SSL Plugin Deployment Guide"
date: 2023-11-15
description: "Deployment guide for the China CloudFront SSL Plugin - free SSL certificate automation."
image: images/architecture.png
categories:
  - AWS
tags:
  - cloudfront
  - ssl
  - deployment
---

> **Original Post:** [Divert Website Access Traffic from EC2 to Amazon CloudFront](https://aws.amazon.com/cn/blogs/china/divert-website-access-traffic-from-ec2-to-amazon-cloudfront/)
>
> **GitHub:** [aws-samples/China-CloudFront-SSL-Plugin](https://github.com/aws-samples/China-CloudFront-SSL-Plugin)

This article applies to AWS China Region services. You will learn how to use Amazon CloudFront in the China Region to accelerate and distribute traffic from websites deployed on EC2, and use the [China CloudFront SSL Plugin](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/) to deploy free SSL certificates to protect your site. The plugin helps you generate, renew, and download free SSL certificates in the AWS China Regions, with Amazon CloudFront integration and automatic certificate renewal. You can also refer to the EC2-CloudFront integration section for configuring CloudFront to distribute EC2 website traffic in AWS Global Regions.

## Why Choose Amazon CloudFront?

Amazon CloudFront is a Content Delivery Network (CDN) service provided by AWS. Using a CDN reduces website load times, lowers bounce rates, and increases traffic and revenue, while also reducing the load on origin servers, improving website stability and security. Amazon CloudFront securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds in a developer-friendly environment, and integrates seamlessly with Amazon S3, Elastic Load Balancer, Amazon EC2, and more.

Amazon CloudFront not only accelerates your website and reduces origin server load, but also lowers the data transfer costs for traffic leaving your AWS-hosted website to the internet. For example, compared to EC2's outbound data transfer costs, using Amazon CloudFront in the AWS China Regions can help you reduce outbound data transfer costs by at least 67%. For specific pricing, refer to [EC2 Data Transfer Pricing](https://www.amazonaws.cn/ec2/pricing/#Amazon_EC2_.E6.95.B0.E6.8D.AE.E4.BC.A0.E8.BE.93) and [CloudFront Data Transfer Pricing](https://www.amazonaws.cn/cloudfront/pricing/#On-demand_Pricing).

## Considerations for Using CloudFront in China Regions

- **ICP Filing and Domain Registration:** According to relevant regulations, websites hosted in mainland China require ICP filing. Domains without ICP filing cannot serve web content. Please refer to the AWS China [ICP Filing Support Documentation](https://www.amazonaws.cn/support/icp/) for more details.

- **CloudFront Provided Domain:** CloudFront automatically assigns a `*.cloudfront.cn` domain. However, due to ICP requirements, you cannot directly use this domain for website services in China. You must add an ICP-filed domain as an alternate domain name (CNAME).

- **SSL/TLS Certificate Integration:** Amazon CloudFront in the China Regions does not currently support [Amazon Certificate Manager](https://www.amazonaws.cn/certificate-manager/features/). You can obtain SSL/TLS certificates from third-party CAs or use the [China CloudFront SSL Plugin](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/) for free certificates.

- **Feature Differences Between China and Global Regions:** Amazon CloudFront in China Regions does not currently support Lambda@Edge, Amazon WAF, etc. See the [documentation](https://docs.amazonaws.cn/aws/latest/userguide/cloudfront.html#feature-diff) for details.

## Prerequisites

To complete all sections of this article and get a consistent experience with AWS services, please ensure you meet the following prerequisites.

- Your AWS China Region account has completed ICP filing, with ports 80/443 open
- You have an ICP-filed domain
- Use [Amazon Route 53](https://www.amazonaws.cn/route53/) as your DNS service. If you haven't migrated yet, see the [reference documentation](https://www.amazonaws.cn/getting-started/tutorials/migrate-domain-to-amazon-route53/)

## Integrating EC2 with CloudFront

In the following sections, you will launch an EC2 instance, set up a web server, integrate EC2 with CloudFront, and deploy a free SSL certificate using the China CloudFront SSL Plugin.

You will also learn some tips, such as using Elastic IP to fix your EC2 public DNS hostname for CloudFront origins, or using AWS-managed prefix lists to enhance EC2 security.

The deployment architecture is shown below:

![Deployment Architecture](images/architecture.png)

### Create EC2 and Install Web Server

In this section, you will create an EC2 instance with a web server, then bind an Elastic IP to fix the public DNS hostname.

#### Step 1: Launch EC2 Instance

Launch an EC2 instance from the EC2 console.

![Launch EC2 Instance](images/ec2-create.jpg)

Name your instance, e.g., "web-server".

You can keep the default AMI and instance type.

- AMI: Amazon Linux 2023
- Instance type: micro

![AMI and Instance Type](images/cloudfront-ssl-2.jpg)

Select an existing key pair or create a new one for SSH access.

![Key Pair Settings](images/cloudfront-ssl-3.jpg)

For network settings, ensure the EC2 instance is in a public subnet and check "Allow HTTP traffic from the internet" to make port 80 accessible.

![Network Configuration](images/cloudfront-ssl-4.jpg)

Expand the "Advanced details" section at the bottom:

![Advanced Details](images/cloudfront-ssl-5.jpg)

Paste the following user data script to install a web server on first boot, then click "Launch instance".

```bash
#!/bin/bash
yum install -y httpd
systemctl enable httpd
systemctl start httpd
```

![User Data](images/cloudfront-ssl-6.jpg)

#### Step 2: Create Elastic IP and Associate with EC2

[Elastic IP](https://docs.amazonaws.cn/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) is a static IPv4 address designed for cloud computing. It ensures your EC2 instance's public IP address and DNS hostname remain unchanged. In this section, you'll learn how to associate an Elastic IP with your EC2 instance and access your site using the public DNS hostname.

Find Elastic IP under "Network & Security" in the EC2 console left menu.

![Elastic IP Menu](images/cloudfront-ssl-7.jpg)

Click "Allocate Elastic IP address" then "Allocate" to obtain an Elastic IP.

![Allocate Elastic IP](images/cloudfront-ssl-8.jpg)

Select your Elastic IP, click "Actions", and choose "Associate Elastic IP address".

![Associate Elastic IP](images/cloudfront-ssl-9.jpg)

Select your previously created EC2 instance and click "Associate" to ensure the public IP address remains stable.

![Select EC2 Instance](images/cloudfront-ssl-10.jpg)

Return to the instance list, select your instance, and copy the public IPv4 DNS.

![Copy Public DNS](images/cloudfront-ssl-11.jpg)

Access the public DNS hostname in your browser to verify the web server is installed. You'll see the site is using port 80 without SSL/TLS.

![Browser Verification](images/cloudfront-ssl-12.jpg)

In the following sections, you'll use this hostname as the CloudFront origin to divert website traffic from EC2 to Amazon CloudFront.

### Create CloudFront Distribution

In this section, you will create a CloudFront distribution and associate it with your EC2 instance to accelerate content delivery.

#### Step 1: Create CloudFront Distribution

Next, you'll quickly set up a CloudFront distribution. Go to the CloudFront console and create a distribution:

![Create CloudFront Distribution](images/cloudfront-ssl-13.jpg)

On the CloudFront configuration page, you'll see the basic configuration elements:

- **Origin** – The origin server, supporting S3, EC2, ELB, API Gateway, and third-party origins
- **Cache Behavior** – Define caching behavior through path matching, enable compression, allowed methods, access control, etc.
- **Settings** – Alternate domain names (CNAME), SSL certificate, default root object, logging, etc.

For the origin, use the EC2 public DNS (with Elastic IP) as the origin domain. Ensure the origin protocol is HTTP.

![Origin Settings](images/cloudfront-ssl-14.jpg)

Keep the default cache behavior settings:

![Cache Behavior Settings](images/cloudfront-ssl-15.jpg)

> **Note:** Due to compliance requirements, the default CloudFront domain in Beijing/Ningxia regions cannot be accessed directly. You must complete ICP filing and set up CNAME DNS resolution.

In the settings section, enter your ICP-filed domain as the alternate domain name (CNAME):

![Alternate Domain Name Settings](images/cloudfront-ssl-16.jpg)

After creation, wait for deployment. Once complete, check your alternate domain name — if ICP-filed, you should see a "green checkmark".

![ICP Filing Green Checkmark](images/cloudfront-ssl-17.jpg)

After deployment, go to Route 53 (or your DNS provider) to update DNS records. Create a new record in the hosted zone.

![Route 53 Create Record](images/cloudfront-ssl-18.jpg)

Fill in the DNS record:

![DNS Record Configuration](images/cloudfront-ssl-19.jpg)

After DNS update, access your ICP-filed domain in the browser:

![Browser Access Domain](images/cloudfront-ssl-20.jpg)

> **Note:** If you get a 502 error, check whether EC2 has an SSL certificate installed or if the origin port is correct. See [documentation](https://docs.amazonaws.cn/AmazonCloudFront/latest/DeveloperGuide/http-502-bad-gateway.html). For 403 errors, ensure you're using the ICP-filed domain.

#### Step 2: Enhance EC2 and Website Security

In this section, you'll use [AWS-managed prefix lists](https://docs.amazonaws.cn/vpc/latest/userguide/working-with-aws-managed-prefix-lists.html#available-aws-managed-prefix-lists) to enhance EC2 security. You can use the CloudFront managed prefix list to restrict inbound HTTP/HTTPS traffic to CloudFront origin-facing IP addresses only.

Edit the security group inbound rules: add an HTTP rule with `com.amazonaws.global.cloudfront.origin-facing` prefix list as the source, and remove the existing `0.0.0.0/0` rule.

![Security Group Prefix List Configuration](images/cloudfront-ssl-21.jpg)

You can also associate SSL/TLS certificates with CloudFront to enhance website security. In the following section, you'll deploy free SSL certificates using the China CloudFront SSL Plugin.

## Deploy Free SSL Certificates with China CloudFront SSL Plugin

Before starting, confirm you're using Amazon Route 53 for DNS. This section covers deployment only. For more details, see the [China CloudFront SSL Plugin](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/?nc1=h_ls).

### 1. Initialize Deployment

Deploy via CloudFormation. Click the [link](https://console.amazonaws.cn/cloudformation/home?#/stacks/create/template?templateURL=https://aws-cn-getting-started.s3.cn-northwest-1.amazonaws.com.cn/china-cloudfront-ssl-plugin/ChinaCloudFrontSslPluginStack.json) to launch the stack in the CloudFormation console.

![CloudFormation Deployment](images/cloudfront-ssl-22.jpg)

### 2. Enter Deployment Parameters

Specify stack details with the following parameters:

- **Stack Name:** Name your stack
- **Email:** Enter your email for SNS notifications (one email only)
- **Domain Name:** Enter domain names for the SSL certificate. Supports wildcard and multiple domains (comma-separated)
- **SSL Renew Interval Days:** Enter the renewal interval. Let's Encrypt certificates are valid for 90 days; enter 1-89. Default: 80 days.

![Stack Parameters](images/cloudfront-ssl-23.jpg)

### 3. Confirm Deployment

Confirm deployment details, check the acknowledgment box at the bottom, and click **Submit**.

![Confirm Deployment](images/cloudfront-ssl-24.jpg)

After submission, you'll see resources being created in the stack events tab. Wait about 3 minutes.

### 4. Subscribe to SNS Notifications

During deployment, check your email for an SNS subscription confirmation from no-reply@sns.amazonaws.com. Click the confirmation link promptly.

![SNS Subscription Email](images/cloudfront-ssl-25.jpg)

Successful subscription confirmation:

![Subscription Successful](images/cloudfront-ssl-26.jpg)

### 5. Check Stack Deployment Progress

When the stack status turns to green `CREATE_COMPLETE`, the deployment is finished.

Check the "Outputs" tab for quick links:

- **CloudfrontConsole:** Access the CloudFront console to bind the issued certificate
- **ManagementWebURL:** Access SwaggerUI to view or delete existing SSL certificates in IAM
- **S3BucketURL:** Access the S3 console to download issued SSL certificates

![Stack Outputs](images/cloudfront-ssl-27.jpg)

### 6. Bind SSL Certificate in the Amazon CloudFront Console

After stack deployment, an SSL certificate is automatically requested for your domain. If subscribed to SNS, you'll receive an email confirming certificate issuance. The certificate name consists of the stack name and expiry time, e.g., `Certbot-2023-11-14-1540`.

![SSL Certificate Email Notification](images/cloudfront-ssl-28.jpg)

Open the CloudFront console, select your distribution, and find the option to edit alternate domain names and SSL certificate.

![CloudFront Edit Settings](images/cloudfront-ssl-29.jpg)

Select the corresponding SSL certificate from the custom SSL certificate dropdown, then save changes.

![Select SSL Certificate](images/cloudfront-ssl-30.jpg)

After deployment, you can access your CloudFront-accelerated site via HTTPS and verify the Let's Encrypt SSL certificate, valid for 90 days.

![HTTPS Access Verification](images/cloudfront-ssl-31.jpg)

For more information on using the China CloudFront SSL Plugin, see the [plugin documentation](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/?nc1=h_ls).

## Summary

Through this article, you've learned the basics of Amazon CloudFront and how to divert EC2 website traffic to CloudFront for acceleration and cost savings. You've also learned to use AWS-managed prefix lists to restrict EC2 traffic to CloudFront only, and to deploy free SSL certificates using the China CloudFront SSL Plugin to protect your site with HTTPS.

## References

- [China CloudFront SSL Plugin](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/?nc1=h_ls)
- [Amazon CloudFront Introduction](https://docs.amazonaws.cn/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
- [Amazon CloudFront China Region Differences](https://docs.amazonaws.cn/aws/latest/userguide/cloudfront.html#feature-diff)
- [Network Acceleration with Amazon CloudFront in China](https://www.amazonaws.cn/getting-started/use-cases/cloudfront-network-acceleration/?nc1=h_ls)
