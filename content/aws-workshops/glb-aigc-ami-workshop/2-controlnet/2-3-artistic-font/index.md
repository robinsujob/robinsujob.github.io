---
title: "2.3 生成艺术字"
weight: 3
type: workshops
---
字体是一种艺术形式，不仅可以传递信息，还可以为品牌和产品带来独特的风格和个性。如何选择合适的字体成为了品牌宣传和市场营销中的重要环节。

Stable Diffusion可以将文字和图像完美地融合在一起，形成了一种全新的表现方式。 这种创意让字与图相互交织，呈现出独特的视觉效果！本文主要分享使用伊克罗德的 imAgine 产品生成光影艺术字的最佳实践。我们将以 QRCode 作为 ControlNet 的输入，使 QRCode 文字图像融入到艺术图像中，从而以一种全新的方式来表达和传递信息。以下为几张图片案例：

- **渲染海报艺术字**

| ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/1-cake-example01.png) | ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/1-cake-example02.png) |
|-------------------------|---------------------------------------------|

- **嵌入艺术字**

| ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/2-sea-example01.png) | ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/2-sea-example02.png) |
|--------------------------------------------|--------------------------------------------|

- **光影效果艺术字**

| ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/3-Tianjin-example01.png) | ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/3-Tianjin-example02.png) |
|------------------------------------------------|------------------------------------------------|
#### 前期准备： (1)底图
首先需要准备类似我下面的白字的图片，白字的内容决定了画面里展示的内容。推荐使用PS、美图秀秀，亦可以打开Word打字然后截图也行。

| ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/4-Template01-Cake.jpg) | ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/4-Template02-Sea.png) | ![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/4-Template03-Tianjin.png) |
|----------------------------------------------|---------------------------------------------|-------------------------------------------------|
#### 前期准备：(2)模型环境准备
当我们选择好合适的底图文件进行后续加工后，选择合适的模型生成至关重要。如果目标是生成有质感的服装搭配图片,我强烈建议使用3D模型,例如 MajicmixRealistic和 ChilloutMix。这些模型可以增强图像的逼真性和质感。
具体来说,我推荐根据图片内容选择如下模型:
- 真人图片: `majicmixRealistic、chilloutmix` ，这些模型在处理人像图像方面表现优秀。
- 其他类型图片: `revAnimated、realisticVision、deliberate` ，这些通用模型可以处理各类图像,输出效果更为均衡。
### 一、海报艺术字
> 这里我们使用Stable Diffusion帮助我们快速生成海报元素，比如蛋糕的各种元素拼成的”文字”图片,且背景简单容易抠图 由于是关于真实物品的图片，所以在推荐模型里选择`revAnimated`作为主模型
```code
Part1: Prompt
white background, cake, fruit, white background, 4k ,ins
(白色背景, 蛋糕, 水果, 白色背景, 4k, ins)
=====================================
Part2: Negative Prompt
easy negative,worst quality.low quality,normal quality:jpeg artifacts,signature, watermark,username,blurry, (bad and mutated hands),(worst quality :2.0), (low quality:2.0)
(容易出现负片，质量最差。低画质，画质正常：jpeg 伪像、签名、水印、用户名、模糊、（手牌不好和变异），（质量最差：2.0），（低质量：2.0）)
```
##### 1.模型选择与参数调整
由于是关于真实物品的图片，所以在推荐模型里选择revAnimated作为主模型
我们的需求是，生成”文字”以白色浪花的形式嵌入海洋的图片,故在这里推荐模型里选择了revAnimated作为主模型.
填好提示词后就需要调整参数，主要分为Stable Diffusion参数和ControlNet参数
###### Part1: Stable Diffusion参数
 - **采样方法**(Sampler)：Euler
 - **宽度**(Width)和**高度**(Height)则根据底图的大小调整 - 由于图片大小我选择1270（长）*520（高）
 - 其他参数则保持默认
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/5-SD_Setting-1.png)

###### Part2: ControlNet参数
 - 海报效果需要**白底黑字**的底图
 - 把底图上传到ControlNet内，如下图所示
 - 勾选**启用(Enable)**和**完美像素模式(Pixel Perfect)**
 - **预处理器(Preprocessor)选择**depth_midas
 - **模型(Model)**选择depth
 - **控制权重(Control Weight)**建议0.7-1之间 ，同时可以适当调整引导介入时机0-0.1
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/5-SD_Setting-2.png)
##### 2.海报艺术字生成
如下图所示是通过Stable Diffusion Web UI生成的Cake宣传图，可以多次生成选择最有质感的作品作为素材
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/6-AI-Cake.png)
### 二、嵌入艺术字
> 这里我们使用Stable Diffusion帮助我们快速生成海报元素，，生成”文字”以白色浪花的形式嵌入海洋的图片
```code
Part1: Prompt
wide sea,long shot,bird's eye view,Aerial view,complex details,wave,masterpiece,realistic,8k,Fujifilm,film
（宽阔的海，长镜头，鸟瞰图，鸟瞰图，复杂细节，波浪，杰作，写实，8K，富士胶片，胶片）
==========================================================================
Part2: Negative Prompt
worst quality, low quality, normal quality, lowres, watermark, monochrome
（最差质量，低质量，正常质量，低分辨率，水印，黑白的）
```
##### 1.模型选择与参数调整
由于是关于真实场景的图片，这里依旧推荐模型里选择revAnimated作为主模型
我们的需求是，生成”文字”以白色浪花的形式嵌入海洋的图片,故在这里推荐模型里选择了revAnimated作为主模型.
填好提示词后就需要调整参数，主要分为Stable Diffusion参数和ControlNet参数
###### Part1: Stable Diffusion参数
  - **采样方法**(Sampler)：DPM++3M SDE Karras
  - **选代步数**(Steps)：40
  - 勾选**完美像素模式(Pixel Perfect)**
  - **宽度**(Width)和**高度**(Height)则根据底图的大小调整,其他参数则保持默认.
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/5-SD_Setting-3.png)
###### Part2: ControlNet参数
  - 勾选**启用(Enable)**和**完美像素模式(Pixel Perfect)**
  - **预处理器(Preprocessor)** 选择Tile_resample
  - **模型(Model)** 选择Tile
  - **控制权重(Control Weight)** 建议0.65-0.9之间,其他参数则保持默认.
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/5-SD_Setting-4.png)
##### 2.嵌入艺术字生成
如下图所示是通过Stable Diffusion Web UI生成的乘风破浪概念图，可以多次生成选择最有质感的作品作为素材
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/7-AI-Lake.png)
### 三、光影/隐藏艺术字
> 这里我们使用Stable Diffusion帮助我们快速生成带有光影/隐藏艺术字的特效照片。例如"天津"的城市景观中嵌入字体。
```code
Part1: Prompt
A picture of the night scene in Tianjin with a warm atmosphere. The huge Ferris wheel in the eye of Tianjin slowly rotates, and excited tourists are seated in every cabin. Under the ferris wheel, the lights were red, wine and green, and the bar street was full of people coming and going. The lights of the Tianjin Eye flickered on the surface of the Haihe River, and the light shone through the windows of the skyscrapers lined up on both sides of the river. The family sat on a bench in front of Tianjin, laughing and taking a group photo. The city is brightly lit, and the atmosphere of life is everywhere.
（一张气氛温馨的天津夜景照片,天津之眼巨大的摩天轮缓缓转动,每个舱里都坐着兴奋的游客。摩天轮下是一片灯红酒绿,酒吧街涌动着来来往往的人群。天津之眼的灯光在海河水面上闪烁,两岸林立的摩天大楼窗户里透出光亮。一家人坐在天津之眼下的长椅上,笑着合影留念。这座城市灯火通明,处处洋溢着生活的气息。）
=======================================================================================================================================================================================================================================
Part2: Negative Prompt
worst quality, low quality, normal quality, lowres, watermark, monochrome
（质量最差、质量低、质量正常、低分辨率、水印、单色）
```
##### 1.模型选择与参数调整
由于是关于真实场景的图片。这里对于推荐模型里选择revAnimated作为主模型 我们的需求是，生成天津"的城市景观中嵌入字体的图片,故在这里推荐模型里选择了revAnimated作为主模型.
填好提示词后就需要调整参数，主要分为Stable Diffusion参数和ControlNet参数
###### Part1: Stable Diffusion参数
  - **采样方法**(Sampler)：DPM++3M SDE Karras
  - **选代步数**(Steps)：40
  - 勾选**完美像素模式(Pixel Perfect)**
  - **宽度**(Width)和**高度**(Height)则根据底图的大小调整,其他参数则保持默认.
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/5-SD_Setting-5.png)
###### Part2: ControlNet参数
  - 勾选**启用(Enable)**和**完美像素模式(Pixel Perfect)**
  - **预处理器(Preprocessor)** 选择None
  - **模型**(Model)选择QRCode_Monster
  > 截至目前，**QRCode Monster** 是我们测试后认为成功率最高，也是文字融入图像效果最好的模型，目前 **QRCode Monster** 已经更新至 **v2** 版本，相比起 v1，融合度和出图率会有更高的表现。
  - **控制权重(Control Weight)** 建议1.15-1.5之间,其他参数则保持默认.
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/5-SD_Setting-6.png)
##### 2.嵌入艺术字生成
如下图所示是通过Stable Diffusion Web UI生成的天津城市风景概念图，可以多次生成选择最有质感的作品作为素材
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-3-front/8-AI-Tianjin.png)
