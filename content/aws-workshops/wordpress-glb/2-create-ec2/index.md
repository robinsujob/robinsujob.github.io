---
title: "2. 创建EC2实例"
weight: 4
type: workshops
---
在本模块中，您将创建一个 Amazon EC2 实例来运行您的 WordPress 网站。Amazon EC2 按需提供高度可配置的服务器实例。在 EC2 实例上，您可以运行可供各地用户访问的 WordPress 网站。

Amazon EC2 提供按需服务器预置。借助 Amazon EC2，您可以租用具有不同大小、CPU、RAM 和网络配置的服务器实例。这些服务器按使用时间计费，您可以使用它们来托管网站（例如 WordPress 网站）。使用 EC2 实例后，您的 WordPress 网站将能持续运行，并且任何人都可以通过互联网访问它。

在以下步骤中，您将启动一个 EC2 实例来托管您的 WordPress 网站。

#### 2.1 搜索EC2服务

在页面顶部“服务”处搜索`EC2`，并点击，进入EC2控制面板

![image-20221011180306693](/aws-workshops/wordpress-glb/assets/2-create-ec2/1-search-service.png)

#### 2.2 进入EC2创建向导

点击“启动实例”，开始创建EC2实例。

![image-20221011180729057](/aws-workshops/wordpress-glb/assets/2-create-ec2/2-ec2-launch-wizard.png)

#### 2.3 选择 Amazon 系统映像（AMI）

 [Amazon 系统映像（AMI）](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/AMIs.html)将决定新 EC2 实例上安装的基本软件，其中包括操作系统（Amazon Linux、Red Hat Enterprise Linux、Ubuntu、Microsoft Server 等）以及计算机上安装的应用程序。

本次实验请在 AMI 选择视图中选择Amazon Linux 2023 AMI，**架构选择64位(ARM)**。

![image-20221011181050818](/aws-workshops/wordpress-glb/assets/2-create-ec2/3-ami.png)

#### 2.4 选择实例类型

选择实例类型在 EC2 向导的第二步。实例类型是 CPU、内存 (RAM)、存储和网络容量的特定配置。本次实验选择**m7g.large**，请您在筛选条件中输入m7g, 并选择**m7g.large**型号。

![image-20221011181216749](/aws-workshops/wordpress-glb/assets/2-create-ec2/4.1-instance-type.png)

#### 2.5 创建用于登陆EC2实例的密钥对

您将使用密钥对通过 SSH 访问实例，从而使您能够在服务器上运行命令。
为您的实例创建新的密钥对，并为其命名。根据连接方式选择密钥类型（pem/ppk）然后，单击下载密钥对按钮，将.pem/.ppk文件下载到您的计算机上，妥善保管以便在后续实验中使用。

![image-20221011183218056](/aws-workshops/wordpress-glb/assets/2-create-ec2/12.1-create-key-pair.png)

![image-20221011183245296](/aws-workshops/wordpress-glb/assets/2-create-ec2/12.2-download-key-pair.png)

#### 2.6 配置实例网络信息

为实例配置网络详细信息。点击右上角编辑按钮，选择对应名为**WordPress**的VPC，及一个**公有子网（subnet-public）**，并**启用自动分配公有IP选项**。

![image-20221011181524879](/aws-workshops/wordpress-glb/assets/2-create-ec2/5.2-auto-public-ip.png)

![image-20221011181453129](/aws-workshops/wordpress-glb/assets/2-create-ec2/5.1-vpc-info.png)

#### 2.7 配置安全组

为实例配置安全组，在这里为WordPress实例创建一个安全组。安全组名称填写**wordpress-sg**，填写描述信息。

亚马逊云科技中的安全组（Security Group）充当虚拟防火墙，描述了可以访问资源网络流量类型，这意味着您可以使用[安全组控制到资源的流量](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/ec2-security-groups.html)。

![image-20221011182404256](/aws-workshops/wordpress-glb/assets/2-create-ec2/9-sg-name.png)

#### 2.8 添加安全组规则

为安全组添加规则。通常根据情况，需要允许两种类型的流量访问您的WordPress资源：

- 来自您当前 IP 地址的 SSH 流量，让您可以使用 SSH 协议登录到 EC2 实例并配置 WordPress
  - 在规则区域，其中已配置了 SSH 规则，但是它允许从任何 IP 地址进行 SSH 访问。**在源下方单击，源选择我的IP**

![image-20221011182554277](/aws-workshops/wordpress-glb/assets/2-create-ec2/10.1-sg-ssh.png)

- 来自所有 IP 地址的 HTTP 流量，让用户可以查看您的 WordPress 网站
  - 点击添加安全组规则，在新建的安全组规则中，单击类型列下方的下拉列表。选择 HTTP，在源类型下方单击列表，选择任何位置。

![image-20221011182804550](/aws-workshops/wordpress-glb/assets/2-create-ec2/10.2-sg-http.png)

#### 2.9 设定存储大小

为实例设定存储大小，根据需求填写。本实验建议设定20GB-30GB，磁盘类型选择gp3。

![image-20221011182055857](/aws-workshops/wordpress-glb/assets/2-create-ec2/7-ebs.png)

#### 2.10 配置用户数据（首次启动时初始化实例的代码）

在页面最下方的高级详细信息中，请将下面的shell脚本代码粘贴至[用户数据](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/user-data.html)处，该代码将在实例首次启动时，将安装并配置Apache、PHP、MySQL客户端等WordPress安装所需的服务及配置。

```shell
#!/bin/bash
#安装WordPress依赖
dnf update -y
dnf install -y mariadb105-server httpd wget php-fpm php-mysqli php-json php php-devel

#修改Apache客户端权限，以便于WordPress创建文件
chown -R apache /var/www
chgrp -R apache /var/www
chmod 2775 /var/www
find /var/www -type d -exec sudo chmod 2775 {} \;
find /var/www -type f -exec sudo chmod 0644 {} \;

#下载WordPress并安装
wget https://cn.wordpress.org/latest-zh_CN.tar.gz
tar -xzf latest-zh_CN.tar.gz
cp -r wordpress/* /var/www/html/

#重启服务并设定开机自启动
service httpd restart
systemctl enable httpd
```

![image-20221011181810047](/aws-workshops/wordpress-glb/assets/2-create-ec2/6-user-data.png)

#### 2.11 检查实例信息，启动
检查实例创建信息，尤其是VPC、子网信息，点击右侧橙色按钮“启动实例”

![image-20221011183026869](/aws-workshops/wordpress-glb/assets/2-create-ec2/11-check-info.png)

#### 2.12 查看实例启动状态

点击实例ID查看启动状态。当实例状态成为“正在运行”以及“状态检查”通过，则实例成功启动。

![image-20221011183438228](/aws-workshops/wordpress-glb/assets/2-create-ec2/13.1-created-instance.png)

![image-20221011183504873](/aws-workshops/wordpress-glb/assets/2-create-ec2/13.2-instance-list.png)




您已成功启动 EC2 实例。在下一个模块中，您将使用 Amazon RDS 启动 MySQL 数据库实例用于存储WordPress的内容。
