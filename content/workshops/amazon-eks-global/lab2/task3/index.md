---
title: "2.3．检查资源并验证集群创建成功"
weight: 3
type: workshops
---
# 
当您等待创建集群和节点组时，您可以浏览 AWS 管理控制台以了解 eksctl 命令的结果。
#
1.	返回**亚马逊云科技管理控制台**。
2.	在**Services(服务)** 菜单上，选择 **CloudFormation**。
3.	请注意，正在创建一个名为 **eksctl-eks-cluster-cluster** 的新 CloudFormation 堆栈。eksctl create cluster 命令可利用 CloudFormation 创建 Amazon EKS 控制层面集群所需的各种资源。集群堆栈完成部署后，eksctl 实用程序将使用第二个堆栈创建您指定的 Amazon EKS 托管节 点组。
4.	选择 **eksctl-eks-cluster-cluster** 链接，然后选择 **Resources(资源)** 选项卡，以查看 eksctl 实用程序为此特定集群部署创建的所有资源的列表。
5.	您还可以从 Amazon EKS 管理控制台查看 Amazon EKS 集群部署的状态。
6.	在 **Services(服务)** 菜单上，选择 **Elastic Kubernetes Service**。
7.	如果尚未显示 Clusters(集群)页面，请从左侧列表中选择 **Clusters(集群)**。
8.	选择 **eks-cluster** 链接以显示正在创建的集群的详细信息。
9.	请注意，状态为 Creating(正在创建)或 Active(活动)。如果集群仍处于正在创建状态，您可能看不到已填充的所有可用信息。
10.	等待集群 Status(状态)更改为 **Active(活动)**。 您可能需要选择页面右上角的**refresh(刷新)** 以刷新状态。
11.	在 **Cluster configuration(集群配置)** 部分下方，选择 **Compute(计算)** 选项卡以查看与 此集群关联的节点组的详细信息。
12.	集群标记为活动后，可能不会立即显示节点组。如果没有看到，请等待一分钟，然后选择页面右 上角的**refresh(刷新)**。
13.	请注意，有一个名为 eks-nodes 的节点组，且 *Desired size(所需大小)为 3。当您运行 eksctl create cluster 命令时，指定节点组至少应包含两个节点，最多包含四个节点，所 需大小为三个节点。由于您指定了这些选项，因此 eksctl 实用程序会创建一个 Amazon EC2 Auto Scaling 组来管理节点组中的节点数。
14.	在 **Services (服务)** 菜单上，选择 **EC2**。
15.	在左侧列表中的 **AUTO SCALING** 下，选择 **Auto Scaling Groups(Auto Scaling 组)** ，选择名称以 eks 开头的组，以查看有关该组的详细信息。
16.	请注意，最小值、最大值和所需值与您为节点组指定的值相同。因为您指定了 Amazon EKS 托管 节点组，所以当节点组计算资源负载发生变化时，Amazon EKS 将使用此 Amazon EC2 Auto Scaling 组自动增加或减少节点数。
17.	返回到堡垒主机会话。
18.	等待 eksctl create cluster 集群命令完成。完成后，输出的最后一行应类似于以下内容:
````shell  
[✔] EKS cluster "eks-cluster" in "ap-northeast-1" region is ready
````
![img_1.png](/workshops/amazon-eks-global/assets/img_2.png)
注：列出的区域可能与此处显示的区域不同，具体取决于您的实验部署在哪个区域。当前我们配置的区域为**ap-northeast-1**。


19.	输入以下命令以列出 Kubernetes 节点并验证是否创建了三个节点:
````shell
kubectl get nodes
````
输出应类似于以下内容:
````shell
NAME                                                STATUS   ROLES    AGE     VERSION
ip-xxx-xxx-xxx.ap-northeast-1.compute.internal      Ready    <none>   2m32s   v1.26.4-eks-0a21954
ip-xxx-xxx-xxx.ap-northeast-1.compute.internal      Ready    <none>   2m31s   v1.26.4-eks-0a21954
ip-xxx-xxx-xxx.ap-northeast-1.compute.internal      Ready    <none>   2m31s   v1.26.4-eks-0a21954
````


{{% workshop-alert type="success" title="恭喜您！" %}}
您已成功安装了所需的命令行实用程序，并使用托管节点组部署了 Amazon EKS 集群。  
{{% /workshop-alert %}}
