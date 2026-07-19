---
title: "3. 生成拜年图"
weight: 5
type: workshops
---
本节将为大家演示如何使用[imAgine绘图方案](https://www.ecloudrover.com/aigc/)生成新春贺年图，以下呈现了几张效果图，祝大家龙年大吉！

![](/aws-workshops/glb-aigc-ami-workshop/assets/3-newyear/example-image01.png) 

| ![](/aws-workshops/glb-aigc-ami-workshop/assets/3-newyear/example-image02.png) | ![](/aws-workshops/glb-aigc-ami-workshop/assets/3-newyear/example-image03.png) |
|-------------------------|---------------------------------------------|


[Stable Diffusion](https://github.com/CompVis/stable-diffusion) (SD)是2022年发布的开源的文生图模型，通用性强，但无法满足对细节和特定内容的绘图需求，因此人们通常会对官方SD模型进行微调来得到可以应用于特定领域的定制模型。常见的SD微调技术包括[Dreambooth](https://dreambooth.github.io/)，[LoRA](https://github.com/microsoft/LoRA)，[Textual Inversion](https://textual-inversion.github.io/)（也称为 Embedding）和[Hypernetworks](https://stable-diffusion-art.com/hypernetwork/)等，几种技术的对比可参考此[博客](https://aws.amazon.com/cn/blogs/china/stable-diffusion-quick-kit-series-model-fine-tuning-with-dreambooth-optimization-practices-on-sagemaker/)。为了方便您使用，本次实验涉及到的模型均已预装入专用的AMI中。


### 一、实验环境准备

实验开始前，请确保您已完成以下事项：

* 已按照[0.简介与前提条件](/aws-workshops/glb-aigc-ami-workshop/0-prerequisites/)申请了加速计算型实例资源
* 已按照[1.订阅和部署解决方案](/aws-workshops/glb-aigc-ami-workshop/1-subscribe/)订阅并部署了imAgine绘图解决方案。


### 二、图片生成
**1.参数配置**

```code
1girl, eastern dragon, open mouth, smile, long sleeves, chinese clothes, black hair, brown eyes, dress, short hair, socks, simple background, hair ribbon, red ribbon, china dress, yellow eyes, red footwear, red dress,ribbon, two side up, bangs, tabi, brown hair, :d, red background<lora:mw_hbfm_v1:0.85>
Negative prompt: easynegative,dark,bad hands,bad feet,worst quality,low quality,normal quality,bad artist,bad anatomy,Japanese style
Steps: 20, Sampler: DPM++ SDE Karras, CFG scale: 7, Seed: 475956187, Size: 512x728, Model hash: e3edb8a26f, Model: ghostmix_v20Bakedvae, VAE hash: 735e4c3a44, VAE: vae-ft-mse-840000-ema-pruned.safetensors, Denoising strength: 0.5, Clip skip: 2, ADetailer model: face_yolov8n.pt, ADetailer prompt: "Little girl, young, Smile", ADetailer confidence: 0.3, ADetailer dilate erode: 4, ADetailer mask blur: 4, ADetailer denoising strength: 0.4, ADetailer inpaint only masked: True, ADetailer inpaint padding: 32, ADetailer model 2nd: hand_yolov8n.pt, ADetailer prompt 2nd: "Little girl, young, delicate hands, delicate fingers", ADetailer confidence 2nd: 0.3, ADetailer dilate erode 2nd: 4, ADetailer mask blur 2nd: 4, ADetailer denoising strength 2nd: 0.4, ADetailer inpaint only masked 2nd: True, ADetailer inpaint padding 2nd: 32, ADetailer version: 24.1.1, Hires upscale: 2, Hires steps: 10, Hires upscaler: R-ESRGAN 4x+ Anime6B, Lora hashes: "mw_hbfm_v1: 36178776ef7d", TI hashes: "easynegative: c74b4e810b03", Version: v1.7.0
```

首先将上述参数复制到SD Web UI 的正向提示词文本框中，如下图所示

![](/aws-workshops/glb-aigc-ami-workshop/assets/3-newyear/webui-config-01.png) 

然后点击下图所示的**箭头**，Web UI可自动识别并加载相关参数到相应配置。请确保勾选了**高分辨率修复**和**启用After Detailer**。

![](/aws-workshops/glb-aigc-ami-workshop/assets/3-newyear/webui-config-02.png) 

点击生成，即可生成精美的拜年图片

![](/aws-workshops/glb-aigc-ami-workshop/assets/3-newyear/webui-config-03.png) 

**2.参数解释**


|  参数   | 解释  |
|  ------  | ----  |
| 正向提示词（Positive Prompt）  | 对想要生成的图片的描述。 |
| 反向提示词（Negative Prompt）| 不希望包含在图片中的的元素。 |
| 迭代步数（Steps）  | SD将初始噪声转换为可识别图像所运行的迭代次数。 |
| 采样方法（Sampler） | SD每迭代一步都会产生一个新的图像样本，这个过程被被称为采样，所使用的方法被称为采样方法。不同采样方法的对比可参考此[博客](https://stable-diffusion-art.com/samplers/)。 |
| 提示词引导系数（CFG Scale）  | 图片与提示词的相关度。数值越大，生成的图片与提示次描述越像；数值越小关联度越低。 |
| 生图长宽（Size）  | 生成图片的大小，它在一定程度上影响了主题/图片内容。 |
| 随机种子（Seed）  | 决定了生成图片时的随机性，同时确保了结果的可重现性。在其他参数不变的情况下，相同的种子可以多次生成（几乎）相同的图像。 |
| 高分辨率修复 (Hires. fix)   | 放大算法（Hires upscaler）：通过大量数据训练的模型，能够恢复原始图像并填补缺失信息。不同放大算法的对比可参考[博客](https://civitai.com/articles/636/sd-upscalers-comparison)。<br>重绘幅度（Denoising strength）：决定算法对图像内容的影响程度。设置0时，不会改变图像，而在1时，将获得不相关的图像。<br>放大倍数（Hires upscale）：指放大到原图的多少倍。倍数越大，细节越丰富，但显存占用也会增加。 |
| [ADetailer](https://github.com/Bing-su/adetailer)  | ADetailer是一款识别面部/人物/手部并自动对其进行mask和重绘的工具，可以通过调整参数去改变识别的对象和识别区域的大小及位置。|
| [Clip skip](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/5674)  | CLIP是SD的三个模型之一，用于将提示文本转换为数值表示。CLIP 是一个神经网络，向量化的提示词会通过各层传递直到最后一层。Clip Skip参数用于控制向量化的提示词会在哪一层停止传递。例如，Clip Skip = 1代表使用CLIP模型的所有层，Clip Skip = 2 表示跳过CLIP模型的最后一层，依此类推。 |


### 三、X/Y/Z脚本查找最佳参数（可选）

[X/Y/Z Plot](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#xyz-plot)脚本可以按照我们设定的参数矩阵生成对比图，方便我们观察不同参数对于图片的影响。

以Clip skip参数为例，我们希望对比CFG Scale一定时，不同Clip skip数值对最终生成的图片的影响，可在SD Web UI中按照下图配置。

![](/aws-workshops/glb-aigc-ami-workshop/assets/3-newyear/xyz-plot-01.png) 

可以看到，随着Clip skip值的增加，提示词中的一些信息，例如dragon被忽略了。

![](/aws-workshops/glb-aigc-ami-workshop/assets/3-newyear/xyz-plot-02.png) 

![](/aws-workshops/glb-aigc-ami-workshop/assets/3-newyear/xyz-plot-03.png)
