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

This article applies to AWS China Region services. You will learn how to use Amazon CloudFront in the China Region to accelerate and distribute traffic from websites deployed on EC2, and use the [China CloudFront SSL Plugin](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/) to deploy free SSL certificates to protect your site. The plugin helps you generate, renew, and download free SSL certificates in the AWS China Regions, with Amazon CloudFront integration and automatic certificate renewal. You can also refer to the EC2-CloudFront integration section for configuring CloudFront to distribute EC2 website traffic in AWS Global Regions.

## Why Choose Amazon CloudFront?

Amazon CloudFront is a Content Delivery Network (CDN) service provided by AWS. Using a CDN reduces website load times, lowers bounce rates, and increases traffic and revenue, while also reducing the load on origin servers, improving website stability, security, availability, and reliability. Amazon CloudFront securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds in a developer-friendly environment, and integrates seamlessly with Amazon S3, Elastic Load Balancer, Amazon EC2, and more.

Amazon CloudFront not only accelerates your website and reduces origin server load, but also lowers the data transfer costs for traffic leaving your AWS-hosted website to the internet. For example, compared to EC2's outbound data transfer costs, using Amazon CloudFront in the AWS China Regions can help you reduce outbound data transfer costs by at least 67%. For specific pricing, refer to the AWS China Region official website [EC2 Data Transfer Pricing](https://www.amazonaws.cn/ec2/pricing/#Amazon_EC2_.E6.95.B0.E6.8D.AE.E4.BC.A0.E8.BE.93) and [CloudFront Data Transfer Pricing](https://www.amazonaws.cn/cloudfront/pricing/#On-demand_Pricing).

## Considerations for Using CloudFront in China Regions

- **ICP Filing and Domain Registration:** According to relevant laws and regulations, if you need to host a website in mainland China, you must first complete ICP filing. Domains without ICP filing cannot serve web content. Please prepare an ICP-filed domain. Refer to the AWS China [ICP Filing Support Documentation](https://www.amazonaws.cn/support/icp/) for more details on obtaining the required ICP filing for your domain.

- **CloudFront Provided Domain:** CloudFront automatically assigns a `*.cloudfront.cn` domain. However, due to ICP filing requirements, you cannot directly use this domain for website services in China. You must add an ICP-filed domain as an alternate domain name (also known as CNAME) to your CloudFront distribution, and then use the alternate domain name to access your website.

- **CloudFront SSL/TLS Certificate Integration:** Amazon CloudFront in the China Regions does not currently support [Amazon Certificate Manager](https://www.amazonaws.cn/certificate-manager/features/). If you need to use SSL/TLS certificates with CloudFront, you can obtain them from third-party certificate authorities and [import SSL/TLS certificates](https://docs.amazonaws.cn/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-procedures.html#cnames-and-https-uploading-certificates). You can also use the [China CloudFront SSL Plugin](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/) to obtain free SSL/TLS certificates, which will be covered in detail in the "Deploy Free Certificates with China CloudFront SSL Plugin" section of this article.

- **Feature Differences Between China and Global Regions:** Amazon CloudFront in the China Regions does not currently support Lambda@Edge, Amazon WAF, and other features. See the [documentation](https://docs.amazonaws.cn/aws/latest/userguide/cloudfront.html#feature-diff) for more details.

## Prerequisites

To complete all sections of this article and get a consistent experience with AWS services, please ensure you meet the following prerequisites.

- Your AWS China Region account has completed ICP filing, with ports 80/443 open
- You have an ICP-filed domain
- Use [Amazon Route 53](https://www.amazonaws.cn/route53/) as your DNS service. If you haven't migrated your DNS to Amazon Route 53 yet, see the [reference documentation](https://www.amazonaws.cn/getting-started/tutorials/migrate-domain-to-amazon-route53/)

## Integrating EC2 with CloudFront

In the following sections, you will launch an EC2 instance, set up a web server, integrate EC2 with CloudFront, and deploy a free SSL certificate using the China CloudFront SSL Plugin.

You will also learn some tips for using EC2 and CloudFront, such as using Elastic IP to fix your EC2 public DNS hostname for CloudFront origins, or using AWS-managed prefix lists to enhance EC2 security.

The deployment architecture is shown below:

![Deployment Architecture](images/architecture.png)

### Create EC2 and Install Web Server

In this section, you will create an EC2 instance with a web server, then bind an Elastic IP to fix the EC2 public DNS hostname.

#### 1. Launch EC2 Instance

You can launch an EC2 instance from the EC2 console.

![Launch EC2 Instance](images/ec2-create.jpg)

Name your instance, e.g., "web-server".

You can keep the default AMI and instance type.

- AMI: Amazon Linux 2023
- Instance type: micro

![AMI and Instance Type](images/cloudfront-ssl-2.jpg)

Under "Key pair", select an existing key pair or create a new one for subsequent system administration.

![Key Pair Settings](images/cloudfront-ssl-3.jpg)

For network settings, ensure your EC2 instance is deployed in a public subnet, and check "Allow HTTP traffic from the internet" to make port 80 accessible from the internet.

![Network Configuration](images/cloudfront-ssl-4.jpg)

Expand the "Advanced details" section at the bottom:

![Advanced Details](images/cloudfront-ssl-5.jpg)

At the bottom of the page under "User data", paste the following script to install a web server on first boot. Then click "Launch instance" to start the instance.

```bash
#!/bin/bash
yum install -y httpd
systemctl enable httpd
systemctl start httpd
```

![User Data](images/cloudfront-ssl-6.jpg)

#### 2. Create Elastic IP and Associate with EC2

[Elastic IP](https://docs.amazonaws.cn/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) is a static IPv4 address designed for cloud computing. Using an Elastic IP ensures your EC2 instance's public IP address and public DNS hostname remain unchanged. In this section, you will learn how to associate an Elastic IP with your EC2 instance and access your site using the EC2 instance's public DNS hostname.

Find Elastic IP under "Network & Security" in the EC2 console left menu.

![Elastic IP Menu](images/cloudfront-ssl-7.jpg)

Click "Allocate Elastic IP address" in the upper right, then click "Allocate" to obtain an Elastic IP.

![Allocate Elastic IP](images/cloudfront-ssl-8.jpg)

Select your Elastic IP, click the "Actions" button in the upper right, and choose "Associate Elastic IP address".

![Associate Elastic IP](images/cloudfront-ssl-9.jpg)

Select your previously created EC2 instance and click "Associate" to ensure the EC2 instance's public IP address remains stable.

![Select EC2 Instance](images/cloudfront-ssl-10.jpg)

Click the "Instances" menu on the left to return to the instance list, select your instance, and copy the public IPv4 DNS.

![Copy Public DNS](images/cloudfront-ssl-11.jpg)

Access the public DNS hostname in your browser to verify the web server is installed. You can see the site is currently using port 80 without an SSL/TLS certificate.

![Browser Verification](images/cloudfront-ssl-12.jpg)

In the following sections, you will use this hostname as the CloudFront origin to divert website traffic from EC2 to Amazon CloudFront.

### Create CloudFront Distribution

In this section, you will create a CloudFront distribution and associate it with the previously deployed EC2 instance, routing traffic through CloudFront to accelerate content delivery.

#### 1. Create CloudFront Distribution and Associate EC2

Next, you will quickly set up a CloudFront distribution. Go to the CloudFront console and create a distribution:

![Create CloudFront Distribution](images/cloudfront-ssl-13.jpg)

On the CloudFront configuration page, you will see the basic configuration elements that a CloudFront distribution requires:

- **Origin** – The origin server, supporting multiple AWS services including but not limited to S3, EC2, ELB, API Gateway, as well as third-party origins
- **Cache Behavior** – Define caching behavior through path matching, enable transfer compression, allowed request methods, access control, etc.
- **Settings** – Alternate domain names (CNAME), SSL certificate, default root object, logging, etc.

For the origin, use the EC2 public DNS (with Elastic IP) as the origin domain. Ensure the origin protocol is HTTP.

![Origin Settings](images/cloudfront-ssl-14.jpg)

For the default cache behavior, you can keep the default settings:

![Cache Behavior Settings](images/cloudfront-ssl-15.jpg)

> **Note:** Due to compliance requirements, the default CloudFront distribution domain in the Beijing/Ningxia regions cannot be accessed directly. You must complete domain ICP filing and set up CNAME DNS resolution before access is possible.

In the settings section, enter your ICP-filed domain as the alternate domain name (CNAME):

![Alternate Domain Name Settings](images/cloudfront-ssl-16.jpg)

After creation, wait for deployment to complete. Once deployed, check your alternate domain name — if the domain has passed ICP filing, you should see a "green checkmark".

![ICP Filing Green Checkmark](images/cloudfront-ssl-17.jpg)

After deployment, go to Route 53 (or your DNS provider) to update the DNS configuration. Using Route 53 as an example, enter the corresponding domain's hosted zone and create a new record.

![Route 53 Create Record](images/cloudfront-ssl-18.jpg)

Fill in the DNS record:

![DNS Record Configuration](images/cloudfront-ssl-19.jpg)

After completing the DNS update, open your browser and access the ICP-filed domain:

![Browser Access Domain](images/cloudfront-ssl-20.jpg)

> **Note:** If you encounter a 502 error, check whether EC2 has an SSL certificate installed or whether the origin port is correct. See the [documentation](https://docs.amazonaws.cn/AmazonCloudFront/latest/DeveloperGuide/http-502-bad-gateway.html). If you encounter a 403 error, ensure you are accessing via the ICP-filed domain.

#### 2. Enhance EC2 and Website Security

In this section, you will use [AWS-managed prefix lists](https://docs.amazonaws.cn/vpc/latest/userguide/working-with-aws-managed-prefix-lists.html#available-aws-managed-prefix-lists) to enhance EC2 security. You can use the Amazon CloudFront managed prefix list to restrict inbound HTTP/HTTPS traffic to only the IP addresses of CloudFront origin-facing servers.

Select your instance, go to the EC2 security group, and edit the inbound rules: add an HTTP rule, enter "cloudfront" in the source field, select the `com.amazonaws.global.cloudfront.origin-facing` prefix list, and remove the existing `0.0.0.0/0` rule.

![Security Group Prefix List Configuration](images/cloudfront-ssl-21.jpg)

You can also associate SSL/TLS certificates with CloudFront to enhance website security. In the following section, you will deploy free SSL certificates using the China CloudFront SSL Plugin.

## Deploy Free Certificates with China CloudFront SSL Plugin

Before starting, please confirm once again that you are using Amazon Route 53 for DNS resolution. This section covers the deployment process only. For more details, see the [China CloudFront SSL Plugin](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/?nc1=h_ls).

### 1. Initialize Deployment

Deploy via CloudFormation. Click the [link](https://console.amazonaws.cn/cloudformation/home?#/stacks/create/template?templateURL=https://aws-cn-getting-started.s3.cn-northwest-1.amazonaws.com.cn/china-cloudfront-ssl-plugin/ChinaCloudFrontSslPluginStack.json) to launch the stack in the CloudFormation console.

![CloudFormation Deployment](images/cloudfront-ssl-22.jpg)

### 2. Enter Deployment Parameters

Specify stack details with the following parameters:

- **Stack Name:** Name your stack
- **Email:** Enter your email for SNS email notifications (only one email supported)
- **Domain Name:** Enter the domain names for the SSL certificate. Supports wildcard domains and multiple domains (comma-separated)
- **SSL Renew Interval Days:** Enter the certificate renewal interval. Let's Encrypt certificates are valid for 90 days; enter a number between 1 and 89. Recommended default: 80 days.

![Stack Parameters](images/cloudfront-ssl-23.jpg)

### 3. Confirm Deployment

Review the deployment details on the current page, check the "I acknowledge" box at the bottom, and click **Submit**.

![Confirm Deployment](images/cloudfront-ssl-24.jpg)

After submission, you will see resources being created in the stack events tab. Wait approximately 3 minutes.

### 4. Subscribe to SNS Notifications Promptly

During the stack deployment process, check your email promptly. You will receive an SNS subscription confirmation request from no-reply@sns.amazonaws.com. Please click the confirmation link as soon as possible.

![SNS Subscription Email](images/cloudfront-ssl-25.jpg)

Successful subscription confirmation:

![Subscription Successful](images/cloudfront-ssl-26.jpg)

### 5. Check Stack Deployment Progress

When the stack status changes to green `CREATE_COMPLETE`, the deployment is finished.

Check the "Outputs" tab for quick links:

- **CloudfrontConsole:** Access the CloudFront console to quickly bind the issued certificate
- **ManagementWebURL:** Access SwaggerUI to view or delete existing SSL certificates in IAM
- **S3BucketURL:** Access the S3 console to download the issued SSL certificates

![Stack Outputs](images/cloudfront-ssl-27.jpg)

### 6. Bind SSL Certificate in the Amazon CloudFront Console

After stack deployment is complete, an SSL certificate will be automatically requested for your domain. If you have subscribed to the SNS topic, you will receive an email notification confirming the certificate has been issued. The certificate name consists of the stack name and expiry time, e.g., `Certbot-2023-11-14-1540`.

![SSL Certificate Email Notification](images/cloudfront-ssl-28.jpg)

Open the CloudFront console, select your distribution, and find the option to edit alternate domain names and SSL certificate.

![CloudFront Edit Settings](images/cloudfront-ssl-29.jpg)

Select the corresponding SSL certificate from the custom SSL certificate dropdown, then save changes.

![Select SSL Certificate](images/cloudfront-ssl-30.jpg)

After deployment, you can access your CloudFront-accelerated site via HTTPS in the browser and verify the SSL certificate issued by Let's Encrypt, valid for 90 days.

![HTTPS Access Verification](images/cloudfront-ssl-31.jpg)

For more information on using the China CloudFront SSL Plugin, see the [plugin documentation](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/?nc1=h_ls).

## Summary

Through this article, you have learned the basics of Amazon CloudFront and how to divert website traffic deployed on EC2 to CloudFront for acceleration and cost savings. You have also learned to use AWS-managed prefix lists in EC2 security groups to ensure your EC2 only accepts traffic originating from CloudFront, and to deploy free SSL certificates using the China CloudFront SSL Plugin to protect your site with HTTPS.

## References

- [China CloudFront SSL Plugin](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/?nc1=h_ls)
- [Amazon CloudFront Introduction](https://docs.amazonaws.cn/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
- [Amazon CloudFront China Region Differences](https://docs.amazonaws.cn/aws/latest/userguide/cloudfront.html#feature-diff)
- [Network Acceleration with Amazon CloudFront in China](https://www.amazonaws.cn/getting-started/use-cases/cloudfront-network-acceleration/?nc1=h_ls)

---

> **Original Post:** [Amazon CloudFront Deployment Mini-Guide (Part 8) - Deploy Free Certificates with China CloudFront and CloudFront SSL Plugin](https://aws.amazon.com/cn/blogs/china/divert-website-access-traffic-from-ec2-to-amazon-cloudfront/)
>
> **GitHub:** [aws-samples/China-CloudFront-SSL-Plugin](https://github.com/aws-samples/China-CloudFront-SSL-Plugin)
