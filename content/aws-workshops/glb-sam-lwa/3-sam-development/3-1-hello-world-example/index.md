---
title: "3.1 创建 hello world 示例并打包部署"
weight: 1
type: workshops
---
在本节我们将创建项目 yaml 文件并体验 SAM 的工作方式

#### 1. 创建应用程序项目目录

在 Cloud9 的 terminal 执行以下命令生成项目的文件目录，并安装 tree 工具后续用于查看路径：

```shell
mkdir sam-app && cd sam-app
mkdir src
touch src/app.py
touch template.yaml
sudo yum install tree -y
```

目录结构如下：

```shell
Admin:~/environment $ tree
.
├── README.md
├── resize.sh
└── sam-app
    ├── src
    │   └── app.py
    └── template.yaml

2 directories, 4 files
```

* `tempalte.yaml`: SAM 使用 yaml 模板来描述应用程序所需的AWS资源 (集成 Lambda 函数, API Gateway, DynamoDB等)
* `src`目录： 存放Lambda的代码

打开`app.py`，将以下代码复制过去：

```shell
import json

print("Loading function")


def lambda_handler(event, context):
    return "Hello world"
```

`template.yaml` 内容：

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: 'AWS::Serverless-2016-10-31'
Description: A starter AWS Lambda function.
Resources:
  helloworldpython3:
    Type: 'AWS::Serverless::Function'
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.9
      CodeUri: src/
      Description: A starter AWS Lambda function.
      MemorySize: 128
      Timeout: 3
```

关于 yaml 模块语法的具体介绍，请参考 https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-template-anatomy.html

这里仅介绍其中一部分：

* **Type: 'AWS::Serverless::Function'：** 表示创建 Lambda 函数类型的资源。通过SAM可以定义非常多种的资源类型，如 `AWS::Serverless::Function` 对应 Lambda, `AWS::Serverless::Api`对应 API Gateway, `AWS::Serverless::SimpleTable`对应DynamoDB，其他支持的资源类型可以参考[官方文档](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-resources-and-properties.html)
* **Handler: app.lambda_handler:** 表示 Lambda 的 handler 函数，格式为`文件名 + 入口函数名`。这里我们的文件名为`app.py`，入口函数为`def lambda_hander()`。
* **Runtime:** 表示 Lambda 的执行语言环境，由于目前 Cloud 9 自带的 python 版本为3.9，我们必须和本机的版本保持一致，否则部署时会报错
* **CodeUri:** 代码目录。我们的 python 代码放在`src/`目录下
* **MemorySize, Timeout:** Lambda 的内存及超时时间配置

#### 2. 项目打包及部署
Package 过程涉及到将 template.yaml 及代码一起打包，生成 CloudFormation 模板，以进行后面的测试或者部署过程

Deploying 过程涉及到将上一步生成的 CloudFormation 资源部署到 AWS 环境：

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-1/1-package-and-deploy.png)

#### 3. 执行构建
在`sam-app`目录下执行：

```shell
cd ~/environment/sam-app/
sam build
```

构建完成后，在当前目录生成了 .aws-sam 目录，用于后续的测试或部署环节。
可以运行`tree -a`查看路径 

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-1/2-tree-file.png)

#### 4. 执行测试
在执行完 `sam build` 命令后，控制台会输出`[*] Invoke Function: sam local invoke`，表示我们可以使用该命令来执行测试：

```shell
sam local invoke
```

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-1/3-sam-local-invoke.png)

#### 4. 执行部署
执行以下命令将生成的 CloudFormation 部署到 AWS 环境

```shell
sam deploy --guided
```

所有参数保持默认即可（使用回车键）：

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-1/4-sam-deploy.png)

#### 4. 部署完成

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-1/5-sam-deploy-result.png)

进入 AWS 控制台，切换到 Lambda 页面，发现 SAM 已经为我们自动部署了资源：

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-1/6-lambda-console.png)

Lambda 的内容和代码中是一致的

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-1/7-lambda-function-code.png)

_______________

参考： 
* https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-building.html

* https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-deploying.html
