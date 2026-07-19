---
title: "2.2 创建EKS集群并部署节点"
weight: 2
type: workshops
---
接下来您就可以创建您的第一个 Amazon EKS 集群。

输入以下命令以使用具有三个节点的托管节点组部署 Amazon EKS 集群。这里我们选用m5.large实例，您可以体验新一代基于x86架构的通用型EC2实例。

````shell
eksctl create cluster --name eks-cluster --nodegroup-name eks-nodes --node-type m6i.large --nodes 3 --nodes-min 1 --nodes-max 4 --managed --version 1.26 --region ap-northeast-1
````

创建新集群可能需要 10 到 15 分钟才能完成。

注：当您使用 eksctl 创建 Amazon EKS 集群时，默认情况下会创建一个新 VPC、三个公有子网和 三个新的私有子网，用于与 Amazon EKS 控制层面集群和节点一起使用。但是，您可以使用其他 命令标志来指定使用现有 VPC 和子网。有关更多信息，请参阅[Amazon EKS 联网](https://docs.aws.amazon.com/zh_cn/eks/latest/userguide/eks-networking.html)。

下表描述了您刚刚输入的命令上使用的每个标志:

| 参数/命令                      | 含义                                   |
|----------------------------|--------------------------------------|
| eksctl create cluster      | 创建新 Amazon EKS 集群                    |
| --name eks-cluster         | -name 允许为 Amazon EKS 集群指定名称          |
| --nodegroup-name eks-nodes | --nodegroup-name 用于为Amazon EKS节点组指定名称 |
| --node-type m6i.large      | --node-type 指定用于工作线程节点的实例类型          |
| --nodes 3                  | --nodes 指定在所需的自动扩展定义期间部署的节点数         |
| --nodes-min 1              |--nodes-min 设置 Amazon EC2 Autoscaling 配置中节点组的最小节点数|
| --nodes-max 4              |--nodes-max 设置 Amazon EC2 Autoscaling 配置中节点组的最大节点数|
| --managed                  |--managed 创建 Amazon EKS 托管节点组|
| --version 1.21             |--version指定要在AmazonEKS集群上部署的Kubernetes版本|
| --region                   |-region 指定要在其中部署 Amazon EKS 集群和节点组的 AWS 区域。如果不包括 --region 标志，eksctl 实用程序默认为 us-west-2 区域|



{{% workshop-alert type="success" title="恭喜您！" %}}
当前您已成功创建EKS集群。 
{{% /workshop-alert %}}


注：eksctl create cluster 命令可在 ~/.kube/config 创建配置文件，也称为 kubeconfig。 kubeconfig 包含有关 Amazon EKS 集群的详细信息，包括集群名称和身份验证方法。有关更多 信息，请参阅[集群身份验证](https://docs.aws.amazon.com/eks/latest/userguide/cluster-auth.html)。

创建EKS集群时，将用于创建集群的 IAM 角色或用户自动添加到 Kubernetes RBAC 配置中的 **system&#58;masters** 组，使其成为 Kubernetes 集群的完全管理员。在授予额外权限之前，它也是唯一能够访问集群的角色或用户。在这种情况下，堡垒主机担任的 IAM 角色是创建集群的角色。有关更多信息，请 参阅[让 IAM 用户和角色有权访问您的集群](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html)。
