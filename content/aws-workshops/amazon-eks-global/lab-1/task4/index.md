---
title: "1.4 堡垒机配置IAM用户访问秘钥"
weight: 4
type: workshops
---
# 
在此任务中，您将在堡垒机上配置 Amazon Command Line Interface (Amazon CLI) 用于与 Amazon 交互的基本设置。其中包括您的安全凭证、原定设置输出格式和原定设置 Amazon 区域。该安全凭证授予EC2堡垒机权限以创建EKS集群。
#
1. 按照任务[1.3](/aws-workshops/amazon-eks-global/lab-1/task3/#task3)连接到EC2实例。
2. 配置AWS CLI凭证。AWS CLI 要求您在环境中配置 AWS 凭证。在会话窗口中输入：
````shell
aws configure
````

打开您在任务[1.2](/aws-workshops/amazon-eks-global/lab-1/task2/#task2)中下载的.csv文件，复制表中的**Access key Id**和**Secret access key**配置如下：

![img.png](/aws-workshops/amazon-eks-global/assets/Lab1/task4/img.png)

会话框中输入如下：

      AWS Access Key ID: [Access Key ID in .csv]
      AWS Secret Access Key: [Secret access key in .csv]
      Default region name: ap-northeast-1
      Default output format: json


{{% workshop-alert type="success" title="恭喜您！" %}}
当前您已成功在EC2堡垒机上配置安全凭证。 
{{% /workshop-alert %}}


您将在[任务二](/aws-workshops/amazon-eks-global/lab2/)中继续完成EKS集群的创建与部署。
