---
title: "5.部署UE演示项目"
weight: 6
type: workshops
---
在本节中您将在Linux实例中部署UE演示项目，以通过PC和手机端实现UE引擎的像素流送。

本节会提供样例代码，简化您构建、部署服务过程中的步骤。


{{% workshop-alert type="info" %}}
以下操作将在Windows EC2实例上操作
{{% /workshop-alert %}}


#### 1.Fork样例代码仓库

样例代码的存放链接如下，在连接的Windows EC2实例中，请在浏览器中打开该链接。

```api
https://github.com/robinsujob/UE4-Workshop
```

点击右上角的“Fork"按键，以Fork该仓库。

![image-20221109220014886](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/1-fork-repo.png)

保持名称为默认，点击页面底部的绿色"Create Fork"按钮。Fork后您将在您的Github中看到该仓库。

Fork后请记录您的仓库地址，例如：`https://github.com/user/UE4-Workshop.git`

![image-20221109215914278](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/1-github-page.png)

该仓库包含三个主要文件，Dockerfile, docker-compose.yml, tools.sh：

- Dockerfile：使用UE官方引擎作为基本镜像，将您的UE演示项目打包至容器中作为新的镜像
- docker-compose.yml：创建STUN/TURN Server, Signalling Server, 并将Dockerfile创建的镜像作为像素流送服务。更多信息可[参考Unreal Engine文档](https://docs.unrealengine.com/4.27/zh-CN/SharingAndReleasing/PixelStreaming/Hosting/#stun%E5%92%8Cturn%E6%9C%8D%E5%8A%A1%E5%99%A8)。其架构如下：

![img](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/2-stun-turn-architecture.png)

- tool.sh: 通过Tool文件，快速帮您构建镜像、开启或者关闭像素流送服务

#### 2.修改Dockerfile文件

打开Dockerfile文件，点击右上角“🖌️”，修改相应的Dockerfile文件，将项目仓库地址、项目名称修改为您的演示项目。

![image-20221109211838825](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/3-edit-dockerfile.png)

- `<YOUR_PROJECT_GITHUB_REPO>` 修改为您在**上一节上传UE演示项目的Github仓库地址**，例如：`https://github.com/user/ue-demo-project.git`

它可以在Github项目页的右上角绿色“Code"处找到。

![image-20221109212231919](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/4-your-github-git.png)

- `<YOUR_PROJECT_NAME>`**共四处**，修改为您的uproject的名字，例如`MyFirstPersonProject`

![image-20221109212513342](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/5-your-project-name.png)

修改完毕后的Dockerfile，**样例代码**如下：

![image-20221109212706969](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/6-edited-dockerfile.png)

点击页面底部绿色“Commit changes“提交修改。


{{% workshop-alert type="success" %}}
至此在Windows EC2实例上的操作已完成。您将在Linux EC2实例进行UE引擎容器化以及部署
{{% /workshop-alert %}}


***


{{% workshop-alert type="info" %}}
以下操作将在Linux EC2实例上操作
{{% /workshop-alert %}}


#### 3.连接到Linux EC2实例

请您连接到你的Linux EC2实例，如何连接可以参考[3.3节](/workshops/glb-ue-pixel-g4dn/3-install-engine/3-4-ubuntu-ec2/#12.ec2)的内容。

连接后执行以下命令，以管理员身份进行运行并切换至用户根路径下：

```shell
sudo -i
cd ~
```

#### 4.安装docker-compose

安装docker-compose，且版本需要1.27以上才支持nvidia GPU。首先安装docker-compose 1.29.2，请执行以下指令：

```shell
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose version
```

结果如下：

![image-20221109222445192](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/7-docker-compose.png)

#### 5. 克隆修改后的样例代码

执行以下代码，克隆您修改后的样例代码

```shell
git clone <YOUR_SAMPLE_UE_WORKSHOP_REPO>
cd UE4-Workshop
```

您修改后的样例代码应该为本节第一步中Fork后，复制的仓库地址。

#### 6. 构建UE演示项目镜像

在构建之前，请您执行以下代码，以验证UE引擎镜像是否拉取完毕：

```shell
docker pull ghcr.io/epicgames/unreal-engine:dev-4.27
```

若如图所示，则已经拉取完毕，否则还需等待：

![image-20221109222746862](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/8-image-validation.png)

请执行以下指令，构建您的UE演示项目镜像

```shell
./tools.sh build
```

这将帮您构建一个包含您演示项目的UE镜像，构建过程大约需要3分钟。构造完成后的结果如图所示。

![image-20221109223412953](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/9-create-image.png)

#### 7.运行UE演示项目镜像

请使用以下指令，**运行**您的UE演示项目镜像

```shell
./tools.sh start
```

![image-20221109225050763](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/10-run-image.png)

请打开您的浏览器，输入命令行中的地址即可体验您的UE演示项目！若您无法访问请检查您的Linux安全组配置，参考[3.5节](/workshops/glb-ue-pixel-g4dn/3-install-engine/3-4-ubuntu-ec2/#7)。

如果您需要体验其它项目，请使用以下指令，**停止**您的UE演示项目镜像，并使用新的UE演示项目进行构建。

```shell
./tools.sh stop
```


{{% workshop-alert type="success" %}}
恭喜您！Have Fun！🎉🎉🎉
{{% /workshop-alert %}}


![image-20221109225008755](/workshops/glb-ue-pixel-g4dn/assets/5-deploy-project/11-play-project.png)
