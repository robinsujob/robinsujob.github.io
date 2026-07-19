---
title: "3.4 通用物体识别"
weight: 4
type: workshops
---
检测图像中的通用对象主体，返回该对象主体的区域信息与置信度。支持识别300类物体。可应用于IPC图像检测、交通、安防等行业中图像场景的目标检测与跟踪。

#### 3.4.1 API 请求参数说明

* HTTP方法：POST

* 请求参数

|名称|类型|是否必选|说明|
|:-----:|:-----:|:-----:|:-----:|
|url|String|与 img 参数二选一|图像的 URL 地址。支持 HTTP/HTTPS 和 S3 协议。要求图像格式为 jpg/jpeg/png/bmp ，最长边不超过 4096px|
|img|String|与 url 参数二选一|进行 Base64 编码的图像数据|

* 请求示例

```
{
"url": "图像的URL地址"
}
```

```
{
"img": "Base64编码的图像数据"
}
```

#### 3.4.2 开始使用

本节用到的测试样例：/workshops/glb-ai-solution-kit/assets/0-images/object-detection.png

1)	点击API右侧的向下箭头，展开通用物体识别的请求方法。
2)	点击右侧的测试（Try it out）按钮
3)	在Request body中输入以下的请求数据进行测试，并查看测试结果。您也可以将您的图片转换为Base64编码，使用img属性自行选择测试的图片。

```json
{
  "url": "/workshops/glb-ai-solution-kit/assets/0-images/object-detection.png"
}
```

4)	确认格式正确后，点击下方的 **Execute**。
5)	在 **Responses body** 中查看返回的JSON结果。您还可以通过右侧复制或下载按钮保存处理结果。在 **Response headers** 中查看响应头的相关信息。

![image.png](/workshops/glb-ai-solution-kit/assets/3-use-aikit/3.4/3.4-Picture1.png)

![image.png](/workshops/glb-ai-solution-kit/assets/3-use-aikit/3.4/3.4-Picture2.png)
