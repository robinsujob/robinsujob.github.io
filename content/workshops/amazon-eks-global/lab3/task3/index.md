---
title: "3.3 使用Ingress与ALB访问应用(可选)"
weight: 3
type: workshops
---
Ingress 是公开从集群外部到集群内Service的 HTTP 和 HTTPS 路由。 流量路由由 Ingress 资源上定义的规则控制。

下面是一个将所有流量都发送到同一 Service 的简单 Ingress 示例：

![image-20220915105223201](/workshops/amazon-eks-global/assets/ingress.png)

Ingress 可为 Service 提供外部可访问的 URL、负载均衡流量、终止 SSL/TLS，以及基于名称的虚拟托管。但是为了让 Ingress 资源工作，集群必须有一个正在运行的 Ingress Controller（控制器）。Ingress控制器常见的有例如[Nginx Ingress Controller](https://github.com/kubernetes/ingress-nginx)

在亚马逊云的EKS中，我们可以使用[Amazon Load Balancer Controller(负载均衡器控制器)](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/)作为Ingress控制器。

Amazon负载均衡器控制器是帮助管理Kubernetes集群的弹性负载均衡器，它可以：

- 通过配置 Application Load Balancers 来满足 Kubernetes Ingress 资源
- 通过配置 Network Load Balancers来满足 Kubernetes Service资源

***注意，在3.1节创建Service时自动创建的NLB来源于Amazon cloud provider load balancer controller，请参考：https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer***

对于部署到 1.19 或更高版本集群的新服务，我们建议您使用 2.4.3 或更高版本的 Amazon 负载均衡器控制器，而不是 Amazon cloud provider load balancer controller。 如果您的集群早于 1.19，那么我们建议您使用 2.3.1 版本的控制器。 

Amazon Load Balancer Controller是一个在 GitHub 上管理的[开源项目](https://github.com/kubernetes-sigs/aws-load-balancer-controller)。 本主题介绍如何使用默认选项安装控制器。 您可以在 GitHub 上查看控制器的完整文档。

### 将 Amazon 负载均衡器控制器部署到 Amazon EKS 集群

切换至ecsdemo-frontend的文件下操作。

```shell
cd ~/ecsdemo-frontend
```



#### 创建IAM策略与角色

1. 下载 Amazon Load Balancer Controller 的 IAM 策略，允许它代表您调用 Amazon API

````sh
curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.7/docs/install/iam_policy.json
````

2. 使用在上一步中下载的策略创建 IAM 策略，这将创建一个名为`AWSLoadBalancerControllerIAMPolicy`的策略，策略名称可以修改。

```shell
aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json
```

3. 创建 IAM OIDC Provider并与集群关联
```sh
eksctl utils associate-iam-oidc-provider --region=ap-northeast-1 --cluster=eks-cluster --approve
```

4. 创建 IAM 角色。 在 Amazon Load Balancer Controller 的 kube-system 命名空间中创建一个名为 aws-load-balancer-controller 的 Kubernetes 服务账户，并使用 IAM 角色的名称注释 Kubernetes 服务账户。

   将 ***`YOUR_ACCOUNT_ID`*** 替换为您的帐户 ID，然后运行命令。

```sh
eksctl create iamserviceaccount \
--cluster=eks-cluster \
--namespace=kube-system \
--name=aws-load-balancer-controller \
--role-name "AmazonEKSLoadBalancerControllerRole" \
--attach-policy-arn=arn:aws:iam::YOUR_ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
--approve
```

#### 安装 Amazon Load Balancer Controller

1. 安装 cert-manager 以将证书配置注入 webhook

```shell
kubectl apply \
    --validate=false \
    -f https://github.com/jetstack/cert-manager/releases/download/v1.5.4/cert-manager.yaml
```

2. 安装控制器，下载控制器配置文件。 有关控制器的更多信息，请参阅 [GitHub 上的文档](https://kubernetes-sigs.github.io/aws-load-balancer-controller/)

```sh
curl -Lo v2_4_7_full.yaml https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.4.7/v2_4_7_full.yaml
```

3. 对文件进行以下编辑，请运行以下命令以删除清单中的 ServiceAccount 部分。如果您不删除此部分，您在上一步中对服务帐户所做的修改将被覆盖。 如果您删除控制器，删除此部分还会保留您在上一步中创建的服务帐户。

```shell
sed -i.bak -e '561,569d' ./v2_4_7_full.yaml
```

4. 将文件的 Deployment spec 部分中的 ***`your-cluster-name`*** 替换为您的集群名称

```sh
sed -i.bak -e 's|your-cluster-name|eks-cluster|' ./v2_4_7_full.yaml
```

5. 执行文件

```sh
kubectl apply -f v2_4_7_full.yaml
```

6. 将 ***IngressClass*** 和 ***IngressClassParams*** manifest文件应用于集群

```sh
kubectl apply -f https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.4.7/v2_4_7_ingclass.yaml
```

7. 验证控制器是否已安装

```shell
kubectl get deployment -n kube-system aws-load-balancer-controller
```

   示例输出如下

```sh
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
aws-load-balancer-controller   1/1     1            1           84s
```

#### 部署前端应用适用于Ingress的Service 与 Ingress

1. 输入以下命令，部署Service

```shell
kubectl apply -f kubernetes/service-for-ingress.yaml
```

2. 输入以下命令，部署Ingress

```sh
kubectl apply -f kubernetes/ingress.yaml
```

3. 执行完毕后，可以打开负载均衡器控制台，看到正在预置一个Application类型的负载均衡器

   ![image-20221013183617196](/workshops/amazon-eks-global/assets/ingress-3.png)

4. 也可通过命令，验证Ingress资源是否已部署成功，输入以下命令

```sh
kubectl get ingress/ecsdemo-frontend
```

   可以看到一个ALB类型的Ingress

```sh
NAME               CLASS   HOSTS   ADDRESS                                                                         PORTS   AGE
ecsdemo-frontend   alb     *       k8s-default-ecsdemof.ap-northeast-1.elb.amazonaws.com   80      101s
```

5. 您也可以通过复制DNS名称浏览该网站。

   ![image-20221013183818253](/workshops/amazon-eks-global/assets/ingress-4.png)




{{% workshop-alert type="success" title="恭喜您！" %}}
您已经完成了Amazon Load Balancer Controller(负载均衡器控制器)的配置，并成功部署了Ingress，未来您可以通过Ingress和ALB访问您的网站
{{% /workshop-alert %}}
