---
title: "4. 总结"
weight: 6
type: workshops
---
本指南简要介绍了设置 SaaS Boost 所需的基本步骤。当您考虑将工作负载转移到 SaaS Boost  中时，请详细地参阅 SaaS Boost 更多功能。您需要仔细地查看您的应用程序的配置方案，以及它们如何适配到不同的 SaaS Boost 应用程序设置。

在熟悉了以上步骤之后，您可以继续通过查看 SaaS Boost [用户指南](https://github.com/awslabs/aws-saas-boost/blob/main/docs/user-guide.md) 和 [开发人员指南](https://github.com/awslabs/aws-saas-boost/blob/main/docs/developer-guide.md) 来更好地配置 SaaS Boost 模型。

容器化工作负载所需的步骤因应用程序的性质而异。您可以使用 SaaS Boost 提供的示例应用程序中的 Dockerfile 示例。以下是一些提供有关容器化应用程序信息的其他资源：

- [亚马逊云科技学习路径：容器化单体应用](https://aws.amazon.com/getting-started/container-microservices-tutorial/module-one/)
- [亚马逊云科技 App2Container](https://aws.amazon.com/app2container/)

---

### 清理资源

如果您需要卸载体验的SaaS Boost，请遵循以下步骤。



[//]: # (#### 1. 删除租户)

[//]: #
[//]: # (清空所有租户列表中的租户。)

[//]: #
[//]: # (![]&#40;/aws-workshops/glbsaas-boost/assets/4-summary/1-delete-tenants.png)
#### 1. 卸载SaaS Boost

在Cloud9的终端中运行以下命令：

```shell
cd ~/environment/aws-saas-boost
./install.sh 
```

根据提示选择**第5项**执行卸载流程，卸载流程会提示您提供 SaaS Boost 环境名称，并进行二次确认。


{{% workshop-alert type="warning" %}}
删除SaaS Boost 环境是不可逆的，所有已部署的租户资源都将被删除！
{{% /workshop-alert %}}


请连续两次输入您在运行 SaaS Boost 安装程序时指定的环境标签，例如`workshop`，并输入`y`完成二次确认。如图所示卸载流程将首先完成租户资源的清除，最后会完成SaaS Boost的卸载。

![](/aws-workshops/glbsaas-boost/assets/4-summary/2-delete-saas-boost.png)

若您看到**Delete of SaaS Boost environment workshop complete.**的提示则代表您的环境已经删除。

![](/aws-workshops/glbsaas-boost/assets/4-summary/2-1-deleted-saas-boost.png)

#### 2. 删除Cloud9

在Cloud9的环境列表，选择需要删除的IDE环境，点击右上角“删除”按钮。

![](/aws-workshops/glbsaas-boost/assets/4-summary/3-delete-cloud9.png)

在弹出的提示框中，输入“删除”，确认删除环境。

![](/aws-workshops/glbsaas-boost/assets/4-summary/4-confirm-delete.png)
