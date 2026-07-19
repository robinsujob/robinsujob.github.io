---
title: "使用的前提条件"
weight: 4
type: workshops
---
#### 安装AWS CLI

在使用System Manager构建端口转发隧道，连接EC2实例之前，请确保您已经安装了AWS CLI。AWS 命令行界面（AWS CLI）是用于管理 AWS 产品的统一工具。更多请参考：https://aws.amazon.com/cn/cli/

- **Windows**：下载并运行 [64 位](https://awscli.amazonaws.com/AWSCLIV2.msi) Windows 安装程序。
- **MacOS**：下载并运行 [MacOS PKG](https://awscli.amazonaws.com/AWSCLIV2.pkg) 安装程序。

**验证 AWS CLI安装**

运行以下命令验证是否已成功安装 AWS CLI。

```shell
aws --version
```

如果安装成功，将返回类似消息。

```shell
aws-cli/2.9.8 Python/3.9.11 XXXX
```
---
#### 安装Session Manager 插件

此外，您还需要使用 AWS Command Line Interface (AWS CLI) 启动和结束连接到托管式节点的会话，必须先在本地计算机上安装 Session Manager 插件。更多请参考：https://docs.aws.amazon.com/zh_cn/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html。

- **Windows**：下载并运行[Windows 安装程序](https://s3.amazonaws.com/session-manager-downloads/plugin/latest/windows/SessionManagerPluginSetup.exe)。
- **MacOS**：您可以在终端（Terminal）中使用以下命令在 macOS 上安装 Session Manager 插件。

下载已签名的安装程序：

```shell
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/mac/session-manager-plugin.pkg" -o "session-manager-plugin.pkg"
```

运行安装命令。

```shell
sudo installer -pkg session-manager-plugin.pkg -target /
sudo ln -s /usr/local/sessionmanagerplugin/bin/session-manager-plugin /usr/local/bin/session-manager-plugin
```

**验证 Session Manager 插件安装**

运行以下命令验证是否已成功安装 Session Manager 插件。

```shell
session-manager-plugin
```

如果安装成功，将返回以下消息。

```shell
The Session Manager plugin is installed successfully. Use the AWS CLI to start a session.
```
