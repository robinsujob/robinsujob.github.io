---
title: "3.2 高阶文字识别（多语种）"
weight: 2
type: workshops
---
通用场景文字提取，通过返回在图片中文字内容与坐标位置等信息，便于客户进行比对或结构化操作。支持识别**简体中文、繁体中文、越南语、日语、韩语、英文、数字和常用符号**。可应用于纸质文档电子化，证件识别，内容审核等多种场景，大幅提高信息处理效率。

#### 3.2.1 API 请求参数说明

* HTTP 方法：POST

* 请求参数：

|名称|类型|是否必选|说明|
|:--------:|:-------:|:--------:|:--------:|
|url|String|与 img 参数二选一|图像URL地址。支持HTTP/HTTPS和S3协议。要求图像格式为 jpg/jpeg/png/bmp，最长边不超过 4096px|
|img|String|与 url 参数二选一|进行 Base64 编码的图像数据|

* 请求示例：
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

#### 3.2.2 开始使用
本节用到的测试样例：/aws-workshops/glb-ai-solution-kit/assets/0-images/CN_EN_JP_VN_welcome.png

1)	点击API右侧的向下箭头，展开高阶OCR的请求方法

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.2/3.2-Picture1.png)

2)	点击右侧的测试（Try it out）按钮

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.2/3.2-Picture2.png)

3)	测试模型对**简体中文+英文+日文+越南语**的识别能力：在Request body中输入以下的请求数据进行测试，并查看测试结果。您也可以将您的图片转换为Base64编码，使用img属性自行选择测试的图片
```json
{
  "url": "/aws-workshops/glb-ai-solution-kit/assets/0-images/CN_EN_JP_VN_welcome.png"
}
```
4)	确认格式正确后，点击下方的**Execute**

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.2/3.2-Picture3.png)

5)	在**Responses body**中查看返回的JSON结果。您还可以通过右侧复制或下载按钮保存处理结果。在**Response headers**中查看响应头的相关信息

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.2/3.2-Picture4.png)
