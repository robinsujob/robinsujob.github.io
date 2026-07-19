---
title: "1.订阅和部署解决方案"
weight: 3
type: workshops
---
imAgine绘图解决方案已经登陆亚马逊云科技Marketplace，您可以通过订阅解决方案来进行快速体验。

在操作之前请确保您已经登陆至亚马逊云科技控制台，您可以点击以下链接快速进入控制台：https://us-east-1.console.aws.amazon.com/console/home?region=us-east-1

或在控制台右上角确认您当前所在的区域为**美国东部 (弗吉尼亚北部) us-east-1**，否则请切换。

![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/0-region.png)

#### 1.  开始订阅

请点击 [Marketplace 链接](https://aws.amazon.com/marketplace/pp/prodview-ohjyijddo2gka)，进入 Marketplace 产品页面完成订阅流程。

点击右上角橙色按钮 **Continue to Subscribe**，您将在此处完成产品条款、使用条件和软件服务费的确认。

![img](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/2-marketplace.png)

确认产品条款、使用条件和软件服务费的无误后，点击 **“Accept Terms”**。


{{% workshop-alert type="info" %}}
文中的订阅链接为免费版 AMI 产品，除 EC2、EBS 等正常的 AWS 服务使用费，不会产生额外费用。
{{% /workshop-alert %}}


![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/3-accept-terms.png)

您需要在此页面进行等待，显示 “Pending” 则代表订阅还在验证中。

![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/4-pending.png)

大概需要数分钟来确认您的订阅，页面下方会展示订阅的有效期。到此为止，订阅流程已完成。随后您将进行解决方案的部署。

#### 2. 选择部署版本

当界面下方显示具体日期后，即可使用该订阅包含的 AMI，点击右上角 “Continue to Configuration” 继续下一步

![img](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/5-subscribed.png)

关于Software version，请选择专为本次动手训练营准备的 ***imAgine-Workshop-and-Blog-20240115***，在该版本中，为您预装了本workshop所需的模型，以及常用的模型管理插件，历史图片浏览插件等。

对于 Region，Marketplace 的订阅在所有区域都适用，因此您可以选择任意您所需的区域启动，本文中选择的区域为 美国东部 (弗吉尼亚北部) us-east-1


{{% workshop-alert type="info" %}}
您需要保证您需要启动 AMI 的区域有足够的 G 系列 EC2 服务器限额，请参考上一节前提条件完成 G 系列限额提升
{{% /workshop-alert %}}


![img](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/6-deploy-solution.png)

确认版本与区域选择后，点击 “Continue to Launch” 进入启动 EC2 服务器的设置界面。

#### 3. 通过EC2启动解决方案

在启动方式界面，请选择通过EC2启动，随后您将跳转到 EC2 控制台以完成 imAgine 解决方案的部署。

![img](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/7-launch-from-ec2.png)

在启动实例界面，首先填写服务器名称，例如`sd-workshop`。同时请在此处检查 AMI 版本，确保是从 imAgine-Workshop 版本启动。

![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/8-ec2-name.png)

**选择 EC2 实例类型**：此处我们建议选择 g4dn.2xlarge 或 g5.2xlarge，分别拥有 16G 显存和 24G 显存的 GPU。

![image-20230718162753567](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/9-instance-type.png)

**密钥对**：如果您需要使用本地 SSH 工具连接进服务器，则需要在此处创建新密钥并指定，同时需要注意安全组开放 22 端口；如果对 SSH 并不熟悉，请选择 **“在没有密钥对的情况下继续”。**

![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/10-key-pair.png)

**网络配置**：因为 imAgine 中部署的 Stable Diffusion Webui 是一个面向公网提供的 Web 服务，请选择一个公有子网来启动服务器，并允许来自互联网的流量访问80端口，同时确保此处 “自动分配公有 IP” 保持启用状态。

解决方案将帮助您创建安全组及规则，将允许所有来自互联网的流量访问80端口以保证Webui页面可以被正常访问，默认将在Default VPC的公有子网中启动实例。您可以保持默认网络配置。

![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/10-network.png)

 存储默认将使用120GB，用于存储模型相关文件。您可以保持默认存储配置。

![img](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/11-ebs.png)

配置完成后请点击右下角“启动实例”按钮，启动对应实例。

![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/12-launch-ec2.png)

您可以点击实例ID查看启动状态。当实例状态成为“正在运行”以及“状态检查”通过，则实例成功启动。

![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/13-instance-id.png)

#### 4.访问imAgine（Stable Diffusion Webui）

服务器正常启动后，即可在 EC2 控制台界面找到，选中该服务器，复制服务器的**公有 IPv4 地址**

![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/14-public-ip.png)

通过浏览器访问该 IP 地址的 80 端口，在 IP 地址前添加`http://`，例如服务器 IP 为44.200.187.XX，则需要在浏览器地址栏输入`http://44.200.187.XX`

![img](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/15-browser.png)

您会在浏览器上看到登录提示框，用户名为固定的`webui`，密码则为该 EC2 服务器的实例 ID，可以在EC2控制台找到。

![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/16-webui-login.png)

![](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/17-instance-id.png)

填写完成后点击 “登录”，即可进入 Stable Diffusion Webui 界面，您将在此处开始尽情施展艺术创意。

![img](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/18-webui.png)


{{% workshop-alert type="info" %}}
如果访问服务器时出现以下网页内容，请稍等。初次从 Marketplace 订阅的 AMI 运行imAgine绘画服务，通常需要等待 10-15 分钟，以完成服务依赖和模型的加载。
{{% /workshop-alert %}}


![img](/aws-workshops/glb-aigc-ami-workshop/assets/1-subscribe/19-login-page.png)
