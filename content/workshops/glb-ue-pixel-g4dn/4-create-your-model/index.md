---
title: "4.创建UE演示项目"
weight: 5
type: workshops
---
在本节中您将在Windows实例中创建您的UE演示项目，并完成使用UE虚幻引擎完成演示项目的创建、设置以及调试。此外，您还需要将演示项目上传至Github中，以方便Linux实例创建容器所需。


{{% workshop-alert type="info" %}}
以下操作将在Windows EC2实例上操作
{{% /workshop-alert %}}


#### 1. 启动UE引擎

请您连接到Windows EC2实例的，启动UE引擎

![image-20221109092116180](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/1-create-project/1-launch-ue.png)

#### 2.选择项目类型

本次项目选择游戏类型，选择的完毕后点击下一步（Next）。

![image-20221108184055835](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/1-create-project/2-create-game.png)

#### 3.选择一个模版项目

您可以选择您喜好的模版项目，本次动手训练营推荐选择第一人称视角类的项目。

![image-20221108184210944](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/1-create-project/3-select-template.png)

#### 4.项目设置

在项目设置阶段，请选择不包含**初学者内容**，这将节省您整个的项目大小空间。

**为该项目命名**（不要使用中文），其他配置保持默认，点击绿色“创建项目”按钮。

![image-20221109092804228](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/1-create-project/4-project-setting.png)

#### 5.UE编辑器语言切换

选择菜单栏中的“Edit” -> "Editor Preferences"。选择“Region & Language"，随后在“Editor Language”选择“Chinese (Simplified)”

![image-20221109100501797](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/1-create-project/5-change-language.png)

#### 6. 开启像素流送插件

为该项目开启**像素流送**，通过像素流送在云端服务器上运行虚幻引擎应用程序，通过WebRTC将渲染的帧和音频流送到浏览器和移动设备。访问者通过任意现代网络浏览器进行连接（电脑版或移动版），并从虚幻引擎应用程序流送渲染的帧和音频。不需要使用者安装或下载其他内容。

**选择菜单中的”编辑“->"插件"，在搜索框上搜索“Pixel Streaming"，勾选“启用”，并重启UE引擎**。

![image-20221109140131608](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/1-create-project/6-open-streaming.png)

#### 7.开启辅助摇杆

为该项目开启辅助摇杆，这将帮助您在使用手机等移动平台时方便操控。

**选择菜单中的”编辑“->"项目设置"，在左侧找到“引擎”下的“输入”，在右侧移动平台标签页中开启“固定显示触控界面”**。完成设置后，保存该项目。

![image-20221109143451534](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/1-create-project/7-enable-rocker.png)

#### 8.在Windows实例中体验项目

您已经基本完成在Windows中创建、调试UE演示项目的过程，您可以点击“运行”按钮，体验该项目。

![image-20221109145930035](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/1-create-project/8-run-project.png)

#### 9.创建Github仓库

在连接的Windows EC2实例的Edge浏览器中打开以下网址，以创建一个新的Github仓库。

```api
https://github.com/new
```

此处仅填写名称即可，在页面底部，点击绿色“Create Repository”

![image-20221109160247284](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/2-upload-repo/1-create-repo.png)

#### 10.上传UE演示项目文件至仓库

创建Github仓库之后应看到如下页面，请点击“uploading an existing file"

![image-20221109161544798](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/2-upload-repo/2-upload-file.png)

随后，选择您的项目文件。它应该在`C:\Users\Administrator\Documents\Unreal Projects`。请进入到文件夹中，拖拽其中的所有文件至浏览器中。*注意：该方式拖拽只能最多支持100个文件，若超出限额，可以分批上传。*

![image-20221109165955253](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/2-upload-repo/2-drop-file.png)

点击页面底部绿色“Commit changes“提交上传的文件。

![image-20221109171344862](/workshops/glb-ue-pixel-g4dn/assets/4-create-your-model/2-upload-repo/3-commit-file.png)


{{% workshop-alert type="success" title="恭喜您！" %}}
您已经完成在完成在Windows中创建、调试UE演示项，并您的UE项目文件上传至Github中，在下一章节您将使用Linux实例部署您的UE演示项目！
{{% /workshop-alert %}}
