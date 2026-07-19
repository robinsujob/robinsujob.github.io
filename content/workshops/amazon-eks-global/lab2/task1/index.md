---
title: "2.1 安装EKS/Kubernetes命令行工具"
weight: 1
type: workshops
---
# 

1.	在堡垒主机会话中，输入以下命令以更改为主目录 (/home/ssm-user/或者/home/ec2-user/):

````shell
cd ~
````
2. 输入以下命令以验证您是否位于主目录中:
````shell
pwd
````
输出应为:

   会话管理器：`/home/ssm-user/`

或者 

   SSH连接： `/home/ec2-user/`

2.	输入以下命令以下载 Kubernetes kubectl 程序:
````shell
sudo curl --location -o /usr/local/bin/kubectl https://s3.us-west-2.amazonaws.com/amazon-eks/1.26.4/2023-05-11/bin/linux/amd64/kubectl
````

注：在本实验中，由于您将部署 1.26 版 Amazon EKS 集群控制层面，因此您需要下载 1.26 版 kubectl 实用程序。kubectl 的版本必须是高于或低于 Amazon EKS 集群控制层面版本的一个次要版本。例如，1.23 kubectl 客户端使用 Kubernetes 1.21、1.22 和 1.23 集群。

3.	 输入以下命令使 kubectl 成为可执行文件:
````shell
sudo chmod +x /usr/local/bin/kubectl
````
4.	 输入以下命令以显示 kubectl 实用程序的版本并验证其是否被正确安装:
````shell
kubectl version --short --client
````
输出应类似于以下内容:
````shell
Client Version: v1.26.4-eks-0a21954
````
5.	接下来，安装 eksctl 命令行实用程序。运行 eksctl 实用程序是在 Amazon EKS 上创建和管理 Kubernetes 集群的一种方法。您还可以使用 AWS 管理控制台。有关更多信息，请参阅本实验末 尾其他资源部分。 输入以下命令以下载和解压缩 eksctl:
````shell
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
````
6.	输入以下命令将 eksctl 移动到 /usr/local/bin 目录:
````shell
sudo mv -v /tmp/eksctl /usr/local/bin
````
注：将下载的文件移动到 /usr/local/bin 文件夹后，您便可直接使用 eksctl 命令，因为该目录已位 于 PATH 配置中。否则，每次运行下载文件时，您都必须输入完整的文件路径，或者在 PATH 配 置中创建一个新条目。

7.	输入以下命令以验证是否已安装 eksctl:
````shell
eksctl version
````

输出显示 eksctl 的版本，其版本应为 0.141.0。


{{% workshop-alert type="success" title="恭喜您！" %}}
现在您已安装创建和管理 Amazon EKS 和 Kubernetes 所需的实用程序。 
{{% /workshop-alert %}}
