---
title: "2. 借助ControlNet进行AI绘画创作"
weight: 4
type: workshops
---
AIGC 的可控性是它进入实际生产最关键的一环。在此之前，许多用户希望 AI 生成的结果尽可能符合要求，但都不尽如人意。ControlNet 提供一个新的神经网络概念，该网络可以控制Stable Diffusion模型并让Stable Diffusion模型支持更多的输入条件。原始的SDStable Diffusion能接受prompt以及source  image的输入，ControlNet提供了包括canny边缘，语义分割图，姿态识别，涂鸦在内的多种输入条件，拓展了Stable Diffusion的能力边界，使得AI绘画的可控性大幅提高。

imAgine在Stable Diffusion Webui中预装了ControlNet插件以及模型，您可以通过使用 ControlNet 预处理器和 ControlNet 模型，来进行您的创作。

![](/workshops/glb-aigc-ami-workshop/assets/2-controlnet/1-controlnet.png)

本次动手训练营您将通过利用ControlNet体验到以下能力：

- 生成艺术二维码
- 使用Openpose优化人物二维码
- 生成艺术字照片

ControlNet提供多种模型选择，每一种模型对图片的关注不同，例如一些是关注主体边缘，一些是关注建筑线条，一些是关注人物姿势等：

| 模型名称      | 对应模型         | 模型描述                                     |
| ------------- | ---------------- | -------------------------------------------- |
| canny         | control_canny    | 边缘检测                                     |
| depth         | control_depth    | 深度检测                                     |
| hed           | control_hed      | 边缘检测但保留更多细节，适合重新着色和风格化。 |
| mlsd          | control_mlsd     | 线段识别，识别人物功能极差，非常适合建筑。     |
| normal_map    | control_normal   | 根据图片生成法线贴图，适合CG建模师。       |
| openpose      | control_openpose | 提取人物骨骼姿势                             |
| openpose_hand | control_openpose | 提取人物+手部骨骼姿势                        |
| scribble      | control_scribble | 提取黑白稿                                   |
| fake_scribble | control_scribble | 涂鸦风格提取                                 |
| segmentation  | control_seg      | 语义分割                                     |

*注意：目前ControlNet是AI绘画界的热点，其更新速度极快，考虑到时效性，仅作当前参考*
