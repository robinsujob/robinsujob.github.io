---
title: "3.3在Windows实例中安装显卡驱动以及UE引擎"
weight: 3
type: workshops
---
在本节中您将连接到上一节创建的Windows EC2实例上，并在Windows系统中安装显卡驱动以及UE引擎。

#### 1.连接

选中UE-Windows实例，点击页面顶部的“连接”按钮，您可以看到有多种连接EC2的方式，请选择**RDP客户端**的连接方式。

![image-20221103215328809](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/1-connect.png)

![image-20221103220749365](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/1-rdp.png)

#### 2.获取初始登录密码

初始密码获取，请点击“获取密码”。

![image-20221103222805065](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/2-gain-pwd.png)

准备好您在上一节创建实例时下载的pem密钥对，并上传，随后点击右下角橙色“解密密码”按钮，您将获得初始的登录密码，并记录该密码（*建议登录后修改该密码*）

![image-20221103223219544](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/2-upload-pem.png)

#### 3.连接方式至EC2

- ##### 使用RDP连接

如果您是Windows用户，您可以直接使用Windows远程桌面客户端连接。

![image (1)](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/3-win-rdp.png)

如果您是Mac用户，您可以使用[Microsoft Remote Desktop](https://apps.apple.com/app/microsoft-remote-desktop/id1295203466?mt=12)连接。

![image-20221103222256202](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/3-mac-remote-desktop.png)

**连接地址为Public DNS，用户名为Administrator。**

![image-20221103222519148](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/3-pulicdns-username.png)

随后您可以使用**连接地址、用户名和密码**登录。

- ##### 使用Fleet Manager连接

若您没有远程桌面客户端，或您在使用RDP客户端连接出现障碍时，您也可以使用Fleet Manager方式连接，这将会通过浏览器访问您的Windows实例。在开始以下步骤前，请您确认您已经完成[3.1节](/aws-workshops/glb-ue-pixel-g4dn/3-install-engine/3-0-system-manager/)中的内容。若仍然无法使用Fleet Manager，请确认您的实例是否关联`AmazonSSMRoleForlnstancesQuickSetup`角色。

![image-20221103231414690](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/4-fleet-mgr.png)

请使用用户凭证方式验证，并输入**用户名和密码**，并点击右下角橙色“连接”按钮

![image-20221103233456775](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/4-connect-fleet.png)

您将看到如下界面，您可以点击右上角全屏按钮，全屏化该页面。

![image-20221103233957920](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/4-full-screen.png)


{{% workshop-alert type="info" %}}
以下操作将在Windows EC2实例上操作
{{% /workshop-alert %}}


#### 4.下载并安装NVIDIA显卡驱动

在连接的Windows EC2实例中，打开Edge浏览器，复制并输入以下网址：

```api
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html
```

下载NVIDIA显卡驱动，保持默认，并安装

![image-20221104000734092](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/5-install-gpu.png)

![image-20221104001340348](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/5-install-gpu-2.png)

#### 5.下载并安装EPIC客户端

在EC2实例中，打开Edge浏览器，复制并输入以下网址

```api
https://www.epicgames.com/site/zh-CN/home
```

点击右上角，**获取EPIC GAMES客户端**并安装。

![image-20221103234424721](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/6-install-epic.png)

#### 6.运行EPIC客户端并登录

点击Sign in with Epic Games，输入您注册EPIC的账号信息

![image-20221104001447911](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/7-login-epic.png)

切换EPIC语言为中文，点击右上角头像，点击Settings，在Language处，选择简体中文并重启Epic。

![image-20221104001917913](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/7-change-language.png)

#### 7.安装UE虚幻引擎

本次动手训练营将安装**UE虚幻引擎4.27.2版本**，在开始下面的步骤之前，**请确保您已经完成NVIDIA显卡驱动的安装**。

1. 点击EPIC客户端**左侧的虚幻引擎**标签
2. **进入后点击上方的标签，“库”**
3. **点击黄色+号按钮**
4. 点击版本号，**选择4.27.2版本**
5. 随后点击安装，保持默认，并安装。

![image-20221104002649146](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/8-install-ue.png)


{{% workshop-alert type="info" %}}
整个安装过程大约持续30分钟左右，等待过程中您可以继续进行动手训练营的下一步骤。
{{% /workshop-alert %}}


安装完成后界面如下：

![image-20221107090319437](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-2-install-gpu/9-install-ue-finish.png)
