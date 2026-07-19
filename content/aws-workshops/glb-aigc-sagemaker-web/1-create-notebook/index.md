---
title: "1.创建Amazon SageMaker Notebook实例"
weight: 3
type: workshops
---
Amazon SageMaker Notebook实例是运行 Jupyter Notebook 应用程序的ML(机器学习)计算实例。SageMaker管理实例和相关资源的创建。  您可以在您的Notetbook实例中使用 Jupyter Notebook来准备和处理数据、编写代码来训练模型、或将模型部署到 SageMaker I中，以及测试或验证您的模型。

在本节中，您将开启一个Amazon SageMaker Notebook实例，导入用于运行本次动手训练营中的Jupyter Notebook代码。

#### 1. 登录亚马逊云科技控制台

您将在亚马逊云科技的**Tokyo**区域完成本次动手训练营

请通过以下链接登录至亚马逊云科技管理控制台： [https://ap-northeast-1.console.aws.amazon.com/console/home?region=ap-northeast-1# ](https://ap-northeast-1.console.aws.amazon.com/console/home?region=ap-northeast-1#)，确保当前区域为**Tokyo, ap-northeast-1**。

![](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/1-region.png)

#### 2. 进入SageMaker服务

在查找服务处搜索SageMaker，并点击。

![image-20221206191309679](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/2-sagemaker.png)

#### 3. 进入笔记本(Notebook)实例控制面板

在左侧菜单栏，点击“笔记本实例”，进入笔记本(Notebook)实例控制面板。

![image-20221206191445541](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/3-notebook.png)

#### 4. 创建笔记本实例

点击右上角橙色”创建笔记本实例“按钮。

![image-20221206210303259](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/4-create-notebook.png)

#### 5. 配置笔记本实例设置

在创建笔记本实例详情页中，配置笔记本实例的基本信息。

在这个设置中您需要配置以下4部分信息。

- 笔记本实例名称

  - 您需要为您的实例命名，例如`stable-diffusion`

- 笔记本实例类型

  - 请选择`ml.g4dn.xlarge`实例类型
  - 该类型实例搭载NVIDIA T4 Tensor Core GPU显卡，可以提供模型中所需执行浮点数计算的能力

- 平台标识符（操作系统及Jupyter Notebook版本）

  - 请选择`Amazon Linux 2, Jupyter Lab 3`

- 实例存储（卷大小）

  - 请点击展开“其他配置”选项，在卷大小中输入实例大小
  - 推荐至少75GB磁盘大小，用于存储机器学习模型

  ![image-20221206231340501](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/5-notebook-info.png)

#### 6. 配置笔记本实例权限

您需要为您的笔记本实例创建一个IAM角色，用于调用调用包括 SageMaker 和 S3 在内的其他服务。例如上传模型，部署模型等。

在IAM角色出，点击下拉列表，选择”创建新角色“。

![image-20221206232851958](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/6-notebool-create-role.png)

在弹出的配置页面中，请保持默认，并点击右下角橙色“创建角色”按钮。

![image-20221206233011796](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/6-notebool-create-role-2.png)

随后将会看到类似提示信息：

{{% workshop-alert type="success" title="成功！您已创建 IAM 角色。" %}}
[AmazonSageMaker-ExecutionRole-XXXXX](/aws-workshops/glb-aigc-sagemaker-web/1-create-notebook/#7)
{{% /workshop-alert %}}


#### 7. 检查信息，创建实例

检查先前配置的信息，确认无误后请点击右下角橙色按钮”创建笔记本实例“。

创建过程需要若干分钟，请等待。您可以点击“刷新”按钮，等待实例创建完成。

![image-20221206233822774](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/7-instance-created.png)

#### 8. 进入Jupyter Notebook

点击右侧，“打开Jupyter”。

![image-20221207101625228](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/8-open-notebook.png)

#### 9. 下载/上传Notebook文件

请打开[链接](/aws-workshops/glb-aigc-sagemaker-web/assets/code/notebook-stable-diffusion.ipynb)，下载保存Notebook代码文件。

Notebook代码是本次动手训练营的主要内容。该代码文件包含以下内容：

- 在笔记本实例中下载并测试AIGC模型文件
- 编写模型推理入口代码，打包模型文件，并上传至S3桶
- 使用代码部署模型至SageMaker Inference Endpoint

[//]: # (- （可选）使用会话管理器连接至SageMaker Inference Endpoint进行远程调试)

随后在Jupyter Notebook实例中上传下载后代码。
请点击右上角的“upload”按钮，选择刚刚下载的Notebook文件

![image-20221207112240595](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/9-upload.png)

[//]: # (![image-20221207112328656]&#40;/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/9-upload-2.png)

点击蓝色"upload"按钮，完成上传过程。

![image-20221207112457638](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/9-upload-3.png)

[//]: # (请确保上传后的文件名后缀为"ipynb"，否则请修改文件后缀名，保留"ipynb"后缀)

[//]: #
[//]: # (![image-20221207112618589]&#40;/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/10-rename.png)

上传完成后的文件如图所示，请点击该文件进入Notebook中。

![image-20221207112726571](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/11-click-notebook.png)

请确保您的Kernel是`conda_pytorch`开头。

![image-20230223113610465](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/12-kernel.png)

打开后的界面如下。

![image-20221207114114497](/aws-workshops/glb-aigc-sagemaker-web/assets/1-create-notebook/12-notebook.png)


{{% workshop-alert type="info" %}}
此后的操作您将在Jupyter Notebook中进行
{{% /workshop-alert %}}


#### Tips - Jupyter Notebook快捷键

Jupyter Notebook 有两种键盘输入模式。

1. **编辑模式**：允许在单元中键入代码或文本；此时的单元框线是绿色的。
2. **命令模式**：键盘输入运行程序命令；此时的单元框线是蓝色。

部分命令模式常用指令快捷键，更多快捷键可以在命令模式中使用“H"查看

|  按键  | 命令 | 按键 | 命令 |       按键       |         命令         |
|  :--:  | :--:  |  :--:  |  :--:  |  :--:  |  :--:  |
| **Enter** | 进入编辑模式 |   **ESC**   | 编辑模式->命令模式 | **Ctrl/⌘-Enter** |      运行本单元      |
| **Shift-Enter** | 运行本单元，选中下个单元 |    **Y**    |  单元转入代码状态  |      **M**       | 单元转入markdown状态 |
|      **A**      |     在上方插入新单元     |    **B**    |  在下方插入新单元  |     **Up/K**     |     选中上方单元     |
|   **Down/J**    |       选中下方单元       |    **X**    |   剪切选中的单元   |      **C**       |    复制选中的单元    |
|      **V**      |      粘贴到下方单元      | **Shift-V** |   粘贴到上方单元   |     **D,D**      |    删除选中的单元    |
|  **Ctrl/⌘-S**   |       保存Notebook       |   **I,I**   |  中断Notebook内核  |     **0,0**      |   重启Notebook内核   |


{{% workshop-alert type="success" %}}
请移步到Jupyter Notebook中体验您的AIGC之旅吧！
{{% /workshop-alert %}}
