---
title: "3.3 自定义模板文字识别"
weight: 3
type: workshops
---
客户可自定义OCR模板，提取卡证票据中结构化文字信息，并以键值对应关系的形式展现结果。可应用于卡证票据类图片的结构化识别场景，如物流单据、发票、营业执照、行程单、火车票等。

#### 3.3.1 API 请求参数说明

**添加模板：**

进行自定义模版文字识别之前，您需要通过增加模板API创建模板。为了提高文字识别准确性，请选择与被识别图像细节近似并且文字内容清晰的图片创建模板。同一个模板可以包含多个识别区域。

要创建模板，每个待识别区域都需要指定矩形框的四个坐标点和该区域的名称。以下为示例说明：

1)	按照**左上，右上，右下，左下**顺序分别记录矩形框四个坐标点，并指定该识别区域名称，识别区域示例如下：
```
[[[116, 335], [410, 335], [410, 374], [116, 374]], "手机号码"]
```
2)	请参考增加模板API**请求Body示例**，创建自定义模板，并在创建成功后记录的模板ID。
4)	创建好模板后，首先用原图片和模板ID进行文字识别测试，以确保模板能够准确识别到所需信息。
5)	（可选）如果发现提取信息不完整的情况，请确认坐标点是否标注正确，并适当扩大识别区域重新创建模板。

**重要说明：**

矩形框区域必须完全覆盖要识别的文字内容，请在不遮盖其他识别矩形区域的前提下，在识别区域四边留出足够的容错空间，从而获得准确的识别能力。


**API请求参数说明**

* HTTP 方法: POST

* 请求参数

|名称|类型|是否必选|说明|
|:--------:|:-------:|:--------:|:--------:|
|url|String|与 img 参数二选一|图像的 URL 地址。支持 HTTP/HTTPS 和 S3 协议。要求图像格式为 jpg/jpeg/png/bmp ，最长边不超过 4096px|
|img|String|与 url 参数二选一|进行 Base64 编码的图像数据|
|type|String|是|增加模板需要将 type 指定为 add|
|template|List|是|每个元素为一个待提取区域坐标及其名称，请参考**请求 Body 示例**|

* 请求 Body 示例
```json
{
    "type": "add", 
    "url": "图像的URL地址", 
    "template": [
        [
            [[x1, y1], [x2, y2], [x3, y3], [x4, y4]], "名称"
        ], 
        [
            [[x1, y1], [x2, y2], [x3, y3], [x4, y4]], "识别号"
        ]
    ]
}
```

```json
{
    "type": "add", 
    "img": "Base64编码的图像数据", 
    "template": [
        [
            [[x1, y1], [x2, y2], [x3, y3], [x4, y4]], "名称"
        ], 
        [
            [[x1, y1], [x2, y2], [x3, y3], [x4, y4]], "识别号"
        ]
    ]
}
```

**图片坐标定位工具：**

为了方便用户创建模版，我们提供了一个可视化地创建模版的[工具](https://awslabs.github.io/aws-ai-solution-kit/zh/tools/custom-template/index.htm)。您可以按照以下指导使用：
1) 将本地图片或图片URL上传至自定义模版工具中。

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.3/3.3-Picture1.png)

2) 将鼠标放在上传的图片上，您会看到您的鼠标变成一个“+”号，拖动鼠标您可以用红色的矩形框选择出识别区，如下图所示。

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.3/3.3-Picture2.png)

3) 选择好识别区后，在弹出的窗口中输入识别区域名称，点击**OK**。

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.3/3.3-Picture3.png)

4) 您可以图片在下方的列表中看到当前所有识别区的名称和识别矩形框的四个坐标点，并且自定义模版工具会自动为您生成添加模版的请求body。

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.3/3.3-Picture4.png)

5) 点击**复制结果到剪贴板**，回到API Explorer的页面，您可以直接将请求body粘贴到**Request body**对话框中。

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.3/3.3-Picture5.png)

#### 3.3.2 开始使用

本节用到的测试样例：

模版样例：/aws-workshops/glb-ai-solution-kit/assets/0-images/invoice_template.png

测试样例：/aws-workshops/glb-ai-solution-kit/assets/0-images/invoice_example.png

**添加模板：**

1)	点击API右侧的向下箭头，展开自定义OCR的请求方法。

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.3/3.3-Picture6.png)

2)	点击右侧的测试（Try it out）按钮

3)	在Request body中输入以下的Body请求数据添加模版，此处以发票为例。您也可以使用上面介绍的**图片坐标定位工具**，设计符合自己要求的模版。

```json
{
    "type":"add",
    "url":"/aws-workshops/glb-ai-solution-kit/assets/0-images/invoice_template.png",
    "template":[
        [[[402,356],[1403.78666,356],[1403.78666,408.76666],[402,408.76666]],"购买方"],
        [[[254,1478],[592.76666,1478],[592.76666,1552.78336],[254,1552.78336]],"收款人"],
        [[[227,292],[569.76666,292],[569.76666,338.76666],[227,338.76666]],"机器编号"]
    ]
}
```

4)	确认格式正确后，点击下方的**Execute**

5)	在 **Responses body** 中查看返回的JSON结果。并记录创建好的模版ID

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.3/3.3-Picture7.png)

**测试自定义模版结果：**

1)	在Request body中输入以下的Body请求数据，并**替换模版ID**

```json
{
    "template_id": "templateID",
    "url":"/aws-workshops/glb-ai-solution-kit/assets/0-images/invoice_example.png"
}
```

2)	确认格式正确后，点击下方的 **Execute**

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.3/3.3-Picture8.png)

3)	在 **Responses body** 中查看返回的JSON结果
