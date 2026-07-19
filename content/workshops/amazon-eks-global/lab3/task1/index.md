---
title: "3.1 部署单节点应用程序"
weight: 1
type: workshops
---
在该任务中，您将在集群容器上部署一个单节点应用。示例应用程序文件已经事先上传到Amazon S3存储桶中，因此您只需要根据以下步骤下载应用程序文件存储库，并通过 **kubectl apply** 命令部署应用。
### 下载应用程序文件存储库

1. 在堡垒主机会话中，输入以下命令以更改为主目录 (/home/ssm-user/ 或者/home/ec2-user):

````shell
cd ~
````

2. 输入以下命令从Amazon S3存储桶下载示例应用程序文件的存储库: 

````shell
wget -O ecsdemo-frontend.zip /workshops/amazon-eks-global/assets/code/ecsdemo-frontend.zip
wget -O ecsdemo-crystal.zip /workshops/amazon-eks-global/assets/code/ecsdemo-crystal.zip
wget -O ecsdemo-nodejs.zip /workshops/amazon-eks-global/assets/code/ecsdemo-nodejs.zip
````

3. 解压示例应用程序文件存储库：

````shell
unzip ecsdemo-frontend.zip
unzip ecsdemo-crystal.zip
unzip ecsdemo-nodejs.zip
````

### 部署微服务应用程序NodeJS后端

1. 接下来，您可以使用 kubectl 部署示例微服务应用程序的 **NodeJS** 后端部分。 输入以下命令以导航到 ecsdemo-nodejs 文件夹，该文件夹是您下载的存储库的一部分，并
    包含 YAML 格式的配置文件:
````shell
cd ~/ecsdemo-nodejs
````

2. 输入以下命令以使用 kubectl 从 **deployment.yaml** 文件中为示例应用程序的 **NodeJS** 后端 API 组件创建 Kubernetes 部署资源:
````shell
kubectl apply -f kubernetes/deployment.yaml
````

输出应声明部署已创建，类似于以下内容:

````shell
sh-4.2$ kubectl apply -f kubernetes/deployment.yaml 
deployment.apps/ecsdemo-nodejs created
````

3. 输入以下命令以使用 kubectl 从 **service.yaml** 文件中为示例应用程序的 **NodeJS** 后端创建 Kubernetes 服务:
````shell
kubectl apply -f kubernetes/service.yaml
````

输出应声明服务已创建，类似于以下内容:

````shell
sh-4.2$ kubectl apply -f kubernetes/service.yaml 
service/ecsdemo-nodejs created
````
4. 输入以下命令以监视部署的进度并验证部署是否成功完成: 
````shell
kubectl get deployment ecsdemo-nodejs
````

输出应类似于以下内容:
````shell
sh-4.2$ kubectl get deployment ecsdemo-nodejs
NAME            READY   UP-TO-DATE  AVAILABLE  AGE 
ecsdemo-nodejs  1/1     1           1          3m58s
````
### 部署微服务应用程序Crystal后端

1. 接下来，您应按照相同的步骤部署示例应用程序的 **Crystal** 后端 API 组件。 输入以下命令以导航到 ecsdemo-crystal 文件夹，该文件夹是您下载的存储库的一部分，并包含 YAML 格式的配置文件: 
````shell
cd ~/ecsdemo-crystal
````
2. 输入以下命令以使用 kubectl 从 **deployment.yaml** 文件中为示例应用程序的 **Crystal** 后端 API 组件创建 Kubernetes 部署资源:
````shell
kubectl apply -f kubernetes/deployment.yaml
````
3. 输入以下命令以使用 kubectl 从 **service.yaml** 文件中为示例应用程序的 **Crystal** 后端 API 组 件创建 Kubernetes 服务:
````shell
kubectl apply -f kubernetes/service.yaml
````
4. 输入以下命令以监视部署的进度并验证部署是否成功完成:
````shell
kubectl get deployment ecsdemo-crystal
````
输出应类似于以下内容:
````shell
sh-4.2$ kubectl get deployment ecsdemo-crystal
NAME              READY   UP-TO-DATE  AVAILABLE   AGE 
ecsdemo-crystal   1/1     1           1           12s
````
### 部署微服务应用程序前端

现在您可以部署示例应用程序的前端组件。

1. 输入以下命令以导航到 ecsdemo-frontend 文件夹，该文件夹是您下载的存储库的一部分， 并包含 YAML 格式的配置文件:
````shell
cd ~/ecsdemo-frontend
````
2. 输入以下命令以使用 kubectl 从 **deployment.yaml** 文件中为示例应用程序的 **frontend** 前端组件 创建 Kubernetes 部署资源:
````shell
kubectl apply -f kubernetes/deployment.yaml
````
3. 输入以下命令以使用 kubectl 从 **service.yaml** 文件中为示例应用程序的 **frontend** 前端组件创建 Kubernetes 服务:
````shell
kubectl apply -f kubernetes/service.yaml
````
4. 输入以下命令以监视部署的进度并验证部署是否成功完成: 
````shell
kubectl get deployment ecsdemo-frontend
````
输出应类似于以下内容:
````shell
sh-4.2$ kubectl get deployment ecsdemo-frontend
NAME                READY    UP-TO-DATE   AVAILABLE   AGE 
ecsdemo-frontend    1/1      1            1           9s
````

您已经完成了示例微服务应用程序的各个组件的部署，各组件均在 Amazon EKS 集群上的容器内运行! 接下来，检查 Kubernetes 部署以了解每个组件的部署方式。

### 列出所有Kubernetes部署并连接到Web应用

1. 输入以下命令以列出用于部署组件的 default 命名空间中的所有 Kubernetes 部署:
````shell
kubectl get deployments
````
输出应类似于以下内容:
````shell
sh-4.2$ kubectl get deployments
NAME              READY   UP-TO-DATE   AVAILABLE  AGE 
ecsdemo-crystal   1/1     1            1          2m29s 
ecsdemo-frontend  1/1     1            1          77s 
ecsdemo-nodejs    1/1     1            1          7m4s
````
请注意，每个组件只有一个部署。

2. 接下来，获取 ELB 的 IP 地址，以便看到操作中的应用程序。 输入以下命令以显示 ELB 的详细信息: 
````shell
kubectl get service ecsdemo-frontend -o wide
````
3. 复制 **External IP Address(外部 IP 地址)** 并将其粘贴到新的 Web 浏览器标签页中。 请注意，在前端服务的YAML文件中指定了端口为80。
````shell
xxx.elb.ap-northeast-1.amazonaws.com
````
例如：
````
http://a0aa201664bff437f80be414e3adbc60-b7236a920392f0db.elb.ap-northeast-1.amazonaws.com
````
负载均衡器可能需要几分钟时间才能开始将流量传输到前端。如果网页未加载，请等待几分钟， 然后重试。

您应该看到一个动画映像，其中显示了网络流量当前如何通过 ELB 流向您的 Amazon EKS 节点 和容器。请注意流量是如何只流向单个前端和后端的。该网页将每秒刷新几次以显示最新的流量 模式。但是，该流量模式永远不会改变，因为流量仅能流向每种类型中的一个容器。
网页将不时自动刷新以显示新的流量。 请将网页保持为打开状态，以为下一个任务做好准备。


{{% workshop-alert type="success" title="恭喜您！" %}}
当前您已成功部署单节点应用。 
{{% /workshop-alert %}}


注：在本任务中，我们使用了网络负载均衡器（Network Load Balancer），在ecsdemo-frontend的service.yaml文件中配置如下,其中设置service.beta.kubernetes.io/aws-load-balancer-type的取值为nlb。

````yaml
apiVersion: v1
kind: Service
metadata:
  name: ecsdemo-frontend
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  selector:
    app: ecsdemo-frontend
  type: LoadBalancer
  ports:
   -  protocol: TCP
      port: 80
      targetPort: 3000
````
如您需要配置应用负载均衡器（Application Load Balancer），请参考： 任务[3.3](/workshops/amazon-eks-global/lab3/task3/#task3)（可选)。

更多信息，请参阅[Kubernetes 负载均衡与服务](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#load-balancer-class)。
