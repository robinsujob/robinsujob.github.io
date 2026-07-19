---
title: "3.5创建Linux实例并拉取UE镜像"
weight: 5
type: workshops
---
在本节中您将了解到如何创建一个带有显卡和Linux系统的Amazon EC2实例，用于演示项目的创建。

#### 1. 搜索EC2服务

请回到您的电脑，打开亚马逊云科技控制台。在页面顶部“服务”处搜索`EC2`，并点击，进入EC2控制面板

![image-20221103130510748](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-1-ec2.png)

#### 2. 进入EC2创建向导

点击橙色“启动实例”按钮，进入EC2创建向导

![image-20221103132921278](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-2-ec2-wizard.png)

#### 3. 填写EC2实例名称

本次填写`UE-Docker`

![image-20221106191305098](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/1-ec2-name.png)

#### 3. 选择 Amazon 系统映像（AMI)

选择 [Amazon 系统映像（AMI）](https://docs.amazonaws.cn/zh_cn/AWSEC2/latest/UserGuide/AMIs.html)。本次动手训练营请在 AMI 选择视图中选择`Deep Learning AMI GPU PyTorch 1.12.1 (Ubuntu 20.04)`。该AMI已经预装Nvidia及其容器化驱动。

![image-20221106191507053](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/2-ami-pytorch.png)

#### 4. 选择 EC2 实例类型

本次实验选择带有NVIDIA显卡的**g4dn.xlarge**实例，请您在搜索框中输入g4dn.xlarge, 并选择g4dn.xlarge型号。

![image-20221103145642573](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-5-type.png)

#### 5. 选择密钥对

请选择先前创建的密钥对。

![image-20221106191851425](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/3-ue-key-pair.png)

#### 6. 配置网络信息

为EC2实例配置网络信息，此处可以保持默认。这将在默认VPC中默认公有子网中为您创建实例。请点击右上角“编辑”按钮，为安全组命名。

![image-20221103153607561](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-8-vpc.png)

#### 7. 编辑安全组信息

亚马逊云科技中的安全组（Security Group）充当虚拟防火墙，描述了可以访问资源网络流量类型，这意味着您可以使用[安全组控制到资源的流量](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/ec2-security-groups.html)。

为安全组命名`UE-Docker-sg`，您需要为Linux实例创建所需的安全组入站规则。

- 添加SSH类型入站规则，允许My IP访问，用于Linux实例远程操作。
- 添加自定义TCP类型入站规则，端口为10001，允许任意IPv4访问。未来10001端口将作为演示项目的访问入口。
- 添加自定义TCP类型入站规则，端口为3578-3579，允许任意IPv4访问，以允许像素流送传输。
- 添加自定义UDP类型入站规则，端口为3578-3579，允许任意IPv4访问，以允许像素流送传输。

![image-20221106192251067](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/4-linux-sg.png)

![image-20221109224156294](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/4-linux-sg-2.png)

#### 8.为实例设定存储大小

本次动手训练营建议100GB存储大小
![image-20221106192346085](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/5-linux-ebs.png)

#### 9.挂载System Manager配置文件

在高级详细信息中，选择IAM实例配置文件，选择AmazonSSMRoleForlnstancesQuickSetup。

![image-20221103180603227](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-10-iam-role.png)

#### 10. 检查实例信息并启动

检查信息，尤其是VPC、AMI、子网、安全组等信息，点击右侧橙色按钮“**启动实例**”。

![image-20221106192453650](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/6-launch-ec2.png)

#### 11.查看实例信息

点击实例ID查看启动状态。当实例状态成为“正在运行”以及“状态检查”通过，则实例成功启动。

![image-20221106192607614](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/7-instance-id.png)

![image-20221106221702646](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/7-instance-state.png)

#### 12.连接EC2实例

选中UE- Docker实例，点击页面顶部的“连接”按钮，可以看到有多种连接EC2的方式。您可以采用会话管理器或者SSH客户端的方式连接实例。

![image-20221106224923932](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/8-connect-ec2.png)

##### 选择一：通过 SSH 访问 EC2 实例

在[3.2节](/aws-workshops/glb-ue-pixel-g4dn/3-install-engine/3-1-windows-ec2/#5)中您为实例的密钥对下载了 .pem 文件。现在请找到该文件。

对于 Mac 或 Linux 用户：

1. 打开终端窗口。Mac 用户可以使用系统自带的终端程序，也可以使用自己的终端。
2. 查找您的私有密钥文件。用于启动此实例的密钥为 **UE.pem**。
3. 如有需要，运行此命令，以修改文件权限仅供您使用
````shell
chmod 400 UE.pem
````
4. 通过其公有 DNS / IP连接到您的实例，示例:

````shell
ssh -i "UE.pem" ubuntu@您EC2的IP/DNS地址
````
当您在终端中看到以下内容时，表明您已成功连接：

![image-20221106225355408](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/9-connected-ec2.png)

对于 Windows 用户：

您将需要使用
[PuTTY（适用于 Windows 的 SSH 客户端）连接到 EC2 实例](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/putty.html)。详细操作步骤请参阅本指南中的使用 PuTTY 从 Windows 连接到 Linux 实例。您需要用到先前下载的 .pem 文件，以及 EC2 实例的公有 IP 地址。

问题排查：如果您无法通过SSH连接，例如“连接被拒”或“连接超时”错误。请检查您的安全组是否允许22端口入站，来源IP是否正确。

##### 选择二：通过会话管理器（Session Manager）连接

在开始以下步骤前，请您确认您已经完成[3.1节](/aws-workshops/glb-ue-pixel-g4dn/3-install-engine/3-0-system-manager/)中的内容。若仍然无法使用会话管理器，请确认您的实例是否关联`AmazonSSMRoleForlnstancesQuickSetup`角色。

选中会话管理器的标签，点击橙色**“连接”**按钮，您应该可以看到新打开的，可以执行指令的会话窗口，代表“会话管理器”连接成功。

![image-20221106230206353](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/10-connect-session-mgr.png)

![image-20221106230304845](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/11-session-mgr-command.png)

#### 13.检查显卡驱动

输入一下指令，以检查显卡驱动

```shell
nvidia-smi
```

若与以下不一致，请检查您的AMI是否选择为带有显卡驱动的AMI。

![image-20221109221639594](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/13-check-gpu-drive.png)

#### 14.登陆Github容器仓库并拉取UE引擎镜像

在开始以下步骤前，请您确保已经完成[3.4节](/aws-workshops/glb-ue-pixel-g4dn/3-install-engine/3-3-connect-epic/)的全部内容，将EPIC账号与Github关联，并创建了Github Access Token。

您需要先准备您的Github Access Token并登陆Github容器仓库才可以下载UE镜像，请修改以下代码替换`<Github ACCESS_TOKEN>`与`<Github 账号邮箱>`为您的信息，并执行。

```shell
#以root身份执行
sudo -i 
#切换至当前用户路径
cd ~
#使用Github ACCESS_TOKEN登陆ghcr.io仓库
echo <Github ACCESS_TOKEN> | sudo docker login ghcr.io  -u <Github 账号邮箱> --password-stdin
#拉取UE引擎的基础镜像（后台执行，防止SSH断开后拉取过程中断）
nohup docker pull ghcr.io/epicgames/unreal-engine:dev-4.27 &
#观察拉取过程
tail -f nohup.out
```

![image-20221106233150484](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/12-docker-pull.png)


{{% workshop-alert type="info" %}}
整个镜像拉取过程大约持续30分钟左右，等待过程中您可以继续进行动手训练营的下一步骤。
{{% /workshop-alert %}}


若镜像拉取完成，您应看到如下信息：

![image-20221107085629701](/aws-workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-4-linux/12-docker-finish.png)
