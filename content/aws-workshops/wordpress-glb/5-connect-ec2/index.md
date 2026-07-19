---
title: "5. 连接您的EC2 实例"
weight: 7
type: workshops
---
在本模块您将了解到如何连接到EC2实例，为完成后续的配置性工作做初步的准备。

#### 5.1 连接 

选中WordPress EC2实例。点击页面顶部的“连接”按钮，您可以看到在在东京区域，提供了四种连接EC2的方式，分别是EC2 Instance Connect、会话管理器、SSH客户端和EC2串行控制台。EC2 Instance Connect、EC2串行控制台和会话管理器能够在网页上直接访问到EC2实例，SSH客户端连接使用本地终端通过密钥方式进行远程连接。这里我们介绍如何使用SSH客户端、EC2 Instance Connect和会话管理器三种方式来连接到EC2实例。

![image-8](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture8.png)

![image-9](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture9.png)

#### 5.2 通过 SSH 访问 EC2 实例

先前您为实例的密钥对下载了 .pem 文件。现在请找到该文件。它可能位于您桌面上的下载文件夹中。

- **对于 Mac 或 Linux 用户**：

     *	打开终端窗口。Mac 用户可以使用系统自带的终端程序，也可以使用自己的终端。

     *	查找您的私有密钥文件。用于启动此实例的密钥为 EC2-ap-northeast-1.pem

     *	出于安全因素考虑，SSH客户端要求私钥的权限必须为只有当前用户拥有只读权限，因此在密钥所在路径下，执行命令`chmod 400 EC2-ap-northeast-1.pem`为私钥配置适当的权限。

     *	通过其公有 DNS / IP连接到您的实例:

     *	示例: `ssh -i "EC2-ap-northeast-1.pem" ec2-user@您EC2的IP/DNS地址`


当您在终端中看到类似以下界面时，表明您已成功连接：

![image-10](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture10.png)

- **对于 Windows 用户**：
  - 您将需要使用 [使用 OpenSSH 从 Windows 连接到 Linux 实例](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/openssh.html)。详细操作步骤请参阅参考链接中“使用 OpenSSH 从 Windows 连接到 Linux 实例”。您需要用到先前下载的 .pem 文件，以及 EC2 实例的公有 IP 地址。


{{% workshop-alert type="info" %}}
问题排查：如果您无法通过SSH连接，例如“连接被拒”或“连接超时”错误。请检查您的安全组是否允许22端口入站，来源IP是否正确。
{{% /workshop-alert %}}


****

#### 5.3 使用EC2 Instance Connect连接到EC2

Amazon EC2 Instance Connect 提供了一种简单且安全的方法以使用 Secure Shell（SSH）连接到 Linux 实例。借助 EC2 Instance Connect，您可以使用 AWS Identity and Access Management (IAM) 策略和主体来控制对实例的 SSH 访问，无需共享和管理 SSH 密钥。

您可以使用 EC2 Instance Connect 通过 Amazon EC2 控制台或您选择的 SSH 客户端连接到您的实例。

1. 查找IP地址范围。EC2 Instance Connect使用特定的IP地址范围通过基于浏览器的 SSH 连接到您的实例，此IP与您本地的IP不同。因此在使用EC2 Instance Connect之前，请确保与您的实例关联的安全组允许来自EC2_INSTANCE_CONNECT的IP地址范围的入站SSH流量，这些IP地址范围与EC2部署的区域有关。请在[Amazon IP地址范围](https://ip-ranges.amazonaws.com/ip-ranges.json)中，搜索关键字`EC2_INSTANCE_CONNECT`，找到“region”为**ap-northeast-1**的IP范围并记下。如下图中所示，`3.112.23.0/29`即为亚马逊云科技东京区域用于EC2 Instance Connect的IP地址范围。![image-11](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture10.5.png)
2. 配置安全组。在EC2实例页面，选中之前创建的实例，在下方选单中点击安全标签页，点击安全组打开安全组配置。![image-11](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture10.6.png)点击“编辑入站规则”，![image-11](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture10.7.png)点击“添加规则”，新增一条新规则，类型选择`SSH`，源选择`自定义`，并输入上一步中查询到的IP范围，最后点击“保存规则”。![image-11](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture10.8.png)至此，EC2 Instance Connect具有了SSH访问EC2实例所需的网络权限。
3. 连接实例。在EC2的“连接到实例”页面，选择“使用EC2 Instance Connect进行连接”，确认Username为`ec2-user`，点击“连接”![image-11](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture10.9.png)出现类似以下界面时，连接成功。![image-11](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture10.91.png)

#### 5.4 通过会话管理器访问EC2

会话管理器是一项完全托管的 [Amazon Systems Manager](https://aws.amazon.com/systems-manager/) 功能，可让您通过基于浏览器的交互一键式 shell 或通过 Amazon CLI 管理 Amazon EC2 实例。您可以使用会话管理器通过您账户中的实例来启动会话。启动会话后，您可以像通过任何其他连接类型一样运行 bash 命令。

当您选择会话管理器标签时，可能会看到如下提示，此时您需要在Amazon Systems Manager中进行一些配置工作：

![image-11](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture11.png)

1. 通过Amazon Systems Manager的“快速设置”简化会话管理器的配置。Amazon Systems Manager 是一项灵活易用的管理服务，让企业能够安全地管理在本地或亚马逊云科技中运行的工作负载
   
   在控制台搜索Systems Manager，并点击，进入Systems Manager控制面板
   

![image-12](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture12.png)

2. 点击橙色左侧“快速设置”，在页面右侧，确认当前区域，点击橙色“开始使用”按钮

![image-13](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture13.png)

3. 在第二个跳转界面点击Host Management下的创建按钮，Targets根据需要选择，region即实例所在的region，instances可以选择全部，其他可以保持默认，完成右下角橙色“创建”按钮。

![image-14](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture14.png)

4. 返回EC2实例页面，等待大约1-2分钟左右刷新，会看到WordPress EC2实例自动分配了一个名为“AmazonSSMRoleForInstancesQuickSetup”的实例配置文件

![image-15](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture15.png)

5. 点击页面顶部的“连接”按钮，选择“会话管理器”标签，此时应当不会出现之前的错误提示。若有，请刷新页面尝试，或者重新绑定名为“AmazonSSMRoleForInstancesQuickSetup”的角色。

![image-16](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture16.png)

![image-17](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture17.png)

点击橙色“连接”按钮。您应该可以看到新打开的，可以执行指令的会话窗口，代表“会话管理器”连接成功。

![image-18](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture18.png)

![image-19](/aws-workshops/wordpress-glb/assets/5-connect-ec2/5-Picture19.png)

在本节中，您使用SSH终端或者会话连接器成功连接到了EC2实例。后面您将从 EC2 实例连接到 RDS 数据库，并为 WordPress 应用程序创建数据库用户。
