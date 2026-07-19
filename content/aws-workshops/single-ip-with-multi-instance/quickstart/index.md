---
title: "快速开始"
weight: 5
type: workshops
---
在开始以下步骤之前，请您确保已经完成[前提条件](/aws-workshops/single-ip-with-multi-instance/prerequisite/)。

请根据您使用的设备系统，选择对应的标签页。


{{% workshop-tabs %}}


{{% workshop-tab title="Mac" %}}

#### 1. 开启命令行终端（Terminal）
请在启动台（Launchpad）中，搜索Terminal，打开终端
![image-20221220212924161](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/mac/terminal.png)

#### 2. 初始化凭证的环境变量

若要进行访问，您需要访问密钥 ID 和秘密访问密钥

根据[部署章节](/aws-workshops/single-ip-with-multi-instance/deploy/#5)中最后输出的密钥结果，替换AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY的内容，并在终端中执行。

```shell
export AWS_DEFAULT_REGION=xx-xxxx-1
export AWS_ACCESS_KEY_ID=AKIAS.....OH4
export AWS_SECRET_ACCESS_KEY=he7Zusj.....AfApQtmUzjZZBY
```

![image-20221220205501047](/aws-workshops/single-ip-with-multi-instance/assets/deploy/output.png)

![image-20221221114939601](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/mac/run-aksk.png)

您也可以通过Profile（命名配置文件）用于在您的设备中记录并区别您的密钥信息。

https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-configure-profiles.html

#### 3. 查找需要连接的实例ID

点击[链接](https://console.aws.amazon.com/ec2/home?#Instances:search=:stack-Name;instanceState=running;v=3;$case=tags:true%5C,client:false;$regex=tags:false%5C,client:false)，进入EC2 Dashboard，查看现在正在运行的实例，请根据实例名称识别并记录需要连接的实例ID。

实例名称后缀的意义为`stack-Name-{您创建CloudFormation堆栈时输入的堆栈名称}`

若没有实例，请确认当前区域，点击屏幕右上角更换区域。

![image-20221221103408950](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/instance-id.png)

#### 4. 修改构建Session Manager隧道（Tunnel）命令

替换下方代码中`i-instanceID`的内容，为上一步需要连接的实例ID编号, 例如`--target i-1234567890123`。

若您需要运行多个Session Manager隧道，请修改`localPortNumber`中的端口号，避免冲突。

```shell
aws ssm start-session --target i-instanceID \
                       --document-name AWS-StartPortForwardingSession \
                       --parameters '{"portNumber":["3389"],"localPortNumber":["9999"]}'
```

#### 5. 运行命令，构建隧道（Tunnel）

在开启的终端中，继续运行上一步的命令，构建会话隧道。

成功后如图所示。

![image-20221221115406272](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/mac/run-start-session.png)

#### 6.使用远程连接（RDP）连接EC2实例

此时您可以开启RDP客户端，输入本机和端口号即可连接通过会话隧道连接至EC2实例中。

例如：127.0.0.1:9999 ，端口号取决于您在构建会话隧道时设定的`localPortNumber`。

![image-20221221115611295](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/mac/rdp.png)

输入用户名和密码，用户名为`Administrator`，密码为您在部署堆栈时，设定的初始化的Windows实例密码。参见[部署章节](/aws-workshops/single-ip-with-multi-instance/deploy/#3)。

![image-20221221115859291](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/mac/rdp-password.png)

#### 7.开启新的会话

若您需要在同一台设备连接多个不同的EC2实例，请重复以上1-6步，并更换第4步的`localPortNumber`端口号避免冲突。

如图所示，已在同一台设备连接了多个不同的EC2实例，且出口IP一致。

![image-20221221132742962](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/mac/rdp-ip.png)


{{% /workshop-tab %}}


{{% workshop-tab title="Windows" %}}


#### 1. 开启命令提示符（CMD）
请在开始菜单中，搜索cmd，打开命令提示符
![image-20221220213423557](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/windows/cmd.png)

#### 2. 初始化环境变量

若要进行访问，您需要访问密钥 ID 和秘密访问密钥

根据[部署章节](/aws-workshops/single-ip-with-multi-instance/deploy/#5)中最后输出的密钥结果，替换AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY的内容，并在终端中执行。

```shell
SET AWS_DEFAULT_REGION=xx-xxxx-1
SET AWS_ACCESS_KEY_ID=AKIAS.....OH4
SET AWS_SECRET_ACCESS_KEY=he7Zusj.....AfApQtmUzjZZBY
```

![image-20221220205501047](/aws-workshops/single-ip-with-multi-instance/assets/deploy/output.png)

![image-20221221121626388](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/windows/run-aksk.png)

您也可以通过Profile（命名配置文件）用于在您的设备中记录并区别您的密钥信息。

https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-configure-profiles.html

#### 3. 查找需要连接的实例ID

点击[链接](https://console.aws.amazon.com/ec2/home?#Instances:search=:stack-Name;instanceState=running;v=3;$case=tags:true%5C,client:false;$regex=tags:false%5C,client:false)，进入EC2 Dashboard，查看现在正在运行的实例，请根据实例名称识别并记录需要连接的实例ID。

实例名称后缀的意义为`stack-Name-{您创建CloudFormation堆栈时输入的堆栈名称}`

若没有实例，请确认当前区域，点击屏幕右上角更换区域。

![image-20221221103408950](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/instance-id.png)

#### 4. 修改构建Session Manager隧道（Tunnel）命令

替换下方代码中`i-instanceID`的内容，为上一步需要连接的实例ID编号, 例如`--target i-1234567890123`。

若您需要运行多个Session Manager隧道，请修改`localPortNumber`中的端口号，避免冲突。

```shell
aws ssm start-session --target "i-instanceID" --document-name AWS-StartPortForwardingSession --parameters "portNumber"=["3389"],"localPortNumber"=["9999"]
```

#### 5. 运行命令，构建隧道（Tunnel）

在开启的终端中，继续运行上一步的命令，构建会话隧道。

成功后如图所示。

![image-20221221125721601](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/windows/run-start-session.png)

#### 6.使用远程连接（RDP）连接EC2实例

此时您可以开启RDP客户端，输入本机和端口号即可连接通过会话隧道连接至EC2实例中。

例如：127.0.0.1:9999 ，端口号取决于您在构建会话隧道时设定的`localPortNumber`。

![image-20221221125838353](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/windows/rdp.png)

输入用户名和密码，用户名为`Administrator`，密码为您在部署堆栈时，设定的初始化的Windows实例密码。参见[部署章节](/aws-workshops/single-ip-with-multi-instance/deploy/#3)。

![image-20221221125946257](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/windows/rdp-password.png)

#### 7.开启新的会话

若您需要在同一台设备连接多个不同的EC2实例，请重复以上1-6步，并更换第4步的`localPortNumber`端口号避免冲突。

如图所示，已在同一台设备连接了多个不同的EC2实例，且出口IP一致。

![image-20221221133049544](/aws-workshops/single-ip-with-multi-instance/assets/quickstart/windows/rdp-ip.png)


{{% /workshop-tab %}}


{{% /workshop-tabs %}}
