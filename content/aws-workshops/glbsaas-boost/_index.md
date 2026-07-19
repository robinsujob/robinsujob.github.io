---
title: "SaaS Boost入门指南"
weight: 8
type: workshops
shortTitle: "AWS SaaS Boost"
homeTitle: "SaaS Boost入门指南"
summary: "安装和配置 AWS SaaS Boost，构建示例容器应用，完成服务配置、租户入驻、访问验证与资源清理。"
workshopRoot: true
---
本文档介绍了在亚马逊云科技 SaaS Boost 中安装、配置和运行工作负载的基本步骤。请参阅其他 SaaS Boost 文档，以更全面地了解系统。

本文档概述了设置亚马逊云科技 SaaS Boost 的步骤，但并不深入探讨用户体验或底层技术。如果您需要参考更多相关详细信息，请参考 [用户指南](https://github.com/awslabs/aws-saas-boost/blob/main/docs/user-guide.md) 和 [开发人员指南](https://github.com/awslabs/aws-saas-boost/blob/main/docs/developer-guide.md)。


## 体验目标

在深入研究设置亚马逊云科技 SaaS Boost 所需的步骤之前，让我们先了解一下环境的基本元素，以便更好地了解 SaaS Boost 支持的功能。下图按设置流程的顺序显示了 SaaS Boost 的关键组件。

![gs-install-flow](/aws-workshops/glbsaas-boost/assets/gs-install-flow.png)

以下是每个步骤的细分：

1. 为安装过程设置所需的工具
2. 克隆 SaaS Boost 存储库
3. 将 SaaS Boost 功能安装到您的亚马逊云科技账户中
4. 访问 SaaS Boost 管理控制台
5. 根据您的要求配置分层和应用程序
6. 为应用程序中的每个服务上传 Docker 镜像

在此阶段，环境的所有组成部分现在都已准备就绪，可以开始载入租户。您可以使用 SaaS Boost 应用程序载入新租户，也可以从应用程序进行 API 调用以触发新租户的载入。

要考虑的最后一点是应用程序的更新过程。当您的应用程序发生变更时，您可以将最新版本上传到 SaaS  Boost。每当上传新版本时，它将自动部署到系统中的所有租户。SaaS Boost 现已准备好作为 SaaS 业务运营，这包括内置于 SaaS  Boost 环境中的操作和管理工具。

至此您已经对 SaaS Boost 技术有了一定的了解，接下来让我们来看看设置 SaaS Boost 所涉及的详细信息。

---

*Contact: Robin Su([usuzhe@amazon.com ](mailto:usuzhe@amazon.com))*

*Last Update: 2023/06/30*
