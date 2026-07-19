---
title: "0.简介与前提条件"
weight: 2
type: workshops
---
通过本次动手训练营，您将了解到以下关于imAgine解决方案的特点：

- 基于SD Webui开箱即用的 AIGC 文生图/图生图平台
- 服务启动后直接通过公网IP地址即可进入产品操作页面
- 预制SD v1.5模型与常见的ControlNet模型，免除下载苦恼
- 预制中英双语界面更符合中国客户的体验
- 直接通过浏览器下载、管理模型，支持WebUI安装所需插件

该解决方案架构组成如下：

![](/workshops/glb-aigc-ami-workshop/assets/0-prerequisites/1.Architecture.png)

本次动手训练营您将通过imAgine解决方案中Stable Diffusion Webui与ControlNet体验到以下能力：

- 生成艺术二维码
- 使用Openpose优化人物二维码
- 生成艺术字照片

---

#### 前提条件

本方案需要使用[加速计算实例](https://aws.amazon.com/cn/ec2/instance-types/#Accelerated_Computing)完成，若您希望完整体验本次动手训练营，请确保您有足够的限额。

本次动手训练营将在**美国东部 (弗吉尼亚北部) us-east-1**区域中完成，需要的服务类型有：

- **EC2:**  `g4dn.2xlarge` 或 `g5.2xlarge`

#### 检查EC2并提升加速计算实例限额

请点击链接：https://us-east-1.console.aws.amazon.com/servicequotas/home/services/ec2/quotas?region=us-east-1

在搜索框中输入`Running On-Demand G and VT instances`

若您`Running On-Demand G and VT instances`行，第二列已应用的配额值小于8，请继续以下步骤

![](/workshops/glb-aigc-ami-workshop/assets/0-prerequisites/2.Limit-Check.png)

**填写提升限额**: 请确保当前要提升限额的区域为您所需的区域，然后填写所需的配额值，例如“8“，然后点击橙色”请求“按钮提交。

![](/workshops/glb-aigc-ami-workshop/assets/0-prerequisites/3-submit-request.png)

请求完成后，您可以点击左侧”**配额请求历史记录**”，可以在此处看到提交的请求历史和状态

![](/workshops/glb-aigc-ami-workshop/assets/0-prerequisites/4-check-request.png)

点击请求的状态，可以看到一个纯数字的工单编号，您可以将该编号提供给您的伊克罗德商务经理或亚马逊云科技商务经理。

![](/workshops/glb-aigc-ami-workshop/assets/0-prerequisites/5-ticket-info.png)

点击工单编号，会跳转到工单的通信界面，如果您的配额请求遇到问题，可以在此处和亚马逊云的后台支持工程师取得联系

![](/workshops/glb-aigc-ami-workshop/assets/0-prerequisites/6-contact-support.png)


{{% workshop-alert type="info" %}}
提交完成您也可以联系您的销售代表，帮助您跟踪限额提升进度。
{{% /workshop-alert %}}
