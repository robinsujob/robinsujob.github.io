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

> **Original Post:** [Amazon CloudFront Deployment Guide (Part 8) - Deploy Free Certificates Using China CloudFront and SSL Plugin](https://aws.amazon.com/cn/blogs/china/divert-website-access-traffic-from-ec2-to-amazon-cloudfront/)
>
> **GitHub:** [aws-samples/China-CloudFront-SSL-Plugin](https://github.com/aws-samples/China-CloudFront-SSL-Plugin)

This article applies to AWS China Region services. You will learn how to use Amazon CloudFront in the China Region to accelerate and distribute traffic from websites deployed on EC2, and use the [China CloudFront SSL Plugin](https://www.amazonaws.cn/getting-started/tutorials/create-ssl-with-cloudfront/) to deploy free SSL certificates to protect your site. The plugin helps you generate, renew, and download free SSL certificates in the AWS China Regions, with Amazon CloudFront integration and automatic certificate renewal. You can also refer to the EC2-CloudFront integration section for configuring CloudFront to distribute EC2 website traffic in AWS Global Regions.

## Why Choose Amazon CloudFront?

Amazon CloudFront is a Content Delivery Network (CDN) service provided by AWS. Using a CDN reduces website load times, lowers bounce rates, and increases traffic and revenue, while also reducing the load on origin servers, improving website stability and security. Amazon CloudFront securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds in a developer-friendly environment, and integrates seamlessly with Amazon S3, Elastic Load Balancer, Amazon EC2, and more.

Amazon CloudFront not only accelerates your website and reduces origin server load, but also lowers the data transfer costs for traffic leaving your AWS-hosted website to the internet. For example, compared to EC2's outbound data transfer costs, using Amazon CloudFront in the AWS China Regions can help you reduce outbound data transfer costs by at least 67%. For specific pricing, refer to [EC2 Data Transfer Pricing](https://www.amazonaws.cn/ec2/pricing/#Amazon_EC2_.E6.95.B0.E6.8D.AE.E4.BC.A0.E8.BE.93) and [CloudFront Data Transfer Pricing](https://www.amazonaws.cn/cloudfront/pricing/#On-demand_Pricing).
