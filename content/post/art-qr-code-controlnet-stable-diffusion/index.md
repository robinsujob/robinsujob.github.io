---
slug: "art-qr-code-controlnet-stable-diffusion"
title: "Art QR Code with ControlNet and Stable Diffusion"
date: 2023-09-01
description: "Generate artistic QR codes using ControlNet and Stable Diffusion, with OpenPose for dynamic character poses."
image: images/sample1.jpg
categories:
  - AI/ML
tags:
  - stable-diffusion
  - controlnet
  - qr-code
  - openpose
  - art
---

## Background

In the past few months, there has been growing interest in combining Stable Diffusion with ControlNet to create artistic QR codes — QR codes that are not only scannable but also visually stunning works of art.

This post shares practical tips for working with Stable Diffusion and walks through the process of generating artistic QR codes using ControlNet. We will use QR codes as ControlNet input, integrating QR code data points into artistic images while maintaining scannability. With this technology, you can transform any QR code into a unique piece of art. Here are some examples:

![Sample 1](images/sample1.jpg)
![Sample 2](images/sample2.jpg)
![Sample 3](images/sample3.jpg)

## Stable Diffusion Practical Tips

### Prompt Engineering

As Stable Diffusion versions continue to evolve, the requirements for effective prompts have changed significantly. Many old prompt conventions can actually hurt image quality with modern models.

#### Basic Concepts

Prompts are divided into **positive prompts** (what you want) and **negative prompts** (what you don't want).

#### Common Misconceptions

Prompts are about precision, not quantity — using the shortest words to describe the scene is more effective than natural language. Quality-improving descriptors should not be mindlessly stacked. Common starters like "masterpiece" and "best quality" were meaningful in the NovelAI era when they were heavily used for image evaluation during training, but after continuous model refinement on Civitai, these prompts barely show their intended effect in modern models.

#### Adjusting Prompt Weights

The default weight of each token is 1, decreasing from left to right. Prompt weights significantly affect the generated image. You can specify weight using parentheses + colon + number, e.g., `(one girl:1.5)`.

#### Mind the Prompt Order

If landscape tags come first, the character will appear small; conversely, the character will be larger or shown as half-body. Choosing the correct order and syntax for prompts will more effectively render the desired scene.

#### Emojis in Prompts

Prompts support emojis with good expressiveness. For specific facial expressions or actions, adding emojis can achieve the desired effect. To prevent semantic drift, prefer emojis and minimize unnecessary complex syntax like "with".

#### Recommended Camera Angle Prompts

| Parameter | Description |
|------|------|
| extreme closeup | Face close-up |
| close up | Head |
| medium close up | ID photo |
| medium shot | Half body |
| cowboy shot | No legs |
| medium full shot | No feet |
| full shot | Full body |

### Image Optimization

Often we generate an image that's not quite satisfactory and want to further optimize it. Here are some best practices for parameter tuning:

#### Which Parameters to Adjust

- **CFG Scale**: The correlation between the image and the prompt. Higher values mean greater prompt influence.
  - CFG 2–6: Creative but may be too distorted. Fun for short prompts.
  - CFG 7–10: Recommended for most prompts. Good creativity-guidance balance.
  - CFG 10–15: Use when the prompt is detailed and clear.
  - CFG 16–20: Generally not recommended. May affect quality.
  - CFG >20: Almost unusable.
- **Sampling Steps**: More steps mean smaller, more precise adjustments per step, but proportionally increase generation time. Beyond 50 steps, improvements become negligible.
- **Sampling Method**: Different methods have different optimal step counts.
  - Euler a: Creative, good for quick prompt testing.
  - DPM2 a Karras: Good for realistic models, hard to control after 30 steps.
  - DPM++ 2M Karras: Excellent at high step counts, more details.
  - DDIM: Fast convergence but needs many steps; good for inpainting.
  - Different model and sampler combinations produce different results; use X/Y/Z plots for comparison.
- **Seed**: The random seed has a huge impact on composition and is the main source of randomness in SD. With the same seed and all other parameters fixed, you can reproduce (nearly) identical images. Once you find a suitable composition, fix the seed and fine-tune details.

#### How to Find Optimal Parameters

Use X/Y/Z plots to clearly compare results under different parameters, quickly locate suitable parameter ranges, and perform further generation control.

![X/Y/Z Plot Comparison](images/image4.jpg)

#### Image Size Optimization

Image quality is not directly tied to image size. However, size somewhat affects the subject and content, as it implicitly represents the category (e.g., portrait for vertical, landscape for horizontal, small resolution for stickers). When the output size is too wide, multiple subjects may appear. Sizes above 1024 may produce undesirable results with significant GPU memory pressure. Small resolution + upscaling is recommended.

#### Optimizing Multi-Character and Wide-Format Generation

Using txt2img alone cannot effectively specify individual character features in multi-character scenarios. The recommended approach is to create a draft + img2img or ControlNet. For wide-format single-character generation, draft a sketch with color blocking to determine the main subject, or use ControlNet's OpenPose for character skeleton. For multi-character scenes, use ControlNet's OpenPose to specify character count; this also works for three-view drawings of the same character.

#### Hand Repair

Send the image to img2img inpaint with similar prompts, placing "hand" prompts at the front. Set denoising strength based on how much you want hand features to change (below 0.25 for just completeness). For more precise hand control, find a satisfactory hand reference image and use ControlNet's Canny or OpenPose_hands preprocessor + model combined with inpaint.

#### Face Repair

When drawing images with small character subjects, facial distortion frequently occurs. Especially in the artistic QR code generation process described later, faces often break due to QR code data points. For facial inpainting, the **ADetailer** plugin is recommended. It uses YOLO for object detection, identifies faces, and performs localized inpainting with specified prompts and models. ADetailer can handle both face and hand detection and repair, and can also reference LoRA models for localized inpainting.

![ADetailer Face Repair](images/image5.jpg)

## Generating Artistic QR Codes with ControlNet

### Step 1: Optimize the QR Code

A QR code is a pattern of black and white geometric shapes distributed in 2D space that records symbolic data. There are multiple encoding methods; we use the most universal one: QR Code.

The input QR code is one of the most important factors in generating artistic QR codes. We mainly care about two characteristics:

![QR Code Structure](images/image6.jpg)

**1. Information contained in the QR code**

The more character information a QR code carries, the more complex its visual structure becomes. Complex structures greatly constrain artistic creativity during generation. Therefore, we first need to simplify the content length.

For the most common use case — web links — shorten the URL first. There are many URL shortening tools available.

![URL Length Comparison](images/image7.jpg)

**2. How the QR code is presented**

With technological development, QR codes no longer only support black and white square patterns; both positioning points and modules support diverse presentation styles.

In practice, try different module styles to achieve the desired generation effect. The following images show how different QR code styles affect the final result:

![Different Module Styles](images/image8.jpg)
![Different QR Code Style Comparison](images/image9.jpg)

Generation parameters:

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

### Step 2: Create the Base QR Code

After understanding the key points above, use a QR code generation tool to create a base QR code for SD input. There are many web-based generators available. For convenience, here's a useful WebUI plugin:

- **Anthony's QR Toolkit**: Integrated QR code generation and optimization tool for WebUI
  - [https://github.com/antfu/sd-webui-qrcode-toolkit](https://github.com/antfu/sd-webui-qrcode-toolkit)

![QR Toolkit Configuration](images/image10.jpg)

After creating the QR code, click "Download" to save it locally, or click "Send to ControlNet" to pass it directly for the next step.

### Step 3: Determine the Art Style

The core of creating art with Stable Diffusion is choosing the right model + prompts. Before creating artistic QR codes, generate an image without ControlNet first to test the style.

![Test Generation Result](images/image11.jpg)

Generation parameters:

```
Prompt: mountain, green grassland, sky, cloud, bird, blue sky, no human, day, wide shot, flying, border, outdoors, white bird, scenery
Negative prompt: easynegative
Steps: 20, Sampler: Euler a, CFG scale: 7, Seed: 4078355702,
Face restoration: CodeFormer, Size: 512x512,
Model hash: 876b4c7ba5, Model: cetusMix_Whalefall2, Clip skip: 2, Version: v1.3.2
```

### Step 4: Import QR Code into ControlNet

After confirming the image style, upload the unprocessed QR code to ControlNet. Pay attention to these configuration options:

- **"Enable" button**: Check to ensure ControlNet is active during generation
- **Model selector**: Select "control_v1p_sd15_qrcode_monster" to strengthen QR code control
- **Control weight**: For the qrcode_monster model, we recommend 1.1–1.6
- **Guidance start/end timing**: Start timing recommended between 0–0.1, end timing recommended at 1

![ControlNet Configuration](images/image12.jpg)

In txt2img configuration, adjust two key values:

- **Sampling steps**: recommended 30–50 (default 20 is insufficient for high-quality QR code images)
- **Width/Height**: match the original QR code aspect ratio from ControlNet

![txt2img Parameter Adjustment](images/image13.jpg)

After all parameters are configured, click generate. Here we can see a good result — the QR code passes scanning tests on mobile phones.

If the generated QR code doesn't meet expectations, try fine-tuning:

- Prompts
- Sampling method
- ControlNet control weight
- ControlNet guidance start/end timing

![Generation Result](images/image14.jpg)
![Parameter Fine-tuning](images/image15.jpg)

When necessary, use the X/Y/Z Plot in "Scripts" to compare QR code generation effects under different parameters. Here we compared ControlNet's control weight and guidance start timing:

![X/Y/Z Plot Comparison](images/image16.jpg)

## Appendix

### Appendix 1: Choosing ControlNet QR Code Models

To date, **QRCode Monster** is the model with the highest QR code control success rate and best image fusion effect. It can be downloaded from HuggingFace:

- [QRCode Monster - HuggingFace](https://huggingface.co/monster-labs/control_v1p_sd15_qrcode_monster)

Another option is **QR Pattern v2.0**, best used with IoC Lab's Brightness model as an auxiliary to improve local contrast. However, based on our testing, this model introduces more interference that may significantly alter the image style. Downloads:

- [QR Pattern v2.0 - Civitai](https://civitai.com/models/90940/controlnet-qr-pattern-qr-codes)
- [IoC Lab ControlNet - HuggingFace](https://huggingface.co/ioclab/ioc-controlnet)

### Appendix 2: imAgine AI Drawing Solution

imAgine is an AI drawing solution based on Automatic1111 Stable Diffusion WebUI, integrated with multiple AWS managed services. It is available on AWS MarketPlace for one-click subscription and rapid deployment.

It integrates with AWS serverless services like Amazon API Gateway and DynamoDB, forwarding training and inference requests from the WebUI frontend to dedicated SageMaker backend servers for seamless compute scaling and cost management.

For detailed steps, refer to the Workshop page: [imAgine Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/facdf921-2eea-4638-bc01-522e1eef3dc5)

## Enhancing QR Codes with OpenPose

Building on the QR code generation techniques above, this section demonstrates how to combine **OpenPose** with QR codes to create even more dynamic and artistic results. OpenPose generates skeleton maps of human poses, which serve as an additional ControlNet input to control character poses in the generated image.

Here are some example results combining OpenPose pose control with QR code generation:

| | |
|:---:|:---:|
| ![OpenPose + QR Code](images/1-open-pose-code.png) | ![Girl with Car](images/2-girl-with-car.png) |

The prompt used for the example above:

```text
(school girl walking on the street:1.6), city background, anime style, masterpiece, best quality
```

### Environment Setup: Enable Multiple ControlNet Units

To use OpenPose and QR Code ControlNet simultaneously, you need at least **2 ControlNet Units** enabled:

1. Go to **Settings** → **ControlNet**
2. Set the **Multi ControlNet** unit count to **2** (or more)
3. Click **Apply Settings**, then **Reload UI**

![Settings](images/3-setting.png)

![Set Multi ControlNet Units](images/4-set-multi-unit.png)

![Reload UI](images/5-reload-ui.png)

![Verify Result](images/6-check-result.png)

### Import Skeleton Data and Enable OpenPose

1. Open the **OpenPose Editor** extension
2. Click **Load JSON** to import your prepared skeleton pose data
3. Click **Send to txt2img** to transfer the pose to ControlNet
4. In ControlNet **Unit 0**, enable ControlNet and select the model **control_v11p_sd15_openpose**

![Import Pose Data](images/7-import-pose.png)

![Enable OpenPose ControlNet](images/8-enable-openpose.png)

### Import QR Code and Configure Generation

1. Switch to **ControlNet Unit 1**
2. Upload your QR code image
3. Select the model **control_v1p_sd15_qrcode_monster** with a **Control Weight of 1.7**
4. Set **Sampling Steps** to 30–50 for better quality
5. Adjust **Width/Height** to match your desired output resolution

![Enable QR Code Monster](images/9-enable-qr-monster.png)

![Set Width and Height](images/10-set-hw.png)

### Prompts and Generation

Set your prompts for the final generation:

**Positive prompt:**
```text
(1girl:1.6, side lying sleep, on the garden, sunflowers), wooden floor, masterpiece, best quality
```

**Negative prompt:**
```text
extra hands, extra fingers, deformed hands, bad anatomy, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality
```

![Set Prompts](images/11-set-prompt.png)

### Results

Here is the final generated result combining OpenPose and QR code:

![OpenPose + QR Code Result](images/12-openpose-qrcode.png)

**Design notes:** By using composition techniques to shift the viewer's visual focus away from the QR code's core functional area, we can create images that are both aesthetically pleasing and maintain QR code scannability. The key is to avoid placing important visual elements directly over the QR code's positioning markers and data modules.

For comparison, here are the individual components:

| | |
|:---:|:---:|
| ![Lying Sleep Pose](images/13-lying-sleep-openpose.png) | ![OpenPose Skeleton](images/14-openpose.png) |

### Fine-Tuning Tips

To achieve the best results when combining OpenPose with QR codes, consider adjusting:

- **Prompts**: Experiment with different scene descriptions and character poses
- **Sampling method**: Try different samplers (Euler a, DPM++ 2M Karras, etc.)
- **Skeleton structure and position**: Adjust the pose skeleton to avoid overlapping with QR code critical areas
- **Control weight**: Balance between OpenPose (pose accuracy) and QR code (scannability) weights
- **Guidance start/end timing**: Fine-tune when each ControlNet kicks in during the denoising process

## References

- [Stable Diffusion AI Solution MarketPlace](https://aws.amazon.com/marketplace/pp/prodview-ohjyijddo2gka?sr=0-1&ref_=beagle&applicationId=AWSMPContessa)
- [Stable Diffusion AI Solution Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/facdf921-2eea-4638-bc01-522e1eef3dc5)
- [QR Toolkit by Anthony Fu](https://antfu.me/posts/ai-qrcode-101)
- [QRCode Monster - HuggingFace](https://huggingface.co/monster-labs/control_v1p_sd15_qrcode_monster)
- [IoC Lab ControlNet - HuggingFace](https://huggingface.co/ioclab/ioc-controlnet)

---

> Original post: [Art QR Code Generation with ControlNet - AI Painting Solution Based on Stable Diffusion](https://aws.amazon.com/cn/blogs/china/art-qr-code-generation-with-controlnet-ai-painting-solution-based-on-stable-diffusion/)
