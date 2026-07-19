---
title: "2. 配置SaaS Boost"
weight: 4
type: workshops
---
### 1. 登录SaaS Boost

如果您成功安装了Saas Boost，您可以在您的邮箱中找到由`no-reply@verificationemail.com`发送的邮件。

![](/workshops/glbsaas-boost/assets/2-saas-boost-setup/1-email-info.png)

点击链接并输入用户名和密码，登录至SaaS Boost控制台。首次登录时需要修改密码。

![](/workshops/glbsaas-boost/assets/2-saas-boost-setup/2-change-pwd.png)

登录后的界面如下。

![](/workshops/glbsaas-boost/assets/2-saas-boost-setup/3-console-ui.png)

### 2. 为演示程序配置SaaS Boost

登录SaaS Boost控制台后，您需要做的第一件事是配置环境，以使其与您的应用程序的运行需求保持一致。

因此您必须为此本次动手训练营的演示程序进行正确设置。此演示程序依赖于 SaaS Boost 中的以下配置。

我们将参照以下配置项来确保 SaaS Boost 以支持您的应用程序。演示程序依赖于 SaaS Boost 中的以下配置：

- 为应用程序输入一个友好的名称 `Name`，例如 **Sample**
- 创建一个 `New Service` 并给它一个名称，例如 **main**
- 确保 `Publicly access` 框被**选中**
- 确保 `Service Addressable Path` 是 **/\***
- 对于 `Container OS`，选择 **Linux**
- 将 `Container Tag` 设置为**latest**
- 将 `Container Port` 设置为 **8080**
- 将 `Health Check URL` 设置为 **/index.html**
- 在 `default` 层设置下，将 `Compute Size` 设置为 **Medium**
- `Minimum Instance Count` 和 `Maximum Instance Count` 可以分别为 **1** 和 **2**
- **启用** `Provision a File System for the application` 复选框
- 将 `Mount point` 设置为 **/mnt**
- **启用** `Provision a File System for the application` 复选框
- 选择对应的数据库（具有 db.t3.micro 实例类的 MariaDB 将提供最快的启动速度）
- 输入 **数据库名称**、**用户名**和**密码**。您 *不需要* 为数据库初始化提供 SQL 文件。

从屏幕左侧的导航中选择**Application**。出现类似于以下内容的页面： 

![](/workshops/glbsaas-boost/assets/2-saas-boost-setup/5-application.png)

#### 2.1 填写应用名称

首先为您的应用程序提供一个的名称，例如`Sample`。本次动手训练营您无需填写 **域名** 或 **SSL 证书** 条目即可进行测试。

> 在生产环境中，确保您在 [Amazon Certificate Manager ](https://aws.amazon.com/certificate-manager/)中为您将托管 SaaS 应用程序的域名定义了一个证书。请注意， [注册域名 ](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register.html)和 [设置 SSL 证书 ](https://docs.aws.amazon.com/acm/latest/userguide/gs.html)必须在配置SaaS Boost 之前完成。 

![](/workshops/glbsaas-boost/assets/2-saas-boost-setup/6-application-name.png)

#### 2.2 创建服务

SaaS Boost 让您可以根据需要进行配置，通过尽可能多的“服务”来支持您的工作负载。您为每个服务提供单独的 Docker  镜像。这些服务可以是公共的或私有的，并且彼此独立配置。服务之间不共享文件系统或数据库等基础设施资源，但它们可以在预置的 VPC 网络内相互通信。公有服务通过应用负载均衡器公开，并可通过互联网上的 DNS  访问。私有服务无法从互联网访问。

通过单击 **New Service** 按钮创建您的第一个服务。将出现类似于以下的弹出对话框：

![7-new-service](/workshops/glbsaas-boost/assets/2-saas-boost-setup/7-new-service.png)

为服务命名，例如 `main`，随后点击单击弹出对话框中右下角的**Create Service**按钮

![8-main-svc](/workshops/glbsaas-boost/assets/2-saas-boost-setup/8-main-svc.png)

新服务将出现在服务列表中，单击服务名称以展开该服务的配置选项。将出现如图的表单。

![9-main-form](/workshops/glbsaas-boost/assets/2-saas-boost-setup/9-main-form.png)

#### 2.3 配置服务

随后将根据演示程序的依赖，配置以下内容。您的配置应类似于以下内容：

![](/workshops/glbsaas-boost/assets/2-saas-boost-setup/10-filled-svc.png)

最后，在页面底部点击**Submit**按钮，提交您的服务配置。

![](/workshops/glbsaas-boost/assets/2-saas-boost-setup/11-submit-svc.png)

关于更多配置，请参阅 [用户指南](https://github.com/awslabs/aws-saas-boost/blob/main/docs/user-guide.md) 和 [开发人员指南](https://github.com/awslabs/aws-saas-boost/blob/main/docs/developer-guide.md)，深入了解如何使用服务来部署您的 SaaS 应用程序。



在下一节您将上传演示程序并分配租户以使用SaaS Boost实现应用程序的SaaS化。
