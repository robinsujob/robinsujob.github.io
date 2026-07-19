---
title: "3. 上传应用程序和租户入驻"
weight: 5
type: workshops
---
### 1. 上传您的应用程序

配置服务后，SaaS Boost 将自动为服务创建一个[Amazon ECR ](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)镜像仓库。 

任何租户入驻（Onboarding）到系统之前，您必须为应用程序中的每个服务上传一个 Docker 镜像至SaaS Boost ECR中。 在 **“Summary”** 页面中，点击 **“Service"** 的区域中的 ECR Repository URL列出的教程，以查看用于上传 Docker 镜像的推送命令及步骤。

![](/workshops/glbsaas-boost/assets/3-create-tenants/1-summary.png)

在本次动手训练营中，您将通过Cloud9中的演示程序构建脚本，为您自动构建 Docker 容器并推送。 

在查找服务处搜索 Cloud9，或点击[链接](https://us-east-1.console.aws.amazon.com/cloud9control/home?region=us-east-1#/product)进入Cloud9控制面板。

![image-1](/workshops/glbsaas-boost/assets/1-create-cloud-9/1-cloud9.png)

在Cloud9的**环境**列表里，点击 **打开** 进入IDE环境。

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/6-open-env.png)

演示程序的代码位于克隆的 SaaS Boost 代码仓库中的 **samples/java/** 目录中，其中`build.sh`文件将构建容器化应用程序并将镜像推送到 SaaS Boost ECR 仓库。您可以查看此示例 shell 脚本中的步骤，了解如何通过构建过程使您的应用程序与 SaaS Boost 灵活集成。

请执行以下命令，构建容器化应用程序并将镜像推送到 SaaS Boost ECR 仓库。

```shell
cd ~/environment/aws-saas-boost/samples/java
sh build.sh
```

此脚本会提示您提供 SaaS Boost 环境名称。输入您在运行 SaaS Boost 安装程序时指定的环境标签，例如`workshop`。

然后该脚本将提示您输入正在构建的服务的编号。在本例中，使用 `main`。请注明服务名称的编号。

![](/workshops/glbsaas-boost/assets/3-create-tenants/2-input-workshop-svc-name.png)

此脚本完成后，演示程序的镜像会发布到 SaaS Boost 镜像仓库。执行后的结果如图所示：

![](/workshops/glbsaas-boost/assets/3-create-tenants/3-uploaded-ecr.png)

当您对应用程序进行更改时，您可以再次执行构建脚本来更新您的应用程序。对于多服务应用程序，您需要为您配置的每个服务重复相同的步骤。

### 2. 创建租户并入驻

完成镜像上传后，您现在可以创建一个新租户，为该租户提供所有必要的基础架构来支持您的应用程序，并部署您配置的服务。

请进入到SaaS Boost控制台，在左侧点击**Onboarding**进入到Onboarding入驻界面，然后单击 **Provision Tenant** 按钮。

![](/workshops/glbsaas-boost/assets/3-create-tenants/4-onboarding.png)

请为您的租户命名，例如`TenantA`，其他保持默认，随后点击**Submit**提交按钮。

![](/workshops/glbsaas-boost/assets/3-create-tenants/5-provison-tenant.png)

在您提交租户配置后， 入驻流程将会根据您的服务配置自动创建应用所需的基础设施，您可以在入驻请求细节中查看入驻的状态。**演示程序的入驻过程大约需要15分钟左右。**

![](/workshops/glbsaas-boost/assets/3-create-tenants/6-create-tenant.png)

当入驻状态显示为**Deployed**，表明租户已成功配置。

![image-20230624010546124](/workshops/glbsaas-boost/assets/3-create-tenants/7-deployed-tenant.png)

部署流程完成后，您将能够访问该租户的演示程序。

请进入到SaaS Boost控制台，在左侧点击 **Tenants** ，然后点击对应的租户

![](/workshops/glbsaas-boost/assets/3-create-tenants/8-tenant.png)

随后单击，**Address**下中链接。

![](/workshops/glbsaas-boost/assets/3-create-tenants/9-click-address.png)

点击后，您应该能看到如下界面。

![](/workshops/glbsaas-boost/assets/3-create-tenants/10-website.png)


{{% workshop-alert type="success" %}}
您已经完成了应用程序部署以及租户入驻的步骤！
{{% /workshop-alert %}}
