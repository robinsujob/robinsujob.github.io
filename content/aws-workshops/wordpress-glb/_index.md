---
title: "动手训练营 - 在两层架构中部署 WordPress和Amazon RDS"
weight: 1
type: workshops
shortTitle: "WordPress + Amazon RDS"
homeTitle: "在两层架构中部署 WordPress和RDS"
originalUrl: "https://catalog.us-east-1.prod.workshops.aws/workshops/ff2db477-bf34-45cc-832a-169f687c4896/zh-CN"
summary: "从零创建 VPC、EC2、弹性 IP 和 Amazon RDS for MySQL，部署 WordPress，并完成数据库安全加固及多可用区故障转移实验。"
workshopRoot: true
---
WordPress 是一种灵活的内容管理系统，用于构建博客、电子商务站点、讨论区等等。无论您创建何种网站，都要存储内容。对于博客而言，需要存储的内容是博客文章和评论。对于电子商务站点而言，需要存储的内容是产品和用户账户。

这些内容需要永久存储在某个地方。WordPress 使用 MySQL 来存储这些内容。WordPress 应用程序中的许多数据都是分层的结构化数据。例如，应用程序可能含有博客文章，而后者又含有用户提交的评论。关系数据库很适合存储类似这样的分层数据。此外，MySQL 是最常用的开源数据库，而且能为此类应用程序提供可靠和出色的性能。

在本实验中，您将学习如何在亚马逊云科技中，使用EC2设置 WordPress 站点来运行博客。WordPress 需要一个 MySQL 数据库来存储其数据。对于本次实验，您还将使用 Amazon RDS for MySQL 来运行您的 MySQL 数据库。

---

*Contact: Robin Su([usuzhe@amazon.com ](mailto:usuzhe@amazon.com)), Luna Lu ([luhaoy@amazon.com ](mailto:luhaoy@amazon.com)), Jason Jin([jasojin@amazon.com](mailto:jasonjin@amazon.com)), Zepei Yu([yuzp@amazon.com ](mailto:yuzp@amazon.com))*

*Last Update: 2024/02/04*
