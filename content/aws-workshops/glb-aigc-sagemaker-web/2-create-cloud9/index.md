---
title: "2.在 AWS Cloud9 创建前后端 Web 应用"
weight: 4
type: workshops
---
AWS Cloud9 是一种基于云的集成开发环境 (IDE)，您只需要一个浏览器，即可编写、运行和调试代码。它包括一个代码编辑器、调试程序和终端，并且预封装了适用于 JavaScript、Python、PHP 等常见编程语言的基本工具，您无需安装文件或配置开发计算机，即可开始新的项目。

在本节中，您将创建一个 Cloud9 环境并导入用于本次动手训练营的 web 应用代码。

#### 1. 进入 Cloud9 服务

在查找服务处搜索 Cloud9，并点击进入服务面板。

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/1-cloud9.png)

#### 2. 创建 AWS Cloud9 环境

点击右上角橙色”Create environment“按钮。

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/2-create-env.png)

在 **Create environment** 界面的，为您的 AWS Cloud9 环境分配一个账户内唯一且符合命名要求的名称。可以命名：**Text-To-Image-Web-App**

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/3-env-name.png)

其他部分配置保持默认，在页面底部点击橙色的 **Create** 按钮创建环境。 环境的创建将花费1-2分钟的时间。

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/4-create.png)

#### 3. 进入 AWS Cloud9 环境

在 AWS Cloud9 主页面**Environments**列表里，点击 **Open** 打开创建的环境。

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/5-open-cloud9-env.png)

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/6-cloud9.png)

#### 4. 下载/上传 Web 应用

在 Cloud9 下方的控制台中输入以下指令下载保存Web应用程序代码压缩文件，并将该压缩文件进行解压。

```shell script
cd ~/environment
wget /aws-workshops/glb-aigc-sagemaker-web/assets/code/SampleWebApp.zip
unzip SampleWebApp.zip
```

解压后您将得到 **SampleWebApp** 文件夹。该文件夹包含以下内容：

- 后端代码 app.py：接收前端请求并调用 SageMaker Endpoint 将文字生成图片。
- 两个前端html文件 image.html 和 index.html。

#### 5. 在 AWS Cloud9 上安装 Flask 和 boto3

在Cloud9下方的控制台中输入指令安装 Flask。

```shell script
pip3 install Flask
```

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/9-install-flask.png)

输入指令安装 boto3。

```shell script
pip3 install boto3
```

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/10-install-boto3.png)

#### 6. 运行 app.py

在左侧项目文件夹中打开 app.py。

如果您在 Notebook 部署 endpoint 的环节修改过 endpoint 名称，请在 app.py **endpoint_name = "stable-diffusion-v1-5-endpoint"** 处将名称修改为您所定义的名称，并将修改内容进行保存。如果未做任何修改，可保持默认内容不变。

点击 AWS Cloud9 上方的 Run 按钮运行代码。

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/11-run.png)

在控制台会显示如下信息表示成功运行。

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/12-run-8080.png)

#### 7. preview 前端 Web 页面

为方便大家体验，本实验使用了8080端口，通过使用AWS Cloud9 的 preview 功能预览网页进行体验。关于 AWS Cloud9 预览应用程序功能的详细介绍可以参考：[预览正在 AWS Cloud9 集成开发环境 (IDE) 中运行的应用程序](https://docs.aws.amazon.com/zh_cn/cloud9/latest/user-guide/app-preview.html)

在 AWS Cloud9 环境中点击 Run 按钮左侧的 **Preview**。

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/16-clik-preview.png)

接下来，在下拉菜单中点击 **Preview Running Application**。

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/17-preview-app.png)

点击后， AWS Cloud9 环境中将会打开本次实验提供的 web 页面。

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/13-web.png)

注：如果您希望在互联网上运行应用程序，可以参考[通过互联网共享运行的应用程序](https://docs.aws.amazon.com/zh_cn/cloud9/latest/user-guide/app-preview.html#app-preview-share)进行配置

#### 8. 输入信息生成图片

在 Web 页面可以通过自定义图片长度和宽度，以及在 Prompt 输入框处输入语句或描绘性词汇生成图片。
不同图片的语句请用分号";"间隔。

在输入语句时，您可以尽可能的完善您的语句，以便AI绘制出的图片更贴合您的预期。
比如，通过描述性词语，如 cartoon style、van gogh style、realistic 表明图片的整体风格。

如，可将长度和宽度都设置成512，输入以下描绘性语句生成一张卡通风格的宇航员猴子图片，以及一张超级英雄的图片。

```shell script
a cartoon style cute monkey wearing a space suit, star background; clear portrait of a superhero concept between spiderman and batman, cottagecore
```

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/14-preview.png)

![image-1](/aws-workshops/glb-aigc-sagemaker-web/assets/2-create-cloud9/15-image.png)
