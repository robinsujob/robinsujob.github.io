---
slug: "art-qr-code-controlnet-stable-diffusion"
title: "Art QR Code with ControlNet and Stable Diffusion"
date: 2023-09-01
description: "Generate artistic QR codes using ControlNet and Stable Diffusion."
categories:
  - AI/ML
tags:
  - stable-diffusion
  - controlnet
  - qr-code
  - art
---


## Background

In the past few months, AWS has published multiple blog posts on deploying Stable Diffusion on AWS, or combining Amazon SageMaker with Stable Diffusion for model training and inference tasks.

To help customers quickly and securely build, deploy, and manage applications on AWS, numerous partners work closely with AWS. They provide a wide range of services, deep technical knowledge, best practices, and solutions, including infrastructure migration, application modernization, security and compliance, data analytics, machine learning, AI, cloud hosting, DevOps, consulting, and training.

Recently, AWS Premier Tier Services Partner eCloudrover launched an AI painting solution based on Stable Diffusion called imAgine, featuring extensively validated and easily deployable advanced AI algorithm models, along with rich and cost-effective cloud resources to optimize costs, aiming to help industries such as gaming, e-commerce, media, film, advertising, and communications rapidly build AIGC application pipelines and create leading productivity in the AI era.

This post mainly shares practical experience we've summarized while helping customers use Stable Diffusion, as well as best practices for generating artistic QR codes using the imAgine product developed based on Stable Diffusion.

We will use QR codes as ControlNet input, integrating QR code data points into artistic images while still being scannable by QR code readers. With this technology, you can transform any QR code into a unique work of art, expressing and conveying information in a completely new way. Here are some example images:

![Sample 1](images/sample1.jpg)
![Sample 2](images/sample2.jpg)
![Sample 3](images/sample3.jpg)

## Stable Diffusion Practical Tips

As the old saying goes: "The first step is always the hardest" and "Reach for the broad while attending to the fine details." This corresponds to the two most common issues customers encounter in Stable Diffusion practice: first, how to choose appropriate prompt starters to generate images that meet expectations; and second, how to optimize image details so that the final output meets production application requirements.

Based on our past experience serving customers using Stable Diffusion, we've compiled the following content as our recommended best practices, hoping to provide reference for readers creating with Stable Diffusion.

### Prompt Engineering

As Stable Diffusion versions continue to iterate and AI's understanding of semantics gets closer to "common sense," the requirements for prompts also increase. Many misconceptions about prompts can sometimes have adverse effects on image generation.

#### Basic Concepts of Prompts

Prompts are divided into positive prompts and negative prompts, used to tell the AI what is needed and what is not.

#### Common Prompt Misconceptions

- Precision over quantity; short words beat natural language.
- Quality descriptors should not be mindlessly stacked.
- Prompts are about precision, not quantity; using the shortest words to describe the scene is more effective than natural language. Quality-improving descriptors should not be mindlessly stacked. Common starters like "masterpiece" and "best quality" often become dead weight in prompts. These words were meaningful in the NovelAI era when they were heavily used for image evaluation during training, but now, after model authors on Civitai continuously refined models, these prompts can barely show their intended effect in generated results.

#### Adjusting Prompt Weights

- Default weight is 1, decreasing left to right
- Prompt weights significantly affect results
- Use parentheses + colon + number for weights, e.g. `(one girl:1.5)`

The default weight of each token is 1, decreasing from left to right. Prompt weights significantly affect the generated image. You can specify prompt weight using parentheses + colon + number, e.g., `(one girl:1.5)`.

#### Mind the Prompt Order

- Landscape tags first = smaller characters
- Correct order and syntax produce better results

For example, if landscape tags come first, the character will be small; conversely, the character will be larger or shown as half-body. Choosing the correct order and syntax for prompts will more effectively render the desired scene.

#### Emojis in Prompts

- Emojis work well for expressions
- Prioritize emojis over complex syntax

Prompts support emojis with good expressiveness. For specific facial expressions or actions, you can achieve the desired effect by adding emoji. To prevent semantic drift, prefer emoji and minimize unnecessary complex syntax like "with".

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

Often we generate an image that's not quite satisfactory and want to further optimize it, but don't know where to start. Here are some best practices for image parameter tuning:

#### Which Parameters to Adjust

- **CFG Scale**: The correlation between the image and the prompt. Higher values mean greater influence of the prompt on the final result.
  - CFG 2-6: Creative but may be too distorted. Fun for short prompts.
  - CFG 7-10: Recommended for most prompts. Good creativity-guidance balance.
  - CFG 10-15: Use when prompt is detailed and clear.
  - CFG 16-20: Generally not recommended. May affect quality.
  - CFG >20: Almost unusable.
- **Sampling Steps**: More steps mean smaller and more precise adjustments per step, but proportionally increase generation time. For most samplers, more iterations yield better results, but beyond 50 steps the improvements become negligible.
- **Sampling method**: Different sampling methods have different optimal step counts.
  - Euler a: Creative, good for quick prompt testing.
  - DPM2 a Karras: Good for realistic models, hard to control after 30 steps.
  - DPM++ 2M Karras: Excellent at high step counts, more details.
  - DDIM: Fast convergence but needs many steps; good for inpainting.
  - Different model and sampler combinations produce different results; use X/Y/Z plots for comparison.
- **Seed**: The random seed often has a huge impact on composition and is the main source of randomness in SD image generation. With the same seed, prompts, model, and all parameters, the same seed can generate (nearly) identical images multiple times. When you've found a suitable composition, fixing the seed and fine-tuning details is the best approach.

#### How to Find Optimal Parameters

Use X/Y/Z plots to find optimal parameters: By using X/Y/Z plots, we can clearly compare results under different parameters, quickly locate suitable parameter ranges, and perform further generation control.

![X/Y/Z Plot Comparison](images/image4.jpg)

#### Image Size Optimization

- Quality is not directly tied to size.
- Size influences subject category/content because it implicitly represents the category (e.g., portrait for vertical, landscape for horizontal, small resolution for stickers).
- Too wide may produce multiple subjects.
- Image quality is not directly tied to image size. However, size somewhat affects the subject/content, as it implicitly represents the category (e.g., portrait for vertical, landscape for horizontal, small resolution for stickers). When the output size is too wide, multiple subjects may appear. Sizes above 1024 may produce undesirable results with significant GPU memory pressure. Small resolution + upscaling is recommended.

#### Optimizing Multi and Wide Character Generation

- txt2img alone cannot specify individual features in multi-character scenes.
- Recommended: draft + img2img or ControlNet.
- For wide-format single-character generation, draft a sketch with color blocking to determine the main subject, or use ControlNet's OpenPose for character skeleton.
- For multi-character scenes, use ControlNet's OpenPose to specify character count; this also works for three-view drawings of the same character.

Using txt2img alone cannot effectively specify individual character features in multi-character scenarios. The recommended approach is to create a draft + img2img or ControlNet. For wide-format single-character generation, draft a sketch with color blocking to determine the main subject, or use ControlNet's OpenPose for character skeleton. For multi-character scenes, use ControlNet's OpenPose to specify character count; this also works for three-view drawings of the same character.

#### Hand Repair

- Send the image to img2img inpaint with similar prompts, placing "hand" prompts at the front. Set denoising strength based on how much you want hand features to change (below 0.25 for just completeness). For more precise hand control, find a satisfactory hand reference image and use ControlNet's Canny or OpenPose_hands preprocessor + model combined with inpaint.

#### Face Repair

When drawing images with small character subjects, facial distortion frequently occurs. Especially in the artistic QR code generation process described later, faces often break due to QR code data points. For facial inpainting, the ADetailer plugin is recommended. It uses YOLO algorithm for object detection, identifies faces, and performs localized inpainting with specified prompts and models. ADetailer can handle both face and hand detection and repair, and can also reference LoRA models for localized inpainting.

![ADetailer Face Repair](images/image5.jpg)

## Generating Artistic QR Codes with ControlNet

### Step 1: Optimize the QR Code

A QR code is a pattern of black and white geometric shapes distributed in 2D space that records symbolic data information. There are multiple encoding methods for QR codes; we use the most universal and basic encoding method: QR Code.

The input QR code is one of the most important parts of generating artistic QR codes with SD. We mainly care about two characteristics of the input QR code:

![QR Code Structure](images/image6.jpg)

1. Information contained in the QR code

Regardless of the encoding method, the more character information a QR code carries, the more complex its visual black-and-white structure becomes. Complex structures can greatly constrain artistic creativity during generation. Therefore, we first need to simplify the character length contained in the QR code.

For the most common use case, QR codes usually contain a web link. To improve the aesthetics of the generated QR code, we first need to shorten the URL. There are many URL shortening tools available. Note that within mainland China, choose platforms with registered domain names, otherwise they may be blocked by WeChat, browsers, etc.

![URL Length Comparison](images/image7.jpg)

2. How the QR code is presented

With technological development, QR codes no longer only support black and white square patterns; both positioning points and modules support diverse presentation styles.

In practice, we can try different module styles to achieve the desired image generation effect. The following image shows how different QR code styles affect the final result:

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

After understanding the above key points, we will start using QR code generation tools to create a base QR code for SD input. There are many web-based QR code generators available. For your convenience, we've pre-installed a QR code generation plugin in the blog-dedicated AMI:

- **Anthony's QR Toolkit**: Integrated QR code generation and optimization tool in Webui
  - [https://github.com/antfu/sd-webui-qrcode-toolkit](https://github.com/antfu/sd-webui-qrcode-toolkit)

![QR Toolkit Configuration](images/image10.jpg)

After creating the QR code, you can click "Download" on the right to save it locally, or click "Send to ControlNet" to send it directly to ControlNet for the next step.

### Step 3: Determine the Art Style

The core of creating art with Stable Diffusion is choosing the right model + prompts. Before creating artistic QR codes, we recommend first generating an image without ControlNet to test the generation effect.

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

After confirming the image style, we upload the unprocessed QR code to ControlNet. Pay attention to the following configuration options:

- **"Enable" button**: Check to ensure ControlNet is active during generation
- **Model selector**: Select "control_v1p_sd15_qrcode_monster" to strengthen QR code control
- **Control weight**: For qrcode_monster model, we recommend setting between 1.1-1.6
- **Guidance start/end timing**: Start timing recommended between 0-0.1, end timing recommended at 1

![ControlNet Configuration](images/image12.jpg)

In txt2img configuration, we recommend adjusting two sets of values:

- **Sampling steps**: recommended 30-50, default 20 is insufficient for high-quality QR code images
- **Width/Height**: recommended to send the original QR code aspect ratio from ControlNet

![txt2img Parameter Adjustment](images/image13.jpg)

After all parameters are configured, click generate. Here we can see a good result — the QR code passes scanning tests on mobile phones.

If the generated QR code doesn't meet expectations, try fine-tuning the following parameters and increasing the total batch count:

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

For your convenience, we have pre-installed ControlNet QR Code models in the blog-specific AMI. You can directly select the model in ControlNet as long as you launch the AMI from the correct version.

To date, **QRCode Monster** is the model we've found to have the highest QR code control success rate and best image fusion effect. It can be downloaded from HuggingFace:

- [QRCode Monster - HuggingFace](https://huggingface.co/monster-labs/control_v1p_sd15_qrcode_monster)

There is also another QR code model: **QR Pattern v2.0**. We recommend using it with IoC Lab's Brightness model as an auxiliary model to improve local contrast. However, based on our testing, this model introduces more interference that may significantly alter the image style. These models can be downloaded from:

- [QR Pattern v2.0 - Civitai](https://civitai.com/models/90940/controlnet-qr-pattern-qr-codes)
- [IoC Lab ControlNet - HuggingFace](https://huggingface.co/ioclab/ioc-controlnet)

### Appendix 2: How to Use the Stable Diffusion AI Drawing Solution

imAgine is an AI drawing solution developed by AWS core-level service partner eCloudrover, based on Automatic1111 Stable Diffusion WebUI and integrated with multiple AWS managed services. imAgine is now available on AWS MarketPlace for one-click subscription and rapid deployment without complex environment configuration.

It also integrates with AWS serverless services like Amazon API Gateway and DynamoDB, seamlessly forwarding training and inference requests from the WebUI frontend to dedicated SageMaker backend servers, enabling seamless compute scaling and precise cost management.

For detailed steps to subscribe to the imAgine solution, please refer to the Workshop page: [imAgine Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/facdf921-2eea-4638-bc01-522e1eef3dc5)

## References

- [Stable Diffusion AI Solution MarketPlace](https://aws.amazon.com/marketplace/pp/prodview-ohjyijddo2gka?sr=0-1&ref_=beagle&applicationId=AWSMPContessa)
- [Stable Diffusion AI Solution Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/facdf921-2eea-4638-bc01-522e1eef3dc5)
- [imAgine Official Website](https://www.ecloudrover.com/aigc/)
- [QR Toolkit Co-creation Document by Anthony Fu](https://antfu.me/posts/ai-qrcode-101)
- [IoC Lab Model Showcase](https://mp.weixin.qq.com/s/i4WR5ULH1ZZYl8Watf3EPw)
- [IoC Lab Stable Diffusion Documentation](http://aigc.ioclab.com/)



Original post: [Art QR Code Generation with ControlNet - AI Painting Solution Based on Stable Diffusion](https://aws.amazon.com/cn/blogs/china/art-qr-code-generation-with-controlnet-ai-painting-solution-based-on-stable-diffusion/)

