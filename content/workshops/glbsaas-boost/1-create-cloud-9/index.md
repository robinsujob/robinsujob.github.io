---
title: "1. 使用Cloud9安装Saas Boost"
weight: 3
type: workshops
---
在本节中，您将创建一个 Cloud9 环境则并使用亚马逊云科技 Cloud9 来安装 SaaS Boost。

SaaS Boost 在安装过程中使用了一些工具与技术。您需要为您的操作系统安装和配置以下每个先决条件（如果尚未安装）：

- Java 11 [Amazon Corretto 11](https://docs.aws.amazon.com/corretto/latest/corretto-11-ug/downloads-list.html)
- [Apache Maven](https://maven.apache.org/download.cgi) (参见[安装说明](https://maven.apache.org/install.html))
- [AWS Command Line Interface version 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [Git](https://git-scm.com/downloads)
- [Node 14 (LTS)](https://nodejs.org/download/release/latest-v14.x/)
- [Yarn](https://classic.yarnpkg.com/en/docs/install)

如果您无法或不希望在本地计算机上安装所有必备组件，则可以使用亚马逊云科技 Cloud9 实例来安装 SaaS Boost。

亚马逊云科技Cloud9 是一种基于云的集成开发环境  (IDE)，您只需要一个浏览器，即可编写、运行和调试代码。它包括一个代码编辑器、调试程序和终端，并且预封装了适用于  JavaScript、Python、PHP 等常见编程语言的基本工具以及AWS CLI与Git，您无需安装文件或配置开发计算机，即可开始新的项目。

### 1. 登陆亚马逊云科技控制台

您将在亚马逊云科技的 **美国东部 (弗吉尼亚北部)** 区域完成本次动手训练营。请点击控制台右上角，选择您的区域。

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/0-region.png)

或通过以下链接登录至亚马逊云科技管理控制台： <https://us-east-1.console.aws.amazon.com/console/home?region=us-east-1> 

确保当前区域为**美国东部 (弗吉尼亚北部), us-east-1**。

### 2. 进入Cloud9服务

在查找服务处搜索 Cloud9，或点击[链接](https://us-east-1.console.aws.amazon.com/cloud9control/home?region=us-east-1#/product)进入Cloud9控制面板。

![image-1](/workshops/glbsaas-boost/assets/1-create-cloud-9/1-cloud9.png)

### 3.创建 Cloud9 环境

点击页面橙色”创建环境“按钮。

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/2-create-env.png)

在 创建环境 界面中，为您的 Cloud9 环境分配一个账户内唯一且符合命名要求的名称。可以命名：**SaaS-Boost-Installer**

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/3-cloud9-name.png)

使用 Amazon Linux 2 和具有至少 4GB RAM 的实例类型创建 AWS Cloud9 环境。例如，选择**其他实例类型**然后选择 **T3 medium**  。 

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/4-choose-instance.png)

其他选项保持默认，点击页面底部右下角橙色**创建按钮**。环境的创建将花费1-2分钟的时间。

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/5-create-instance.png)

### 4.进入Cloud9环境

在Cloud9的**环境**列表里，点击 **打开** 进入IDE环境。

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/6-open-env.png)

进入后的界面如图所示。

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/7-show-env.png)

### 5.准备SaaS Boost的安装环境

Cloud9 环境默认有 10GB 的磁盘空间，没有足够的磁盘空间来运行 SaaS Boost 安装程序。 调整 Cloud9 环境的大小（建议至少 20GB）。 请执行以下脚本，扩展Cloud9磁盘大小。

```shell
cd ~/environment
wget /workshops/glbsaas-boost/assets/code/resize.sh
sh resize.sh 20
df -h
```

运行后可以查看磁盘大小，是否为20GB。

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/8-cloud9-size.png)

检查完毕后，运行以下命令进行环境准备：

```shell
#克隆 SaaS Boost git 存储库： 
git clone https://github.com/awslabs/aws-saas-boost.git ./aws-saas-boost
#我们需要更新的 Apache Maven 版本。要安装更新的版本，请运行以下命令： 
sudo wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
sudo sed -i s/\$releasever/6/g /etc/yum.repos.d/epel-apache-maven.repo
sudo yum install -y apache-maven
#将默认 Java 版本设置回 Amazon Corretto 11（两者都选择选项 1） 
echo -e "1\n" > selectJava.data
sudo alternatives --config java < selectJava.data
sudo alternatives --config javac < selectJava.data
#安装jq用于构建演示程序
sudo yum install jq -y
```

### 6. 运行SaaS Boost 安装脚本

获取自动化参数脚本，您需要填写您的邮件地址用于接收SaaS Boost的用户名密码的邮箱地址，脚本会帮助您初始化SaaS Boost用于本次动手训练营的安装参数。

```shell
cd ~/environment/aws-saas-boost
wget /workshops/glbsaas-boost/assets/code/init-install.sh
sh init-install.sh
```

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/9-input-email.png)

执行安装步骤。

```shell
./install.sh < saas-boost-init.data
```

安装脚本将自动化的为您执行，该安装步骤将以workshop为SaaS Boost的环境名称，以Cognito为身份验证提供程序，不使用自定义域名以及分析模块。


{{% workshop-alert type="info" %}}
安装SaaS Boost过程大约需要30分钟
{{% /workshop-alert %}}


![](/workshops/glbsaas-boost/assets/1-create-cloud-9/10-install-procedure.png)
安装完成后的提示如图所示。

![](/workshops/glbsaas-boost/assets/1-create-cloud-9/11-install-completed.png)


{{% workshop-alert type="success" %}}
您已经完成了SaaS Boost的安装！
{{% /workshop-alert %}}




---

#### Saas Boost安装过程参考：

1. 选择安装选项，例如安装或卸载Saas Boost
2. 输入您的 SaaS Boost 目录的完整路径（点击回车键则安装在当前目录）
3. 输入 SaaS Boost 环境的名称 （例如，dev、QA、 test、 sandbox等）
4. 输入 SaaS Boost 管理员的电子邮件地址，该管理员将收到初始临时密码
5. 为 SaaS Boost 管理 Web 控制台选择身份提供者：输入 `Cognito`或者 `Keycloak`（默认 Cognito 按回车键）
6. 选择是否要为 SaaS Boost 管理 Web 控制台使用自定义域名。要使用自定义域名，您需要经过验证的 TLS (SSL) 证书、现有的 Route53 托管区域和有效的 DNS 解析。 
7. 选择是否要安装可选的分析管道和数据仓库。  这是 **可选的** ，将提供一个[Redshift ](https://aws.amazon.com/redshift)集群。  
8. 最后检查安装设置。 仔细检查您要将SaaS Boost 安装到的帐号和区域。进入 `y`继续或 `n`取消。 

---
