---
title: "1.1 创建实验堡垒机"
weight: 1
type: workshops
---
#
在此任务中，您将创建一个Amazon Linux 2023的Amazon EC2堡垒机实例用以部署EKS集群。您在整个实验过程中都会用到该实例。
#

1.	打开亚马逊云科技管理控制台
      https://ap-northeast-1.console.aws.amazon.com/console/home?region=ap-northeast-1#
      ，这里我们选择区域为**Tokyo, ap-northeast-1**。

2.	在Services(服务)菜单上，选择**EC2**。

![img.png](/aws-workshops/amazon-eks-global/assets/Lab1/task1/img_00.png)

3.	在页面中央，选择启动实例。

![img.png](/aws-workshops/amazon-eks-global/assets/Lab1/task1/img.png)

4.	在名称一栏中，输入EC2的名称。这里我们将堡垒机命名为**Bastion**。

![img.png](/aws-workshops/amazon-eks-global/assets/Lab1/task1/img_0.png)

5. 选择AMI，默认选择 **Amazon Linux 2023 AMI (64位（x86）)** 系统映像。

![image-20230519222510372](/aws-workshops/amazon-eks-global/assets/Lab1/task1/img_1.png)

6.	选择实例类型，在本任务中我们选择**t3.medium**类型实例，您也可以根据需求选择其他实例类型。

![img_2.png](/aws-workshops/amazon-eks-global/assets/Lab1/task1/img_2.png)

7.	在密钥对部分，选择**创建新密钥对**。输入密钥对名称**BastionKey**，如果您使用Xshell等客户端进行SSH连接，在算法处请选择**ED25519**。点击创建密钥对，下载保存。
![img_3.png](/aws-workshops/amazon-eks-global/assets/Lab1/task1/img_3.png)
![img_4.png](/aws-workshops/amazon-eks-global/assets/Lab1/task1/img_4.png)

此时会自动下载私钥对文件，稍后会在任务[1.3](/aws-workshops/amazon-eks-global/lab-1/task3/#task3)中连接EC2的部分使用。

8. 网络部分配置保持默认，此处保持默认VPC，并确认启用自动分配公有IP。此处安全组默认设置为来自任何位置的SSH流量，建议您选择您当前机器的IP (My IP)作为源，并允许来自此IP的SSH流量。此处开放**22端口**让您可以使用 SSH 协议登录到 EC2 实例并进行进一步配置。

![img.png](/aws-workshops/amazon-eks-global/assets/Lab1/task1/img_5.png)

9. 确认摘要信息并点击启动实例：

![image-20230519223131838](/aws-workshops/amazon-eks-global/assets/Lab1/task1/img_7.png)

10. 选择查看所有实例。您可以看到实例中出现一台Name为**Bastion**的EC2实例。
    ![img.png](/aws-workshops/amazon-eks-global/assets/Lab1/task1/img_11.png)

{{% workshop-alert type="success" title="恭喜您！" %}}
您已经成功创建了基于Amazon EC2的堡垒机。
{{% /workshop-alert %}}
