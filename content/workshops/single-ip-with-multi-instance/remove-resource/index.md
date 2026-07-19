---
title: "清空环境"
weight: 7
type: workshops
---
{{% workshop-alert type="warning" %}}
清空过程将会导致您的唯一IP释放且无法找回，请您谨慎处理！
{{% /workshop-alert %}}



{{% workshop-alert type="warning" %}}
您的数据将清空且无法找回，如您还需要保留您的数据请自行备份！
{{% /workshop-alert %}}


如果您需要删除您创建的所有资源，请遵循以下步骤。

1. 终止（删除）对应堆栈的所有实例
   - 点击[链接](https://console.aws.amazon.com/ec2/home?#Instances:search=:stack-Name;instanceState=running;v=3;$case=tags:true%5C,client:false;$regex=tags:false%5C,client:false)，进入EC2 Dashboard，查看现在正在运行的实例，请根据实例名称识别需要删除（停止）的实例ID。
   - 实例名称后缀的意义为`stack-Name-{您创建CloudFormation堆栈时输入的堆栈名称}`
   - 若没有实例，请确认当前区域，点击屏幕右上角更换区域。
   - 选中实例，点击右上角实例状态，选择“终止实例”
2. 等待所有实例终止完毕，请点击[链接](https://console.aws.amazon.com/cloudformation)，进入到堆栈列表中。若没有您要删除的堆栈，请确认当前区域，点击屏幕右上角更换区域。
3. 选中需要删除的堆栈，点击右上角删除按钮，并确认删除堆栈。

![image-20221221143752346](/workshops/single-ip-with-multi-instance/assets/delete-cfn.png)

更多信息请参考：https://docs.aws.amazon.com/zh_cn/AWSCloudFormation/latest/UserGuide/cfn-console-delete-stack.html

删除CloudFormation过程中的故障排除：https://docs.aws.amazon.com/zh_cn/AWSCloudFormation/latest/UserGuide/troubleshooting.html#troubleshooting-errors-delete-stack-fails
