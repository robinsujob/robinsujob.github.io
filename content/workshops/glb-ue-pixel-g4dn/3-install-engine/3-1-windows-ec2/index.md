---
title: "3.2创建Windows实例"
weight: 2
type: workshops
---
在本节中您将了解到如何创建一个带有显卡和Windows系统的Amazon EC2实例，用于演示项目的创建。

#### 1. 搜索EC2服务

在页面顶部“服务”处搜索`EC2`，并点击，进入EC2控制面板

![image-20221103130510748](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-1-ec2.png)

#### 2. 进入EC2创建向导

点击橙色“启动实例”按钮，进入EC2创建向导

![image-20221103132921278](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-2-ec2-wizard.png)

#### 3. 填写EC2实例名称

本次填写`UE-Windows`

![image-20221103144953290](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-3-ec2-name.png)

#### 3. 选择 Amazon 系统映像（AMI)

选择 [Amazon 系统映像（AMI）](https://docs.amazonaws.cn/zh_cn/AWSEC2/latest/UserGuide/AMIs.html)。AMI 将决定新 EC2 实例上安装的基本软件，其中包括操作系统（Amazon Linux、Red Hat Enterprise Linux、Ubuntu、Microsoft Server 等）以及计算机上安装的应用程序。本次动手训练营请在 AMI 选择视图中选择Microsoft Windows Server 2022 Base。

![image-20221103145417649](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-4-ami.png)

#### 4. 选择 EC2 实例类型

实例类型是 CPU、内存 (RAM)、存储和网络容量的特定配置。本次实验选择带有NVIDIA显卡的**g4dn.xlarge**实例，请您在搜索框中输入g4dn.xlarge, 并选择g4dn.xlarge型号。

![image-20221103145642573](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-5-type.png)

#### 5. 创建或选择密钥对

创建用于登录EC2实例的密钥对，并保存。您将使用密钥对获取初始化的Windows密码，从而使您能够通过RDP协议远程访问EC2实例。

为您的实例创建新的密钥对，并为其命名。根据连接方式选择密钥类型（pem）然后，单击下载密钥对按钮，将 .pem文件下载到您的计算机上，妥善保管以便在后续实验中使用。

![image-20221103152105403](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-6-create-key.png)

![image-20221103152150324](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-7-select-key.png)

#### 6. 配置网络信息

为EC2实例配置网络信息，此处可以保持默认。这将在默认VPC中默认公有子网中为您创建实例。请点击右上角“编辑”按钮，为安全组命名。

![image-20221103153607561](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-8-vpc.png)

#### 7. 编辑安全组信息

亚马逊云科技中的安全组（Security Group）充当虚拟防火墙，描述了可以访问资源网络流量类型，这意味着您可以使用[安全组控制到资源的流量](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/ec2-security-groups.html)。

为安全组命名`UE-Windows-sg`，您需要为Windows实例创建所需的安全组入站规则。

- 添加RDP类型入站规则，允许My IP访问，用于Windows实例远程操作。
![image-20221103162854950](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-9-sg.png)

#### 8.为实例设定存储大小
本次动手训练营建议100GB存储大小
![image-20221103163203556](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-10-ebs.png)

#### 9.挂载System Manager配置文件

在高级详细信息中，选择IAM实例配置文件，选择AmazonSSMRoleForlnstancesQuickSetup。

![image-20221103180603227](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-10-iam-role.png)

#### 10. 检查实例信息并启动

检查信息，尤其是VPC、AMI、子网、安全组等信息，点击右侧橙色按钮“**启动实例**”。

![image-20221103170908513](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-12-launch.png)

#### 11.查看实例信息

点击实例ID查看启动状态。当实例状态成为“正在运行”以及“状态检查”通过，则实例成功启动

![image-20221103171312734](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-13-instance-id.png)

![image-20221103171543866](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-1-windows/3-13-instance-state.png)


{{% workshop-alert type="success" title="恭喜您！" %}}
您已经成功创建 Amazon EC2 Windows实例。
{{% /workshop-alert %}}
