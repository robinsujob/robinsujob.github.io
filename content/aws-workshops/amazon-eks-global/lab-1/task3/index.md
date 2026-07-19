---
title: "1.3 连接堡垒机"
weight: 3
type: workshops
---
# 
在此任务中，您将连接到任务[1.1](/aws-workshops/amazon-eks-global/lab-1/task1/#task1)中创建的EC2实例，您可以选择以下两种方法中的任何一个进行连接。

- [通过 SSH 访问 EC2 实例](#ssh-ec2)
- [通过会话管理器 （Session Manager）访问EC2 (推荐)](#ec2())
#
### 选择一：通过 SSH 访问 EC2 实例

任务[1.1](/aws-workshops/amazon-eks-global/lab-1/task1/#task1)中您为实例的密钥对下载了 .pem 文件。现在请找到该文件。它可能位于您桌面上的下载文件夹中。

对于 Mac 或 Linux 用户：

1. 打开终端窗口。Mac 用户可以使用系统自带的终端程序，也可以使用自己的终端。
2. 查找您的私有密钥文件。用于启动此实例的密钥为 **BastionKey.pem**。
3. 如有需要，运行此命令，以修改文件权限仅供您使用
````
chmod 400 BastionKey.pem
````
4. 通过其公有 DNS / IP连接到您的实例:

    示例:
````
ssh -i "BastionKey.pem" ec2-user@您EC2的IP/DNS地址
````
当您在终端中看到以下内容时，表明您已成功连接：

![img.png](/aws-workshops/amazon-eks-global/assets/1_0.png)

对于 Windows 用户：

您将需要使用
[PuTTY（适用于 Windows 的 SSH 客户端）连接到 EC2 实例](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/putty.html)。详细操作步骤请参阅本指南中的使用 PuTTY 从 Windows 连接到 Linux 实例。您需要用到先前下载的 .pem 文件，以及 EC2 实例的公有 IP 地址。

问题排查：如果您无法通过SSH连接，例如“连接被拒”或“连接超时”错误。请检查您的安全组是否允许22端口入站，来源IP是否正确。

### 选择二：	通过会话管理器访问EC2(推荐)
会话管理器是一项完全托管的 Amazon Systems Manager 功能，可让您通过基于浏览器的交互一键式 shell 或通过 Amazon CLI 管理 Amazon EC2 实例。您可以使用会话管理器通过您账户中的实例来启动会话。启动会话后，您可以像通过任何其他连接类型一样运行 bash 命令。
当您选择会话管理器标签时，可能会看到如下提示，此时您需要在Amazon Systems Manager中进行一些配置工作：

![img.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img.png)

通过Amazon Systems Manager的“快速设置”简化会话管理器的配置。Amazon Systems Manager 是一项灵活易用的管理服务，让企业能够安全地管理在本地或亚马逊云科技中运行的工作负载。

1. 在控制台搜索**Systems Manager**，并点击，进入Systems Manager控制面板:

![img.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img_1.png)
2. 点击橙色左侧“快速设置”选项。

![img.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img_9.png)
3. 在页面右侧，确认当前区域，点击橙色“开始使用”按钮。
![img_1.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img_11.png)

4. 在第二个跳转界面点击Host Management下的创建按钮。
![img_2.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img_12.png)
5. Targets根据需要选择，region即实例所在的region，instances可以选择全部，其他可以保持默认，完成右下角橙色“创建”按钮。
![img_3.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img_13.png)
7. 返回EC2实例页面，等待大约1-2分钟左右刷新，会看到Bastion EC2实例自动分配了一个名为“**AmazonSSMRoleForInstancesQuickSetup**”的实例配置文件

![img.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img_4.png)

5. 点击页面顶部的“**连接**”按钮，选择“**会话管理器**”标签，此时应当不会出现之前的错误提示。若有，请刷新页面尝试，或者重新绑定名为“AmazonSSMRoleForInstancesQuickSetup”的角色。

![img_5.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img_5.png)

![img_6.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img_6.png)

点击橙色“**连接**”按钮。您应该可以看到新打开的，可以执行指令的会话窗口，代表“会话管理器”连接成功。

![img_7.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img_7.png)

![img_8.png](/aws-workshops/amazon-eks-global/assets/Lab1/task3/img_8.png)

注：通过会话管理器Session Manager，您可以连接到堡垒主机实例，而无需在防火墙或 Amazon Virtual Private Cloud (Amazon VPC) 安全组上打开特定端口。有关更多信息，请参阅[AWS Systems Manager Session Manager](https://docs.aws.amazon.com/zh_cn/systems-manager/latest/userguide/session-manager.html)。


{{% workshop-alert type="success" title="恭喜您！" %}}
您已经成功连接到我们的堡垒机。
{{% /workshop-alert %}}
