---
title: "2.2 使用OpenPose优化人物二维码"
weight: 2
type: workshops
---
在上一节您体验到了使用ControlNet并结合QR Code生成二维码，在本节中您将会了解到如何通过ControlNet的OpenPose模型与二维码结合，使用 OpenPose 相关模型来生成人体姿势并将其用作 QR 码的输入。

OpenPose 姿态检测可生成图像中角色动作姿态的骨架图，这个骨架图可用于控制生成角色的姿态动作。

例如，您可以看到以下图像是使用 QR Code 和 OpenPose 作为输入生成的。  通过一些构图技巧，您可以将观看者的焦点转移到图像的其他部分，并使二维码不那么明显。 

| ![open-pose-code](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/1-open-pose-code.png) | ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/2-girl-with-car.png) |
| ----------------------------------------------------------- | -------------------------------------------- |

```shell
(school girl:1.6, walking), (a car, side view, to left), (residential area, cherry trees)
Negative prompt: (worst quality:1.6),(low quality:1.6), (inaccurate limb:1.2),bad composition, inaccurate eyes, easynegative
Steps: 50, Sampler: Euler a, CFG scale: 7, Seed: 3408317133, Size: 900x540, Model hash: 876b4c7ba5, Model: cetusMix_Whalefall2, Clip skip: 2, ControlNet 0: "preprocessor: none, model: control_v11p_sd15_openpose [cab727d4], weight: 1.15, starting/ending: (0, 1), resize mode: Crop and Resize, pixel perfect: False, control mode: Balanced, preprocessor params: (512, 64, 64)", ControlNet 1: "preprocessor: none, model: control_v1p_sd15_qrcode_monster [a6e58995], weight: 1.7, starting/ending: (0, 1), resize mode: Crop and Resize, pixel perfect: False, control mode: Balanced, preprocessor params: (512, 64, 64)", Version: v1.4.0
```

#### 1. 数据及环境准备

本次动手训练营为您准备了样例OpenPose骨架数据以及二维码，您可以参考以下教程或者设计您的OpenPose骨架数据与二维码开始体验。

请点击以下链接下载样例数据。

| OpenPose样例数据                                             | 样例二维码                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [点击下载样例数据](/aws-workshops/glb-aigc-ami-workshop/assets/example/pose.json) *(pose.json)* | [点击下载样二维码](/aws-workshops/glb-aigc-ami-workshop/assets/example/example-qr-code.png)  *(example-qr-code.png)* |

为了叠加QR Code与OpenPose效果，您需要开启多个ControlNet Unit以叠加使用模型。要激活多个ControlNet Unit，请进入**设置标签页**。

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/3-setting.png)

在**左侧选择ControlNet**。拖动拉杆，设置需要使用的**ControlNet Unit数量，不小于2。**

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/4-set-multi-unit.png)

随后在页面顶部，点击“保存设置”，并点击“重载前端”。

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/5-reload-ui.png)

重载界面后，请在“文生图”标签页中，展开**ControlNet菜单**，检查是否展示为多个ControlNet单元。

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/6-check-result.png)

#### 2.导入骨架数据并启用OpenPose控制单元

本次动手训练营为您准备了经过设计后的OpenPose骨架数据。请跟随以下步骤导入骨架数据。

- **点击OpenPose编辑器**
- **点击加载JSON**，选中您下载的`pose.json`文件，并点击确定
- 随后您应当能看到右侧出现的骨架图，如图所示。**确认骨架图无误后**，请点击下方的 **“发送到文生图“按钮**
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/7-import-pose.png)

随后页面会自动跳转到"文生图"标签页中，若没有自动跳转，请选择在“文生图”标签页中，展开ControlNet菜单。并注意以下几个选项的配置：

- 勾选 **“启用” 按钮** ：以确保 ControlNet 在图片生成过程中生效；
- 模型选框：请选择 **“control_v11p_sd15_openpose”** 来使用ContolNet Openpose进行姿态控制；

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/8-enable-openpose.png)

您可以观察到，骨架在图片的左侧，为一个蜷缩的状态，随后您将使用提示词来生成为一个正在睡觉的女孩。

#### 3. 导入二维码并生成美化后的二维码图片

随后点击 “ControlNet Unit 1"，进入第二个ControlNet单元，以叠加使用二维码控制模型。请点击上传，选择您下载的样例二维码文件`example-qr-code.png`，并跟随以下几个选项配置ControlNet单元：

- 勾选 **“启用” 按钮** ：以确保 ControlNet 在图片生成过程中生效；
- 模型选框：请选择 **“control_v1p_sd15_qrcode_monster”** 来使用ControlNet二维码控制模型；
- 控制权重：对于叠加OpenPose使用，建议设置为**1.7**；

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/9-enable-qr-monster.png)

您可以看到，二维码的整体在图片右侧，作为一种构图技巧其目是为与骨架躯体相呼应，使得人物生成更加的自然。

在文生图配置中调整两组数值：

- 迭代步数：建议在 **30-50** 之间，默认值 20 不足以引导生成一个高质量的二维码图片

- 宽度/高度：直接从 ControlNet 发送二维码原图的宽高比至上方

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/10-set-hw.png)

我们希望骨架可以生成为一个正在睡觉且躺在木地板上的的女孩，同时以向日葵作为二维码的定位点。随后请参照以下提示词例子输入，并点击生成：

正向提示词：

```shell
(1girl:1.6, side lying sleep, on the garden, sunflowers), wooden floor
```

反向提示词：

```shell
extra hands, extra fingers, extra legs, fewer fingers, (low quality, worst quality:1.4), (bad anatomy), (inaccurate limb:1.2),bad composition, inaccurate eyes, extra digit,fewer digits,(extra arms:1.2), signature, easynegative
```

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/11-set-prompt.png)

最终生成的结果如图所示：

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/12-openpose-qrcode.png)

在本例子的设计中，我们通过与OpenPose叠加，偏移二维码等设计和构图技巧，将观看者的焦点转移到图像的其他部分，同时避开了二维码的核心区域，使得人像更加自然。

| ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/13-lying-sleep-openpose.png) | ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-2-openpose/14-openpose.png) |
| ----------------------------------------------------- | ----------------------------------------- |

如果生成的二维码不能够达到期望，可以选择微调以下几个参数，并增加生成的总批次数，不断尝试抽卡以逼近最终期望的效果：

- 提示词
- 采样方法
- OpenPose骨架的结构与位置
- ControlNet 控制权重
- ControlNet 引导介入/终止时机


{{% workshop-alert type="success" %}}
通过本篇教程，您对如何通过OpenPose来优化人物二维码有了更深入的了解。
{{% /workshop-alert %}}
