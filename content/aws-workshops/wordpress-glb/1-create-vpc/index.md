---
title: "1. 创建Amazon VPC"
weight: 3
type: workshops
---
在本模块中，您将首先为 WordPress 站点创建一个包括有公有子网和私有子网的VPC。通常来说，对于必须连接互联网的资源，应放置在公有子网，对于不需要连接到互联网的资源，应放置在私有子网，以提升整体架构的安全性。因此在实验中，WordPress的Web服务器位于公有子网之内，数据库服务器则位于私有子网。

在下面的步骤中，您将使用亚马逊云科技管理控制台中的VPC服务创建一个包括有公有子网和私有子网的VPC。

#### 1.1 打开亚马逊云科技管理控制台


通过以下链接：[https://ap-northeast-1.console.aws.amazon.com/console/home?region=ap-northeast-1#](https://ap-northeast-1.console.aws.amazon.com/console/home?region=ap-northeast-1#)，进入管理控制台。确保所在区域为**亚太地区（东京）ap-northeast-1**

![image-20221011172534313](/aws-workshops/wordpress-glb/assets/1-create-vpc/1-region.png)

#### 1.2 在查找服务处搜索VPC，并点击

![image-20221011172738773](/aws-workshops/wordpress-glb/assets/1-create-vpc/2-search.png)

#### 1.3 单击橙色的“创建VPC”按钮

![image-20221011173429867](/aws-workshops/wordpress-glb/assets/1-create-vpc/3-launch-wizard.png)

#### 1.4 在创建VPC页面中您可以对VPC进行一些配置
本次实验您需要填写VPC的名字，例如`WordPress`。其他保持默认，在页面底部点击橙色“创建VPC”按钮

![image-20221011174429340](/aws-workshops/wordpress-glb/assets/1-create-vpc/4-input-name.png)

#### 1.5 观察创建过程

您应会看到VPC启动向导创建的有关VPC资源。等待所有进程创建完毕后，您可以点击橙色**View VPC**按钮，查看创建后的VPC

![image-20221011174554800](/aws-workshops/wordpress-glb/assets/1-create-vpc/5-vpc-created.png)

#### 1.6 查阅创建后的子网名称、子网ID、IPv4 CIDR以及可用区信息

在左侧菜单栏选择“子网”，在筛选输入栏中输入`wordpress`， 打开记事本并记录相关子网名称和子网ID信息。

![image-20221011175620854](/aws-workshops/wordpress-glb/assets/1-create-vpc/6-subnet-info.png)



在本模块中，您使用VPC启动向导创建了一个Amazon VPC用于将 Amazon 资源启动到您定义的虚拟网络中。在下一个模块中，您将创建 Amazon EC2 实例以运行 WordPress 站点。
