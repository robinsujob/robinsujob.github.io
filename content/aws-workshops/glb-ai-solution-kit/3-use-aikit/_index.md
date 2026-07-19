---
title: "3. 体验AI Solution Kit的能力"
weight: 5
type: workshops
---
通过CloudFormation的部署方式，您仅仅使用了15分钟便完成了一整套AI Solution服务的部署。在本章节中，您将使用内置的API资源管理器（Swagger UI）、 Postman或者cURL命令来完成对AI API的调用，以体验AI Solution Kit的能力。

AI Solution提供了在文字识别、人脸与人体、图像理解、视觉内容生产和自然理解五大类，十五项服务，有关各服务的API使用方式，可参考一下链接：

|类别|参数名称|API使用方式|
|:--------:|:-------:|:--------:|
| **文字识别** | General OCR - Simplified Chinese | [通用文字识别（简体中文）](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-general-ocr/)|
|**文字识别**| General OCR - Traditional Chinese |[通用文字识别（繁体中文）](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-general-ocr-traditional/)|
|**文字识别**| Advanced OCR |[高阶文字识别（多语种）](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-advanced-ocr/)|
|**文字识别**| Custom Template OCR |[自定义模板文字识别](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-custom-ocr/)|
|**文字识别**| Car License Plate |[车牌信息识别](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-car-license-plate/)|
|**人脸与人体**|Face Comparison|[人脸相似度比对](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-face-comparison/)|
|**人脸与人体**|Face Detection|[人脸识别](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-face-detection/)|
|**人脸与人体**|Human Attribute Recognition|[人体结构化属性](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-human-attribute-recognition/)|
|**人脸与人体**|Human Image Segmentation|[智能人像分割](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-human-image-segmentation/)|
|**图像理解**|Image Similarity|[图片相似度](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-image-similarity/)|
|**图像理解**|Object Recognition|[通用物体识别](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-object-recognition/)|
|**图像理解**|Pornography Detection|[色情内容审核](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-pornography-detection/)|
|**视觉内容生产**|Image Super Resolution|[图像超分辨率](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-image-super-resolution/)|
|**自然语言理解**|Text Similarity|[文本相似度](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-text-similarity/)|
|**自然语言理解**|Natural Language Understanding|[通用自然语言理解](https://awslabs.github.io/aws-ai-solution-kit/zh/deploy-general-nlu/)|

在上一个章节中，您部署了**高阶文字识别（多语种）、自定义模板文字识别、通用物体识别、通用自然语言理解**，共四个服务。本次实验中，您将对这四个服务进行体验。
___
在开始实验之前，请您了解实验中需要的工具：

可能需要的第三方网页工具如下：

* **上述所有服务中**，API调用过程需要Base64编码格式：
    * 图片转Base64：https://base64.guru/converter/encode/image 
<!-- * **智能人像分割**，返回分割后的Base64图片结果转换为图片：
    * Base64转图片：https://base64.guru/converter/decode/image  -->

可能需要的API调用工具：
* Postman: https://www.postman.com/downloads/ 

此外，本次实验的所有内容皆为您提供了测试样例，您也可以自行选择测试样例。
