---
title: "2.1 生成艺术二维码"
weight: 1
type: workshops
---
在本次动手训练营，将使用 eCloudrover imAgine 产品生成艺术二维码，您将以 QRCode 作为 ControlNet 的输入，使 QRCode 数据点融入到艺术图像中，同时仍然可以被 QRCode 扫描器扫描。借助这项技术，您可以将任何二维码转化为独特的艺术作品，以一种全新的方式来表达和传递信息。以下为几张图片案例：

|![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/1-example.png)|![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/2-example.png)|
| ------------------------------------------- | ------------------------------------------- |

#### 1. 优化二维码

二维码是一种借助特定几何图形分配，在二维空间上分布的、黑白相间的、记录数据符号信息的图形。二维码有多种不同的编码方式，我们此处采用通用度最高也是最基础的编码方式：QR Code。

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/3-qr-code-basic.png)

输入的二维码是借助 SD 生成艺术二维码过程中最重要的部分之一。在使用ControlNet生成艺术二维码需要考虑以下两个特点：

1. **二维码中包含的信息量**

无论二维码采用何种编码方式，承载的字符信息越多，二维码在视觉上呈现的黑白结构就越复杂。复杂的结构很容易导致我们在生成艺术创意时，极大地收到二维码本身信息的掣肘。因此我们首先要想办法**精简二维码中包含的字符长度**。

对于最广泛的应用场景，二维码通常会包含一个网页链接；为了提升二维码生成的美观性，首先需要对网页链接进行缩短。市面上的链接缩短工具有很多，您可以自由选择。


{{% workshop-alert type="warning" %}}
注意：在中国大陆境内使用短链，请选择有域名备案的缩链平台，否则会被微信、浏览器等阻挡。
{{% /workshop-alert %}}


例如我们有一个希望制作成二维码的网址：https://www.ecloudrover.com/aigc/ 通过缩链处理后为

```shell
http://c.suo.nz/7KZrF
```

通过下图可以比较直观地看出链接长短对于二维码视觉的影响，缩短的链接将更有利于我们接下来的创作。

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/4-compare-qrcode.png)

2. **二维码的呈现形式**

随着技术发展，二维码不仅只支持黑白方块状的图案样式，定位点和码元都支持多样化的呈现，例如以下几种样式

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/5-qr-code-style.png)

在实际操作中，我们可以尝试多种不同的码点形式，以使得生图效果符合我们的预期。

下图展示了不同的二维码形式对最终效果图的影响：

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/6-qr-code-style-controlnet.png)

```bash
mountain, green grassland, sky, cloud, bird, blue sky, no human, day, wide shot, flying, border, outdoors, white bird, scenery
Negative prompt: easynegative
Steps: 40, Sampler: DPM++ 2M Karras, CFG scale: 6, Seed: 3943213078, Size: 872x872, Model hash: 876b4c7ba5, Model: cetusMix_Whalefall2, Clip skip: 2, ControlNet: "preprocessor: none, model: control_v1p_sd15_qrcode_monster [a6e58995], weight: 1.35-1.5, starting/ending: (0.05, 1), resize mode: Resize and Fill, pixel perfect: True, control mode: Balanced, preprocessor params: (512, 64, 64)", Version: v1.3.
```

#### 2. 制作基础二维码

了解了上述要点后，您将开始使用二维码制作工具，生成一个输入给 SD 的基础二维码。

互联网有多种网页二维码生成工具，您可以自由选择。同时为了方便您使用，在本次动手训练营准备的 专用的 AMI 中已经预装了 QRCode 生成插件，只要您从正确的版本中启用 AMI，都可以直接在 Webui 上看到下述的 QRCode Toolkit：

- Anthony's QR Toolkit：整合在 Webui 的 QRCode 生成与优化工具

  https://github.com/antfu/sd-webui-qrcode-toolkit

接下来我们演示如何使用 Anthony's QR Toolkit 来生成二维码，请选中Webui中的`QR Toolkit`标签页，并参考下图完成二维码参数的配置。

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/7-qrcode-toolkit.png)

完成二维码制作后，点击 “Send to ControlNet”，直接将二维码发送至 ControlNet，或点击右侧的 “Download” 以下载到本地以进行下一步操作。

#### 3. 确定艺术风格

使用 Stable Diffusion 进行艺术创作的核心是选择合适的模型+提示词。您在创作艺术二维码之前，建议先不使用 ControlNet，先进行一次普通的图片生成，以测试生图效果。

此处我们希望二维码中有山川、蓝天、白云等自然景观，因此先使用以下参数，测试提示词和模型的生成效果。

```shell
mountain, green grassland, sky, cloud, bird, blue sky, no human, day, wide shot, flying, border, outdoors, white bird, scenery
Negative prompt: easynegative
Steps: 20, Sampler: Euler a, CFG scale: 7, Seed: 4078355702, Face restoration: CodeFormer, Size: 512x512, Model hash: 876b4c7ba5, Model: cetusMix_Whalefall2, Clip skip: 2, Version: v1.3.2
```
![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/8-blue-sky.png)


#### 4. 生成艺术二维码

确认好图片风格后，我们将未经处理的二维码上传 ControlNet。请在“文生图”标签页中展开ControlNet标签，并注意以下几个选项的配置：

- 勾选 **“启用” 按钮** ：以确保 ControlNet 在图片生成过程中生效；
- 模型选框：请选择 **“control_v1p_sd15_qrcode_monster”** 来使用ControlNet二维码控制模型；
- 控制权重：对于 qrcode_monster 模型，建议设置在 **1.1-1.6** 之间；
- 引导介入/终止时机：介入时机建议在 **0-0.1** 之间，终止时机建议为 **1**。

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/9-controlenet-qrcode.png)

在文生图配置中建议调整两组数值：

- 迭代步数：在 **30-50** 之间，默认值 20 不足以引导生成一个高质量的二维码图片
- 宽度/高度：直接从 ControlNet 发送二维码原图的宽高比至上方

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/10-tx2img.png)

参数全部配置完成后，点击生成即可，可以看到此处我们生成了一个效果不错的图片，使用手机扫码测试也完全通过。

![11-qrcode](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/11-qrcode.png)

#### 5. 结果调优

ControlNet 的参数会影响何时以及如何将控制应用于生成过程。 

- **控制权重** - ControlNet 的权重。   权重越高，输出受 ControlNet 的影响就越大。 
- **开始控制步骤** - ControlNet 开始生效时生成过程的百分比。 
- **结束控制步骤** - ControlNet 停止生效时生成过程的百分比。 

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/controlenet.png)

启动控制步骤将允许提示和模型在知道 QR 码控件存在之前发挥创意。  最终控制步骤将允许模型尝试将 QR 码更多地融入到艺术品中（但会使二维码更难扫描）。 它需要几次尝试和错误才能找到适当的平衡，以便 ControlNet 有足够的时间进行干预，但又不能太多，这样代码就足够艺术化。 

如果生成的二维码不能够达到期望，可以选择微调以下几个参数，并增加生成的总批次数，不断尝试抽卡以逼近最终期望的效果：

- 提示词
- 采样方法
- ControlNet 控制权重
- ControlNet 引导介入/终止时机

必要时可以选择使用 “脚本” 中的 X/Y/Z Plot，来对比不同参数下生成二维码的效果。要使用X/Y/Z Plot，请在WebUI页面底部“脚本”处选择X/Y/Z Plot，您可以尝试通过选中X与Y轴的类型（Type），以控制ControlNet 控制权重（ControlNet Weight）和 ControlNet引导介入/终止时机（ContolNet Guidance Start）来观察不同生成的效果。

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/12-xyz-plot.png)

选中X与Y轴的类型后之后，轴值（Value）部分的设置可以参考以下数值类型的写法：

- 区间写法1，单调递增1：`1-5 = 1, 2, 3, 4, 5`
- 区间写法2，根据指定值递增：
  - `1-5 (+2) = 1, 3, 5`
  - `10-5 (-3) = 10, 7`
  - `1-3 (+0.5) = 1, 1.5, 2, 2.5, 3`
- 区间写法3，生成范围内n个数值
  - `1-10 [5] = 1, 3, 5, 7, 10`
  - `0.0-1.0 [6] = 0.0, 0.2, 0.4, 0.6, 0.8, 1.0`


{{% workshop-alert type="warning" %}}
注意：如果您输入较细粒度的递增指标，则最终结果生成时间较长，请选择适合您的参数。
{{% /workshop-alert %}}


我们此处对比了 ControlNet 的控制权重和引导介入时机。将生成X轴为ControlNet 控制权重`1.0-1.8`按照`0.1`递增，共9个数据点；Y轴ControlNet 引导介入/终止时机 `0-0.1` 按照 `0.01`递增，共3个数据点。共计27张对比图。

![](/aws-workshops/glb-aigc-ami-workshop/assets/2-1-qrcode/13-grid.png)


{{% workshop-alert type="success" %}}
通过优化，您可以选中您喜好的参数以生成最终效果图。
{{% /workshop-alert %}}
