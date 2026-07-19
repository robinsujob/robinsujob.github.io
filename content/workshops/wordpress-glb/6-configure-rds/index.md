---
title: "6. 配置RDS数据库"
weight: 8
type: workshops
---
在此模块中，您将配置 RDS 数据库以允许特定实体访问数据库。保护数据库免遭未经授权的访问至关重要，您可以使用多种策略来增强您数据库的安全性。您将在本模块中学习到其中的一种方法：“网络安全性”，通过拒绝来自未经授权的IP地址的流量，实现对数据库实例的访问限制。

以下步骤将引导您配置这种方法。要完成本模块中的步骤，您需要通过 SSH或者会话连接器 访问 EC2 实例。如果您需要通过重新连接到 EC2 实例，请查看前面模块中的步骤。

#### 6.1 安装 telnet 指令

为了更好的让您理解网络安全性，本模块中需要telnet指令用于测试。请在会话窗口执行如下安装命令

```shell
sudo yum install -y telnet
```

![image-1](/workshops/wordpress-glb/assets/6-configure-rds/6-Picture1.png)

#### 6.2 记录 RDS 数据库主机名 

接下来，请在[RDS 数据库](https://ap-northeast-1.console.aws.amazon.com/rds/home?region=ap-northeast-1#databases:)中找到并记录RDS 数据库的主机名。

在RDS控制台中，点击对应实例名称。在 RDS 数据库的详细信息中，主机名在连接性和安全性部分中显示为终端节点。**请确保数据库状态为可用，并在记事本记录数据库终端节点地址**。

![image-2](/workshops/wordpress-glb/assets/6-configure-rds/6-Picture2.png)

#### 6.3 测试 RDS 数据库端口是否可达 

在终端中输入以下命令，以测试RDS数据库端口是否可达。例如：telnet db-instance.xxx.rds.ap-northeast-1.rds.amazonaws.com 3306

```shell
telnet 您的数据库终端节点地址 3306
```

![image-3](/workshops/wordpress-glb/assets/6-configure-rds/6-Picture3.png)

长时间无反应，说明现在RDS的3306端口不可达，`Control / Ctrl +C`，中断该指令。

**解释：长时间无反应的原因是WordPress EC2 实例不在RDS数据库的安全组中，因此它无权访问 RDS 数据库。后续步骤将允许您的 EC2 实例访问 RDS 数据库**

#### 6.4 允许您的 EC2 实例访问 RDS 数据库

在之前创建EC2的模块，您创建了安全组规则，允许 SSH 和 HTTP 流量访问您的 WordPress EC2 实例。此处适用同样的原则。但是这一次您希望允许某些流量从 EC2 实例访问 RDS 数据库。

要进行配置，请在新的标签页打开[RDS 数据库](https://ap-northeast-1.console.aws.amazon.com/rds/home?region=ap-northeast-1#databases:)控制台。单击您在本实验先前的模块中创建的 MySQL 数据库。在安全组规则区域点击安全组条目。

![image-4](/workshops/wordpress-glb/assets/6-configure-rds/6-Picture4.png)

#### 6.5 选择安全组入站规则

单击入站规则选项卡，然后单击编辑入站规则更改安全组规则

![image-5](/workshops/wordpress-glb/assets/6-configure-rds/6-Picture5.png)

#### 6.6 更改安全组入站规则

单击入站规则选项卡，然后单击编辑入站规则更改安全组规则

默认安全组设有一个规则，该规则在建立RDS数据库时根据您的IP地址生成。但是，由于您的 WordPress EC2 实例不在该安全组中，因此它无权访问 RDS 数据库。

删除自动创建的安全组规则。点击左下角“添加规则”按钮，创建一条新的规则，在类型中选择MySQL/Aurora。在源后的输入栏中输入 **wordpress-sg**，并选择对应的安全组。点击右下角的“保存规则”按钮。

![image-6](/workshops/wordpress-glb/assets/6-configure-rds/6-Picture6.png)

![image-7](/workshops/wordpress-glb/assets/6-configure-rds/6-Picture7.png)

![image-7](/workshops/wordpress-glb/assets/6-configure-rds/6-Picture8.png)

#### 6.7 执行 telnet 指令测试连接

回到会话窗口（会话管理器/SSH终端），再次执行telnet指令，看到提示mysql_native_password等信息代表RDS的安全组配置成功

```shell
telnet 您的数据库终端节点地址 3306
```
![image-8](/workshops/wordpress-glb/assets/6-configure-rds/6-Picture9.png)

在本模块中，您学习了如何为 RDS 数据库配置网络安全性。现在，您的 EC2 实例可以通过网络访问 RDS 数据库。

在下一个模块中，您将通过IP地址对WordPress进行配置。
