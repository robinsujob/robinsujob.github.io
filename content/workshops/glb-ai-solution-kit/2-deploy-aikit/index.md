---
title: "2. 部署解决方案"
weight: 4
type: workshops
---
在本模块中，您将通过Amazon CloudFormation一键部署AI Solution Kit。

#### 2.1 启动堆栈

第一步： 打开亚马逊云科技管理控制台 

https://us-west-2.console.aws.amazon.com/console 确保所在区域为**美国西部（俄勒冈州）** (us-west-2)

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/glb/Picture1.png)


第二步： 在页面顶部的搜索框搜索**CloudFormation**，并点击

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/glb/Picture2.png)

第三步： 单击橙色的“**创建堆栈**”按钮

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/glb/Picture3.png)

第四步： 在**创建堆栈**页面上，在**Amazon S3 URL**文本框粘贴下列模版文件的地址，然后选择下一步。

```shell
https://aws-gcr-solutions.s3.amazonaws.com/Aws-gcr-ai-solution-kit/v1.4.0/AI-Solution-Kit-Workshop.template
```

```
注：
【1】为了使得本次训练营的参与者能够尽可能的体验到更多的服务，本次实验的堆栈模版为定制化模版，以满足新用户配额限制的需要。
【2】当您在使用相应服务时出现超时等情况，不代表服务本身存在问题。
【3】若您在本次实验结束后需要使用解决方案的正式版本，请联系您的业务代表。
```

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/glb/Picture4.png)

第五步： 在**指定堆栈详细信息**页面，为您的解决方案堆栈分配一个账户内唯一且符合命名要求的名称。可以命名：**AI-Solution-Kit**

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/2.1/Picture5.png)

第六步： 在**参数**部分，对API的部署进行配置。

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/2.1/Picture6.png)

* 您可以选择部署API资源浏览器，并选择API网关的认证方式。**本次实验请保持默认选项**。参数解释如下：

|参数名称|默认值|描述|
|:----:|:----|:----|
|**APIExplorer**|yes|默认值为yes，部署API资源浏览器，通过可视化文档便于查看API定义与测试。详情可参见[API参考指南](https://awslabs.github.io/aws-ai-solution-kit/zh/api-explorer/)。如果选择no，则API资源浏览器中只能看到API的参考定义，而不能进行在线测试等操作。|
|**APIGatewayAuthorization**|NONE|API网关的认证方式。默认为NONE，即无权限认证方式。您还可以选择使用[IAM](https://docs.aws.amazon.com/zh_cn/apigateway/latest/developerguide/permissions.html)权限控制对API的访问。|
|**APIGatewayStageName**|prod|API网关（URI）中的第一个路径字段。详情可参见[阶段变量](https://docs.aws.amazon.com/zh_cn/apigateway/latest/developerguide/stage-variables.html)。|

第七步： 对需要部署的AI功能进行选择，本次动手训练营您将体验体验四种服务，分别为：**高阶文字识别（多语种）、自定义模板文字识别、通用物体识别、通用自然语言理解**。

上述四类服务，**在本次实验中已经默认开启，无需选择**。浏览功能后，请点击右下角橙色按钮“**下一步**”。

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/glb/Picture5.png)

第八步： 在**配置堆栈选项**页面保持默认，在页面底部右下角选择**下一步**。

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/2.1/Picture11.png)

第九步： 在**审核**页面，查看并确认设置。在页面底部，确保选中确认模板将创建Amazon Identity and Access Management（IAM）资源的复选框。并确保选中Amazon CloudFormation需要的其它功能的复选框。选择右下角橙色“**提交**”按钮。

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/2.1/Picture12.png)

第十步： 整个堆栈的创建过程预计将花费大约**十五分钟**。可以在CloudFormation控制台的**状态**列中查看堆栈的状态。创建完成后即可看到状态为**CREATE_COMPLETE**。

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/2.1/Picture13.png)

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/2.1/Picture14.png)

第十一步： 堆栈创建成功后，您可以在AI Solution Kit的堆栈输出（Outputs）标签页中通过对应键查看基于Amazon API Gateway的调用URL。

![image.png](/workshops/glb-ai-solution-kit/assets/2-deploy-aikit/2.1/Picture15.png)

在本章节中，您使用了CloudFormation部署了AI Solution Kit方案，在下一章节您将会了解到如何使用AI Solution Kit以满足您的需求。
