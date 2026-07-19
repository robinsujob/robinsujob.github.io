---
title: "添加/删除（停止）实例"
weight: 6
type: workshops
---
若您在部署时预制的实例数量超出您的预期，或者不满足您的预期，您可以随时添加/或者删除（停止）您的实例。

#### 添加新实例

1. 请点击[链接](https://console.aws.amazon.com/ec2/home?#LaunchTemplates:search=stack-Name)，进入到启动模版。

   通过启动模版，您可以根据部署时的配置，快速的启动实例至所需的子网中。若没有实例，请确认当前区域，点击屏幕右上角更换区域。模版名称后缀的意义为`stack-Name-{您创建CloudFormation堆栈时输入的堆栈名称}`

2. 根据模版以及堆栈名称，选中对应的模版，点击右上角“操作” -> ”从模版启动实例“。

   您可以为您的实例选择合适的**实例类型以及存储大小**，未在下文提及的信息，请勿修改。
   ![image-20221221142001551](/aws-workshops/single-ip-with-multi-instance/assets/add-delete/launch-template.png)

3. 您可以创建您需要的实例类型

![image-20221221140720062](/aws-workshops/single-ip-with-multi-instance/assets/add-delete/instance-type.png)

4. **不需要选择密钥对（可以在没有密钥对的情况下继续）**


{{% workshop-alert type="info" %}}
密码将在启动时预制，与创建堆栈时配置的一致。
{{% /workshop-alert %}}


   ![image-20221221140549795](/aws-workshops/single-ip-with-multi-instance/assets/add-delete/key-pair.png)

5. **子网配置无需更改**，仅需选择“默认安全组”即可。

   ![image-20221221140815099](/aws-workshops/single-ip-with-multi-instance/assets/add-delete/instance-sg.png)

6. 您可以在存储配置中修改您的存储大小（最小30GB）

   ![image-20221221141059620](/aws-workshops/single-ip-with-multi-instance/assets/add-delete/instance-ebs.png)

7. **资源标签以及高级详细信息请勿修改，否则会导致无法连接。**


{{% workshop-alert type="warning" %}}
资源标签以及高级详细信息请勿修改，否则可能会导致无法连接
{{% /workshop-alert %}}


   ![image-20221221141433598](/aws-workshops/single-ip-with-multi-instance/assets/add-delete/instance-tag.png)

8. 检查信息后点击橙色按钮，启动实例。启动后可以根据[“快速开始”](/aws-workshops/single-ip-with-multi-instance/quickstart/)文档连接到您的实例。

![image-20221221141655431](/aws-workshops/single-ip-with-multi-instance/assets/add-delete/launch-instance.png)

---

#### 删除（停止）实例

点击[链接](https://console.aws.amazon.com/ec2/home?#Instances:search=:stack-Name;instanceState=running;v=3;$case=tags:true%5C,client:false;$regex=tags:false%5C,client:false)，进入EC2 Dashboard，查看现在正在运行的实例，请根据实例名称识别需要删除（停止）的实例ID。

实例名称后缀的意义为`stack-Name-{您创建CloudFormation堆栈时输入的堆栈名称}`

若没有实例，请确认当前区域，点击屏幕右上角更换区域。

选中实例，点击右上角实例状态。选择您的操作：

- 停止实例：实例关机
- 终止实例：删除实例。默认情况下，当实例终止时，Amazon EBS 根设备卷将自动删除，且无法撤销。

![image-20221221142605717](/aws-workshops/single-ip-with-multi-instance/assets/add-delete/instance-delete.png)

更多有关实例状态的有关信息请参考文档：

https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html
