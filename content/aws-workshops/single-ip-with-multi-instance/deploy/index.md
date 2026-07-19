---
title: "环境部署"
weight: 2
type: workshops
---
部署方式采用CloudFormation一键部署，通过CloudFormation创建符合架构设计的VPC以及对应实例。用户可以通过CloudFomation预制需要部署的Windows实例的数量、实例类型、初始操作系统密码以及中英文版本的操作系统。

*注：Windows操作系为Windows Server 2022*

#### 1. 下载部署文件

[Windows Server 2022 (Chinese)](/aws-workshops/single-ip-with-multi-instance/assets/code/new-template-cn.json)

[Windows Server 2022 (English)](/aws-workshops/single-ip-with-multi-instance/assets/code/new-template-en.json)

#### 2.确认部署区域并上传文件

请点击[链接](https://console.aws.amazon.com/cloudformation/home?#/stacks/create)，快速进入创建模版界面

默认将在美国东部 (弗吉尼亚北部)us-east-1区域部署，若不是您希望部署的区域，请点击右上角更换区域。确认完毕后点击下一步。

![image-20221220201904387](/aws-workshops/single-ip-with-multi-instance/assets/deploy/region.png)

选择“上传模版文件”，并选择在第一步下载的部署文件。完成后点击下一步，进入到配置堆栈的详细信息。

![image-20221229152629072](/aws-workshops/single-ip-with-multi-instance/assets/deploy/upload-cfn.png)

#### 3. 配置堆栈详细信息

可以通过以下配置项，配置例如需要启动的Windows实例的数量、实例类型、磁盘大小、初始操作系统密码等。

**堆栈名称可以填写您可以识别的名称，例如店铺名**，确认完毕后点击下一步。

初始操作系统密码可在登录后修改。

![image-20221221112854322](/aws-workshops/single-ip-with-multi-instance/assets/deploy/deploy-config.png)

#### 4. 部署堆栈

在配置堆栈选项无需进行配置，点击下一步进入审核页面。

在页面底部，请勾选：**我确认，AWS CloudFormation 可能创建具有自定义名称的 IAM 资源**

该CloudFormation脚本将会创建部分IAM资源，未来将利用这些资源通过System Manger连接Windows实例。

确认完毕后，点击下一步创建。

![image-20221220203841853](/aws-workshops/single-ip-with-multi-instance/assets/deploy/confirm-deploy.png)

**该CloudFormation将会为您创建：**

- 一个VPC：包含一个公有子网、一个私有子网和一个NAT网关
- 根据您在堆栈配置中填写的实例类型、初始化密码的启动模版（Launch Template）
- 根据您在堆栈配置中请求数量的实例
- 符合最小权限原则的IAM Role、IAM User以及Access key ID/ Secret access key用于通过会话管理器隧道连接实例

#### 5.检查创建结果

堆栈创建成功后，堆栈应会出现`CREATE_COMPLETE`字样。

![image-20221220205246576](/aws-workshops/single-ip-with-multi-instance/assets/deploy/deployed.png)


{{% workshop-alert type="warning" %}}
以下信息非常重要，请妥善记录并保管
{{% /workshop-alert %}}


进入创建完成的堆栈，请点击至“输出”，**记录以下三项信息**。该信息将用于通过System Manger连接Windows实例。

![image-20221221114631771](/aws-workshops/single-ip-with-multi-instance/assets/deploy/output.png)
