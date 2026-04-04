---
slug: "art-qr-code-controlnet-stable-diffusion"
title: "借助 ControlNet 生成艺术二维码 – 基于 Stable Diffusion 的 AI 绘画方案"
date: 2023-09-01
description: "借助 ControlNet 和 Stable Diffusion 生成可扫描的艺术二维码，并结合 OpenPose 控制人物姿态，创造更具艺术感的作品。"
image: images/2-girl-with-car.png
categories:
  - AI/ML
tags:
  - Stable Diffusion
  - ControlNet
  - QR Code
  - Art
  - OpenPose
---


## 背景介绍

近年来，结合 Stable Diffusion 与 ControlNet 生成艺术二维码的技术引发了广泛关注——这类二维码不仅可以被正常扫描，同时也是视觉上令人惊艳的艺术作品。本文最初作为 AWS Workshop 的一部分开发，展示如何在亚马逊云科技基础设施上部署和使用 Stable Diffusion。

本文将分享使用 Stable Diffusion 的实战经验，以及通过 ControlNet 生成艺术二维码的最佳实践。

我们将以 QRCode 作为 ControlNet 的输入，使 QRCode 数据点融入到艺术图像中，同时仍然可以被 QRCode 阅读器扫描。借助这项技术，您可以将任何二维码转化为独特的艺术作品，以一种全新的方式来表达和传递信息。以下为几张图片案例：

![示例1](images/sample1.jpg)
![示例2](images/sample2.jpg)
![示例3](images/sample3.jpg)

## Stable Diffusion 实战技巧

古语有云：'万事开头难'，'致广大而尽精微'。这两句话恰好对应了使用 Stable Diffusion 时最常见的两大挑战：第一，如何选择合适的提示词策略，以生成符合预期的图像；第二，如何对图像细节进行精细调整，使最终输出达到可用于生产的质量标准。

基于我们帮助用户使用 Stable Diffusion 的经验，我们总结了以下最佳实践供参考。

### 提示词工程

随着 Stable Diffusion 版本不断迭代，AI 对语义的理解越来越接近"常识"之后，对提示词（Prompts）的要求也会越来越高。很多提示词上的误区有时会对绘图产生反作用。

#### Prompt 的基本概念

提示词分为**正向提示词**（positive prompt，告诉 AI 需要什么）和**反向提示词**（negative prompt，告诉 AI 不需要什么）。

#### Prompt 的误区

- Prompt 在于精确，不在于数量；用最简短的单词阐述画面，比自然语言要更有效。
- 提升质量的描绘词绝不是无脑堆砌、越多越好。
- 经常出现的起手式："masterpiece"、"best quality" 等，在 NovelAI 时代是有意义的，因为当时训练模型时大量使用了这些词汇来对图像进行评价；但在如今，经过 Civitai 上模型作者们不断重新炼制模型，这些提示词已经很难在生图结果中展现应有的作用。

#### 调整提示词的权重

- 词缀的权重默认值都是 1，从左到右依次减弱
- 提示词权重会显著影响画面生成结果
- 通过小括号 + 冒号 + 数字来指定提示词权重，写法如 `(one girl:1.5)`

#### 注意提示词的顺序

- 景色 Tag 在前，人物就会小；人物 Tag 在前，人物会变大或半身
- 选择正确的顺序、语法来使用提示词，以更有效地渲染期望的画面

#### Prompt 中的 Emoji

- Prompt 支持使用 emoji，且表现力较好
- 对于特定的人脸表情或动作，可通过添加 emoji 来达到效果
- 为了防止语义偏移，优先考虑 emoji，减少不必要的复杂语法

#### 视角 Prompt 推荐

| 参数 | 说明 |
|------|------|
| extreme closeup | 面部特写 |
| close up | 头部 |
| medium close up | 证件照 |
| medium shot | 半身 |
| cowboy shot | 不带腿 |
| medium full shot | 不带脚 |
| full shot | 全身 |

### 图片优化

很多时候我们生成了一张差强人意的图片，希望对这个结果进行进一步的优化，但往往不知道从何下手。这时您或许可以参考以下图片参数调优的最佳实践：

#### 哪些参数需要调整

- **CFG Scale**：图像与提示词的相关度。该值越高，提示词对最终生成结果的影响越大。
  - CFG 2-6：有创意，但可能太扭曲，适合简短提示词。
  - CFG 7-10：推荐用于大多数提示，创意与引导的良好平衡。
  - CFG 10-15：详细且清晰的提示时使用。
  - CFG 16-20：除非提示非常详细，否则通常不推荐。可能影响一致性和质量。
  - CFG >20：几乎不可用。
- **Sampling Steps**：迭代步数越多，每一步图像的调整越小、越精确，但会成比例增加生成时间。对于大部分采样器，迭代越多次效果越好，但超过 50 步后收效甚微。
- **Sampling method**：不同的采样方法有不同的最佳迭代步数，在进行对比时需要综合考虑。
  - Euler a：富有创造力，适合快速检查 prompt 效果。
  - DPM2 a Karras：适合真实模型，30 步后难以控制。
  - DPM++ 2M Karras：高步数表现优异，细节更丰富。
  - DDIM：收敛快，但效率相对较低，因为需要很多 step 才能获得好的结果，适合在重绘时候使用。
  - 不同模型与采样方法搭配出的结果各不相同，建议使用 X/Y/Z 图表进行对比。
- **Seed**：随机种子对构图的影响巨大，是 SD 生图随机性的主要来源。固定种子后，相同的提示词和参数可以多次生成（几乎）相同的图像。确定好构图后，固定种子再对细节进行打磨是最合适的做法。

#### 如何对比寻找最佳参数

利用 X/Y/Z 图找最佳参数：通过使用 X/Y/Z 图，我们可以很清晰地对比不同参数下的结果，快速定位合适的参数范围，进行进一步的生成控制。

![X/Y/Z 图对比](images/image4.jpg)

#### 图片尺寸优化

- 图片质量并不直接与图像尺寸挂钩。
- 但尺寸在一定程度上影响了主题内容——竖图对应人像、横图对应风景、小分辨率对应贴纸等，不同尺寸隐含了不同的图像类别。
- 当出图尺寸太宽时，图中可能会出现多个主体。
- 1024 以上的尺寸可能会出现不理想的结果，且对显存压力较大。推荐使用小尺寸分辨率 + 高清修复。

#### 优化多人物 / 宽幅单人物的生成

- 单纯使用 txt2img 无法有效指定多人物情况下的特征。
- 推荐方案：制作草稿 + img2img 或 ControlNet。
- 宽幅画作 + 单人物生成，最好打草图进行色彩涂抹以确定画面主体；或使用 ControlNet 的 OpenPose 做好人物骨架。
- 多人物场景，建议使用 ControlNet 的 OpenPose 来指定人物数量；该方案也适合画同一人物的三视图。

#### 进行手部修复

将图片送入 img2img inpaint，使用大致相同的提示词，将关于"手"的提示放在前面，根据希望手部特征变动多少来设置重绘幅度（如果只希望手更完整，调至 0.25 以下），保持步数和 CFG 与 txt2img 相同。找到一个满足期望的手部参考图，借助 ControlNet 的 Canny 或 OpenPose_hands 等预处理器 + 模型，结合 inpaint 操作，能实现更精确的手部控制。

#### 进行面部修复

在绘制人物主体较小的图片时，经常会出现面部崩坏的情况。尤其是本文之后会介绍的生成艺术二维码流程，人物的面部经常会因为二维码码点的存在而崩坏。对面部的重绘，更推荐使用 **ADetailer** 插件实现。该插件使用 YOLO 算法对图片中的物体进行识别，我们设定其识别人物面部，并提供面部重绘的提示词和模型，在相应位置进行局部重绘，完成面部修复。ADetailer 同样支持手部识别与修复，也可在局部重绘中引用 LoRA 模型。

![ADetailer 面部修复](images/image5.jpg)

## 借助 ControlNet 生成艺术二维码

### 第一步：优化二维码

二维码是一种借助特定几何图形分配，在二维空间上分布的、黑白相间的、记录数据符号信息的图形。二维码有多种不同的编码方式，此处我们采用通用度最高的编码方式：QR Code。

输入的二维码是借助 SD 生成艺术二维码过程中最重要的部分之一。我们主要关心以下两个特点：

![QR Code 结构](images/image6.jpg)

**1. 二维码中包含的信息量**

无论二维码采用何种编码方式，承载的字符信息越多，二维码在视觉上呈现的黑白结构就越复杂。复杂的结构会极大地限制艺术创意的发挥。因此首先要想办法精简二维码中包含的字符长度。

对于最广泛的应用场景——网页链接，需要先对链接进行缩短。市面上的链接缩短工具有很多，可自由选择。需要注意的是，在中国大陆使用时，请选择已备案域名的平台，否则链接可能会被微信、浏览器等屏蔽。

![链接长短对比](images/image7.jpg)

**2. 二维码的呈现形式**

随着技术发展，二维码不仅只支持黑白方块状的图案样式，定位点和码元都支持多样化的呈现。

在实际操作中，可以尝试多种不同的码点形式，以使得生图效果符合预期。下图展示了不同的二维码形式对最终效果图的影响：

![不同码点形式](images/image8.jpg)
![不同二维码形式对比](images/image9.jpg)

生成参数：

```
Prompt: mountain, green grassland, sky, cloud, bird, blue sky, no human, day, wide shot, flying, border, outdoors, white bird, scenery
Negative prompt: easynegative
Steps: 40, Sampler: DPM++ 2M Karras, CFG scale: 6, Seed: 3943213078, Size: 872x872,
Model hash: 876b4c7ba5, Model: cetusMix_Whalefall2, Clip skip: 2,
ControlNet: "preprocessor: none, model: control_v1p_sd15_qrcode_monster [a6e58995],
weight: 1.35-1.5, starting/ending: (0.05, 1), resize mode: Resize and Fill,
pixel perfect: True, control mode: Balanced, preprocessor params: (512, 64, 64)",
Version: v1.3.
```

### 第二步：制作基础二维码

了解了上述要点后，使用二维码制作工具生成一个输入给 SD 的基础二维码。互联网上有多种网页二维码生成工具可以选择。同时为了方便使用，这里推荐一个 WebUI 插件：

- **Anthony's QR Toolkit**：整合在 Webui 的 QRCode 生成与优化工具
  - [https://github.com/antfu/sd-webui-qrcode-toolkit](https://github.com/antfu/sd-webui-qrcode-toolkit)

![QR Toolkit 配置](images/image10.jpg)

完成二维码制作后，可以点击右侧的 "Download" 以下载到本地，或点击 "Send to ControlNet" 直接将二维码发送至 ControlNet 以进行下一步操作。

### 第三步：确定艺术风格

使用 Stable Diffusion 进行艺术创作的核心是选择合适的模型 + 提示词。在创作艺术二维码之前，建议先不使用 ControlNet，进行一次普通的图片生成，以测试生图效果。

![测试生图效果](images/image11.jpg)

生成参数：

```
Prompt: mountain, green grassland, sky, cloud, bird, blue sky, no human, day, wide shot, flying, border, outdoors, white bird, scenery
Negative prompt: easynegative
Steps: 20, Sampler: Euler a, CFG scale: 7, Seed: 4078355702,
Face restoration: CodeFormer, Size: 512x512,
Model hash: 876b4c7ba5, Model: cetusMix_Whalefall2, Clip skip: 2, Version: v1.3.2
```

### 第四步：在 ControlNet 中导入二维码

确认好图片风格后，将未经处理的二维码上传至 ControlNet。请注意以下几个选项的配置：

- **"启用" 按钮**：勾选以确保 ControlNet 在图片生成过程中生效
- **模型选框**：请选择 `control_v1p_sd15_qrcode_monster` 来加强二维码的控制力度
- **控制权重**：对于 qrcode_monster 模型，建议设置在 1.1-1.6 之间
- **引导介入 / 终止时机**：介入时机建议在 0-0.1 之间，终止时机建议为 1

![ControlNet 配置](images/image12.jpg)

在文生图配置中建议调整两组数值：

- **迭代步数**：建议在 30-50 之间，默认值 20 不足以引导生成一个高质量的二维码图片
- **宽度 / 高度**：建议直接从 ControlNet 发送二维码原图的宽高比至上方

![文生图参数调整](images/image13.jpg)

参数全部配置完成后，点击生成即可。如果生成的二维码不能够达到期望，可以微调以下几个参数，并增加生成的总批次数，不断尝试以逼近最终期望的效果：

- 提示词
- 采样方法
- ControlNet 控制权重
- ControlNet 引导介入 / 终止时机

![生成效果](images/image14.jpg)

此处我们生成了一个效果不错的图片，使用手机扫码测试也完全通过。

![参数微调](images/image15.jpg)

必要时可以选择使用"脚本"中的 X/Y/Z Plot，来对比不同参数下生成二维码的效果。以下对比了 ControlNet 的控制权重和引导介入时机：

![X/Y/Z Plot 对比](images/image16.jpg)

## 使用 OpenPose 优化人物二维码

在掌握了基础的艺术二维码生成技巧后，我们可以进一步探索如何将 **OpenPose** 与二维码结合——通过人体姿势骨架图作为额外的 ControlNet 输入来控制生成角色的姿态，从而创造出更具艺术感和故事性的二维码作品。

### 效果展示

| ![OpenPose + QR Code](images/1-open-pose-code.png) | ![Girl with Car](images/2-girl-with-car.png) |
|:---:|:---:|

上面的示例使用的提示词：

```text
(school girl:1.6, walking), (a car, side view, to left), (residential area, cherry trees)
Negative prompt: (worst quality:1.6),(low quality:1.6), (inaccurate limb:1.2),bad composition, inaccurate eyes, easynegative
Steps: 50, Sampler: Euler a, CFG scale: 7, Seed: 3408317133, Size: 900x540, Model: cetusMix_Whalefall2
```

### 环境准备：开启多个 ControlNet Unit

要同时使用 OpenPose 和 QR Code 两个 ControlNet 模型，需要启用多个 ControlNet Unit：

1. 进入 **Settings**（设置）标签页
2. 在左侧找到 **ControlNet** 选项
3. 将 **Multi ControlNet** 的 Unit 数量设置为不小于 **2**
4. 点击 **Apply Settings**（保存设置）
5. 点击 **Reload UI**（重载前端）使设置生效

![进入设置](images/3-setting.png)

![设置多 Unit](images/4-set-multi-unit.png)

![重载前端](images/5-reload-ui.png)

![确认生效](images/6-check-result.png)

### 导入骨架数据并启用 OpenPose

1. 在 ControlNet 区域点击 **OpenPose Editor**（OpenPose 编辑器）
2. 加载预设的 JSON 骨架数据
3. 点击 **Send to txt2img**（发送到文生图）
4. 启用 ControlNet，选择预处理器为 `none`，模型选择 `control_v11p_sd15_openpose`

![导入骨架数据](images/7-import-pose.png)

![启用 OpenPose](images/8-enable-openpose.png)

### 导入二维码并生成

1. 切换到 **ControlNet Unit 1**
2. 上传你的二维码图片
3. 选择模型 `control_v1p_sd15_qrcode_monster`，将 **Control Weight**（控制权重）设置为 **1.7**
4. 设置迭代步数为 **30-50** 步
5. 根据需要调整生成图片的宽高比

![启用 QR Code Monster](images/9-enable-qr-monster.png)

![设置宽高](images/10-set-hw.png)

### 设置提示词并生成

**正向提示词（Positive Prompt）：**

```text
(1girl:1.6, side lying sleep, on the garden, sunflowers), wooden floor
```

**反向提示词（Negative Prompt）：**

```text
extra hands, extra fingers, extra legs, fewer fingers, (low quality, worst quality:1.4), (bad anatomy), (inaccurate limb:1.2),bad composition, inaccurate eyes, extra digit,fewer digits,(extra arms:1.2), signature, easynegative
```

![设置提示词](images/11-set-prompt.png)

### 最终效果

![OpenPose + QR Code 最终效果](images/12-openpose-qrcode.png)

通过巧妙地偏移二维码位置和运用构图技巧，可以有效地将观众的视觉焦点从二维码转移到角色本身，让整体画面更加自然协调。

| ![](images/13-lying-sleep-openpose.png) | ![](images/14-openpose.png) |
|:---:|:---:|


### 调优建议

在实际创作中，可以从以下几个方面进行调优：

- **提示词**：调整角色描述、场景、风格等关键词的权重
- **采样方法**：尝试不同的采样器（如 Euler a、DPM++ 2M Karras 等）
- **骨架结构与位置**：调整 OpenPose 骨架的姿势和在画面中的位置
- **控制权重**：分别调整 OpenPose 和 QR Code 的 Control Weight
- **引导介入与终止时机**：调整 ControlNet 的 Starting Control Step 和 Ending Control Step，控制模型在哪些步骤介入引导

## 附录：ControlNet QRCode 模型的选择

截至目前，**QRCode Monster** 是我们测试后认为控制二维码成功率最高，也是二维码融入图像效果最好的模型，该模型可以在 HuggingFace 下载到：

- [QRCode Monster - HuggingFace](https://huggingface.co/monster-labs/control_v1p_sd15_qrcode_monster)

市面上也有另一个二维码模型：**QR Pattern v2.0**。该模型建议结合使用 IoC Lab 的 Brightness 模型作为辅助模型来提高局部对比度，也会产出不错的效果。但根据我们的测试，该模型自带的干扰内容较多，可能会导致图像风格发生很大的变化。这两个模型可以在下方链接下载：

- [QR Pattern v2.0 - Civitai](https://civitai.com/models/90940/controlnet-qr-pattern-qr-codes)
- [IoC Lab ControlNet - HuggingFace](https://huggingface.co/ioclab/ioc-controlnet)

## 参考链接

- [Stable Diffusion AI 方案 Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/facdf921-2eea-4638-bc01-522e1eef3dc5)
- [QR Toolkit 插件作者 Anthony Fu 的 QRCode 共创文档](https://antfu.me/posts/ai-qrcode-101)
- [QRCode Monster - HuggingFace](https://huggingface.co/monster-labs/control_v1p_sd15_qrcode_monster)
- [IoC Lab ControlNet - HuggingFace](https://huggingface.co/ioclab/ioc-controlnet)
- [IoC Lab 模型展示](https://mp.weixin.qq.com/s/i4WR5ULH1ZZYl8Watf3EPw)
- [IoC Lab Stable Diffusion 文档](http://aigc.ioclab.com/)

---

> 原文链接：[借助 ControlNet 生成艺术二维码 – 基于 Stable Diffusion 的 AI 绘画方案](https://aws.amazon.com/cn/blogs/china/art-qr-code-generation-with-controlnet-ai-painting-solution-based-on-stable-diffusion/)
