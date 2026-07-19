---
title: "4. 分配弹性IP地址"
weight: 6
type: workshops
---
目前为止，您已创建 RDS 数据库和 EC2 实例。在后面的几个模块您会连接EC2实例进行一些配置和安装工作。

在本次[动手训练营的第2节2.5步](/aws-workshops/wordpress-glb/2-create-ec2/#2.5)配置网络信息部分，您选择了自动分配公有IP地址的选项。当您启动EC2实例时会自动为您分配一个公有的IPv4地址。但是当您停止EC2实例时，该自动分配的公有IP地址会被释放。要保留永不更改的公有 IP地址，您需要将[弹性 IP 地址](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html)您的实例关联。

在后面的步骤中，您将分配一个弹性IP并与EC2实例关联。

#### 4.1 跳转到EC2实例界面

在亚马逊云科技控制台中，转到 [EC2 实例页面](https://ap-northeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-northeast-1#Instances:v=3;instanceState=running)。您会看到自己为 WordPress 安装创建的 EC2 实例。单击该实例，在实例摘要中可以看到EC2实例的公有IP地址。该实例的公有 IP 地址是在创建EC2实例时自动分配的。在某些情况下，自动分配的公有IP地址会被释放，例如实例停止、休眠等。**如果您需要永久的公有IP地址，可改为使用[弹性 IP 地址](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html)**。

![image-1](/aws-workshops/wordpress-glb/assets/4-create-eip/4-Picture1.png)

#### 4.2 选择弹性IP界面 

为了固定该实例的公有IP地址，我们将为该实例分配弹性IP地址。在EC2控制台界面，左侧导航栏，在“**网络与安全**”菜单下点击弹性IP。

![image-2](/aws-workshops/wordpress-glb/assets/4-create-eip/4-Picture2.png)

#### 4.3 分配弹性IP

在弹性IP地址界面，点击右上角的橙色按钮“分配弹性IP地址”，保持默认项，选择分配，您可以获得到一个公有弹性IP地址。

![image-3](/aws-workshops/wordpress-glb/assets/4-create-eip/4-Picture3.png)

![image-4](/aws-workshops/wordpress-glb/assets/4-create-eip/4-Picture4.png)

#### 4.4 选择关联弹性IP 

将该弹性IP地址附加到创建的EC2实例中。选中该弹性IP，点击右上角操作，选中关联弹性IP地址

![image-5](/aws-workshops/wordpress-glb/assets/4-create-eip/4-Picture5.png)

#### 4.5 将弹性IP关联到EC2实例

选择需要绑定的EC2实例，本实验中实例名称是WordPress。点击右下角的橙色按钮“关联”。”

随后您将看到关联成功的提示，点击实例ID，回到EC2控制面板。

![image-6](/aws-workshops/wordpress-glb/assets/4-create-eip/4-Picture6.png)

![image-7](/aws-workshops/wordpress-glb/assets/4-create-eip/4-Picture7.png)

在本模块中，您完成了为EC2实例分配弹性IP的步骤。在下一个模块您学习如何连接EC2实例。
