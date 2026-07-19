---
title: "3.4在Epic Games 网站上关联GitHub账号"
weight: 4
type: workshops
---
若要在Linux容器化UE项目，您需要将Epic账户与Github账户进行关联，以使用基于Epic提供官方的基础镜像。在本节中您将完成在Epic Games网站上将Epic账号与上GitHub账号关联。


{{% workshop-alert type="info" %}}
以下操作将在Windows EC2实例上操作
{{% /workshop-alert %}}


#### 1. 登录并关联Github账户

在连接的Windows EC2实例中，在浏览器中打开以下网址（EPIC个人信息页），登录至EPIC账户：

```apl
https://www.epicgames.com/account/connections?lang=zh-CN&productName=epicgames
```

登录完成后，点击左侧菜单“连接”，选择“账户“标签，最后点击Github下的连接按钮。

![image-20221106165641643](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-3-connect-epic/3-1-user-info.png)

随后点击“关联”按钮，在弹出的标签页中输入您的Github账号用户名及密码

![image-20221106170823416](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-3-connect-epic/3-2-login-epic.png)

#### 2.访问EPIC Games私有仓库

在浏览器中打开以下网址，以验证Github与Epic账户关联成功

```api
https://github.com/EpicGames/UnrealEngine
```

![image-20221106183307387](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-3-connect-epic/3-3-epic-org.png)

若已看到如图页面，则代表Github与Epic账户关联成功。

#### 3.创建Github Access Token

您还需创建Github Access Token以能够在Linux中通过docker命令拉取UE引擎的基础镜像。

在浏览器中打开以下网址，以可以生成Github Access Token。

```api
https://github.com/settings/tokens/new
```

在Note处为Token命名，仅选择`read:packages`选项，并点击页面最下方绿色***Generate token***按钮。

![image-20221106185759509](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-3-connect-epic/3-4-gen-token.png)

请记录生成的Github Access Token，Access Token会在下一节用到。

![image-20221106190109436](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-3-connect-epic/3-5-token.png)


{{% workshop-alert type="success" title="恭喜您！" %}}
您已经成功将Epic账户与Github关联，并生成所需的Access Token。
{{% /workshop-alert %}}
