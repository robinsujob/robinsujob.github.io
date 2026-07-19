---
title: "附录"
weight: 7
type: workshops
---
### 删除Amazon EKS集群
使用完 Amazon EKS 集群后，如果您不再需要该集群，应删除与其关联的资源，这样便不会产生任何不必要的费用。

在本动手实验中，我们通过**eksctl** 来创建集群，因此在使用完该集群后，我们也可以用**eksctl** 工具来删除集群。

#
请根据以下步骤清空资源：

1. 根据任务[1.3](/aws-workshops/amazon-eks-global/lab-1/task3/#task3)连接到EC2堡垒机**Bastion**。
2. 根据任务[1.4](/aws-workshops/amazon-eks-global/lab-1/task4/#task4)配置访问秘钥，您需要使用在创建EKS集群时使用的Access Key ID和Access Key以及区域。
3. 在堡垒主机会话中，输入以下命令以更改为主目录 (/home/ssm-user/或者/home/ec2-user/):
````shell
cd ~
````
4. 输入以下命令以验证您是否位于主目录中:
````shell
pwd
````
输出应为:

会话管理器：`/home/ssm-user/`

或者

SSH连接： `/home/ec2-user/`

5. 如果您没有配置任务[3.3](/aws-workshops/amazon-eks-global/lab3/task3/#task3)中应用负载均衡以及Ingress，输入以下命令以删除集群，该命令会自动删除在Cloudformation中创建的两个堆栈：

````shell
eksctl delete cluster --name eks-cluster
````

（可选）如果您配置了任务[3.3](/aws-workshops/amazon-eks-global/lab3/task3/#task3),请根据以下步骤进行删除： 

a. 列出集群中运行的所有Ingress。
````shell
kubectl get ingress --all-namespaces
````
b. 删除与Ingress有关的信息。将***`ingress-name`***替换为刚才命令返回的名称。这些Ingress前面配置了一个 Elastic Load Balancing 负载均衡器，您必须从 Kubernetes 中将其删除才能释放负载均衡器和关联资源。

````shell
kubectl delete ingress ingress-name
````

c. 使用以下命令删除集群及其关联的节点。
````shell
eksctl delete cluster --name eks-cluster
````

输出：
````shell
[ℹ]  using region ap-northeast-1
[ℹ]  deleting EKS cluster "eks-cluster"
[ℹ]  will delete stack "eksctl-eks-cluster-nodegroup-standard-nodes"
[ℹ]  waiting for stack "eksctl-eks-cluster-nodegroup-standard-nodes" to get deleted
[ℹ]  will delete stack "eksctl-eks-cluster-cluster"
[✔]  the following EKS cluster resource(s) for "eks-cluster" will be deleted: cluster. If in doubt, check CloudFormation console
````
6. 删除集群成功后，您可以在**Services(服务)** 菜单上，选择 **CloudFormation**。
    
   ![img.png](/aws-workshops/amazon-eks-global/assets/Appendix/img.png)

7. 在右侧的选项栏中选择堆栈，确认其中命名为 **eksctl-eks-cluster-cluster** 和 **eksctl-eks-cluster-nodegroup-eks-nodes** 的两个堆栈都已经被成功删除。删除成功后，您在堆栈列表中不应该再看到这两个堆栈。
    
   ![img_1.png](/aws-workshops/amazon-eks-global/assets/Appendix/img_1.png)

8. 再次点击**Services(服务)** 菜单，选择**EC2**。点击**实例（正在运行）**。示例图为宁夏区实例，您可以根据自己实际部署的区域切换。
   ![img_2.png](/aws-workshops/amazon-eks-global/assets/Appendix/img_2.png)

    ![img_4.png](/aws-workshops/amazon-eks-global/assets/Appendix/img_4.png)
9. 选择**Name**为**Bastion**的EC2实例，选择**实例状态**，点击**终止实例**。

    ![img_3.png](/aws-workshops/amazon-eks-global/assets/Appendix/img_3.png)
10. 在弹出的窗口中，选择**终止**。请注意，终止实例的操作无法撤销。

    ![img_5.png](/aws-workshops/amazon-eks-global/assets/Appendix/img_5.png)


{{% workshop-alert type="success" title="恭喜您！" %}}
您已经成功清除本次动手实验营创建的Amazon EKS相关资源。
{{% /workshop-alert %}}


---

*Contact: Windy Zhu(czhuwenj@amazon.com), Luna Lu (luhaoy@amazon.com), Robin Su(usuzhe@amazon.com),*

*Last Update: 2023/05/20*
