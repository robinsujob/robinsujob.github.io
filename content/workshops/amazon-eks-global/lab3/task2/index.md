---
title: "3.2 扩展微服务应用"
weight: 2
type: workshops
---
目前，应用程序的每个组件仅在一个容器中运行。如果该容器发生故障，则在创建替换容器之前
应用程序将不可用。为了帮助减少此类故障，您可以扩展每个部署以使用每个容器的多个副本。
在此任务中，您可以使用 kubectl scale deployment 命令扩展应用程序的前端和后端服务 ，并了解这些更改如何影响应用程序的操作。

### 扩展微服务应用程序后端

1. 在堡垒主机会话中，输入以下命令以扩展 NodeJS 和 Crystal 后端 API 部署，从而分别使用 三个容器:
````shell
kubectl scale deployment ecsdemo-nodejs --replicas=3
kubectl scale deployment ecsdemo-crystal --replicas=3
```` 
2. 输入以下命令以列出用于部署组件的 default 命名空间中的所有 Kubernetes 部署: 
````shell
kubectl get deployments
````
输出应类似于以下内容:

![img_2.png](/workshops/amazon-eks-global/assets/Lab3/img_2.png)

启动所有部署并使其处于就绪状态可能需要几分钟的时间。

请注意现在 esdemo-nodejs 和 ecsdemo-crystal 部署的 READY 列中所需容器的数量是三个。Kubernetes 现在将尝试针对这两种部署维持正在运行的容器数量。 

返回运行应用程序网页的浏览器标签页并刷新。 请注意网络流量现在如何流向多个后端容器!

### 扩展微服务应用程序前端

1. 返回到堡垒主机会话。
2.  输入以下命令以扩展前端部署，以使用三个容器:
````shell
kubectl scale deployment ecsdemo-frontend --replicas=3
````
3. 输入以下命令以列出用于部署组件的 default 命名空间中的所有 Kubernetes 部署:
````shell
kubectl get deployments
````
输出应类似于以下内容:
````shell
sh-4.2$ kubectl get deployments
NAME              READY   UP-TO-DATE  AVAILABLE   AGE
ecsdemo-crystal    3/3    3           3           8m48s 
ecsdemo-frontend   3/3    3           3           8m6s
ecsdemo-nodejs     3/3    3           3           9m16s
````
请注意，现在 ecsdemo 前端部署所需容器的数量是三个。Kubernetes 现在将尝试针对此部署维 持正在运行的容器数量。

返回运行应用程序网页的浏览器标签页并刷新。 请注意网络流量现在如何流向多个前端和后端容器!


{{% workshop-alert type="success" title="恭喜您！" %}}
您已成功向内外扩展示例应用程序的每个组件的部署。 
{{% /workshop-alert %}}
