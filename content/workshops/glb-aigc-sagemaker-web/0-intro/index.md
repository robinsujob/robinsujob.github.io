---
title: "0.简介与前提条件"
weight: 2
type: workshops
---
在本次动手训练营中，您将基于Amazon SageMaker和AWS Cloud 9了解到：

- 使用Amazon SageMaker Notebook实例测试、验证AIGC模型
- 部署AIGC模型至Amazon SageMaker Inference Endpoint
- 使用AWS Cloud 9调试Web应用并调用SageMaker Inference Endpoint

[//]: # (- （可选）使用会话管理器连接至SageMaker Inference Endpoint进行远程调试)

![Architecture](/workshops/glb-aigc-sagemaker-web/assets/0-intro/Architecture.png)

若您跟随本手册完成，您将会得到一个具有AIGC能力的Web应用

![image-1](/workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/14-preview.png)

![image-1](/workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/15-image.png)



---

## 前提条件

若您希望完整体验本次动手训练营，请确保您有足够的限额。

在本次动手训练营中需要的服务类型有：

- **Amazon SageMaker Notebook:** `ml.g4dn.xlarge`
- **Amazon SageMaker Inference Endpoint:** `ml.g4dn.xlarge`

#### 1. 检查 NoteBook Instance 限额
请点击链接https://ap-northeast-1.console.aws.amazon.com/servicequotas/home/services/sagemaker/quotas

在搜索框中输入`ml.g4dn.xlarge for notebook instance usage`

若您 ml.g4dn.xlarge for notebook instance usage 行，第二列已应用的配额值为0，请继续以下步骤

**提高限额**: 选中`ml.g4dn.xlarge for notebook instance usage`，点击右上角橙色按钮“请求增加配额”

![image-20221208190636993](/workshops/glb-aigc-sagemaker-web/assets/0-intro/4-notebook_request_qupta.png)

**填写提升限额**: 请在输入框中输入您期待的限额，例如“1”。填写完毕后，点击橙色“请求”按钮提交。

![image-20221208190636993](/workshops/glb-aigc-sagemaker-web/assets/0-intro/5-notebook-input_qupta.png)


{{% workshop-alert type="info" %}}
提交完成您也可以联系您的销售代表，帮助您跟踪限额提升进度。
{{% /workshop-alert %}}


#### 2. 检查 SageMaker Endpoint 限额
请点击链接https://ap-northeast-1.console.aws.amazon.com/servicequotas/home/services/sagemaker/quotas

在搜索框中输入`ml.g4dn.xlarge for endpoint usage`

若您的限额如图所示,在ml.g4dn.xlarge for endpoint usage行第二列若为0，请继续以下步骤

![image(1)](/workshops/glb-aigc-sagemaker-web/assets/0-intro/1-sevice-quota-check.png)

**提高限额**: 选中`ml.g4dn.xlarge for endpoint usage`，点击右上角橙色按钮“请求增加配额”

![image-20221208190305257](/workshops/glb-aigc-sagemaker-web/assets/0-intro/2-request-quota.png)

**填写提升限额**: 请在输入框中输入您期待的限额，例如“1”。填写完毕后，点击橙色“请求”按钮提交。

![image-20221208190636993](/workshops/glb-aigc-sagemaker-web/assets/0-intro/3-input-quota.png)


{{% workshop-alert type="info" %}}
提交完成您也可以联系您的销售代表，帮助您跟踪限额提升进度。
{{% /workshop-alert %}}
