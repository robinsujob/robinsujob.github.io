---
title: "1.2 获取IAM用户的用户密钥"
weight: 2
type: workshops
---
# 
访问密钥包含访问密钥 ID 和秘密访问密钥，用于签署对 Amazon 发出的编程请求。 仅当创建访问密钥时，您才能查看或下载秘密访问密钥。以后您无法恢复它们。不过，您随时可以创建新的访问密钥。
#
在此任务中，您将生成当前登录的IAM用户的访问密钥ID和访问密钥，用以配置堡垒，用以授予权限创建EKS集群。由于当前您的IAM用户应该拥有Administrator权限，因此不需要额外配置权限。
#
1. 打开 IAM 控制台，为 IAM 用户创建访问密钥。登录 Amazon Web Services Management Console，单击
   https://us-east-1.console.aws.amazon.com/iamv2/home?region=ap-northeast-1#/home

2. 在导航窗格中，选择 **Users（用户）**。

![img.png](/workshops/amazon-eks-global/assets/Lab1/task2/img.png)

3. 选择要为其创建访问密钥的用户的名称，您可以选择当前登录的IAM用户。然后选择 **Security credentials (安全证书)** 选项卡。

![img_1.png](/workshops/amazon-eks-global/assets/Lab1/task2/img_1.png)

4. 在 Access keys（访问密钥）部分中，选择 **Create access key（创建访问密钥）**。

![img_2.png](/workshops/amazon-eks-global/assets/Lab1/task2/img_2.png)

5. 要查看新访问密钥对，请选择 **Show (显示)**。关闭此对话框后，您将无法再次访问该秘密访问密钥。您的凭证与下面类似：

![img.png](/workshops/amazon-eks-global/assets/Lab1/task2/img_4.png)

````
    访问密钥 ID：AKIARSCTAI355X5GL6NT

    秘密访问密钥：wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
````

6. 要下载密钥对，请选择 **Download .csv file（下载 .csv 文件）**。将密钥存储在安全位置。关闭此对话框后，您将无法再次访问该秘密访问密钥。

![img_3.png](/workshops/amazon-eks-global/assets/Lab1/task2/img_3.png)

注：请对密钥保密以保护您的Amazon Web Services 账户，切勿通过电子邮件发送密钥。请勿对企业外部共享密钥，即使有来自 Amazon 或 Amazon.com 的询问。合法代表 Amazon 的任何人永远都不会要求您提供密钥。

7. 下载 .csv 文件之后，选择 **Close (关闭)**。在创建访问密钥时，预设情况下，密钥对处于活动状态，并且您可以立即使用此密钥对。


{{% workshop-alert type="success" title="恭喜您！" %}}
您已经成功获取了当前IAM用户的用户访问密钥。
{{% /workshop-alert %}}
