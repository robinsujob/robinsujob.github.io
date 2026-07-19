---
title: "4.3 层（Lambda Layer）在Lambda开发中的应用"
weight: 3
type: workshops
---
在上一节，您通过Zip压缩包的方式部署了Lambda Web Adapter。本章节的内容将帮助您理解Layer在Lambda开发中的的作用，同时您将开发一个新的Layer并更新到先前创建的Flask应用中。另外，在本章节中您还将了解到如何通过`sam sync`来进行远程调试。

[Lambda 层](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/chapter-layers.html)是包含补充代码或数据的 .zip 文件存档。层通常包含库依赖项、[自定义运行时系统](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/runtimes-custom.html)或配置文件。如果您需要在Lambda函数中使用一个层，您可以使用SAM在模版文件中引入层，例如：

```yaml
---
Resources:
  FlaskFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: app/
      Handler: run.sh
      Runtime: python3.12
      MemorySize: 256
      Environment:
        Variables:
          AWS_LAMBDA_EXEC_WRAPPER: /opt/bootstrap
          AWS_LWA_PORT: 8000
      Layers:
        - !Sub arn:aws:lambda:${AWS::Region}:753240598075:layer:LambdaAdapterLayerX86:22  
---
```

一般来说创建层通常涉及三个步骤：

1. 打包层内容。此步骤需要创建 .zip 文件存档，其中包含要在函数中使用的依赖项。
2. 在 Lambda 中创建层。
3. 将层添加到函数。

但是通过sam命令与template模版可以简化创建并使用层的步骤。您将跟随以下步骤，创建一个Layer层用于获取系统时间，更新到先前创建的Flask应用中，并通过sam命令进行部署。

#### 1. 使用sam sync远程调试

`sam sync` 命令将本地应用程序的更改同步到 AWS Cloud。您可以通过运行以下命令在AWS Cloud上部署一个测试用的堆栈，在调试过程中请保持`sam sync`保持在运行状态。

```shell
cd ~/environment/flask-lwa/
sam sync --stack-name flask-lwa-layer --use-container --watch
```

![](/workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-3/1-aws-sync.png)

运行完成后，您可以点击API Gateway地址进行访问测试。

![](/workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-3/2-output-api-gw.png)

预期输出结果为：

```json
{"message":"hello world","status":200}
```

随后您将跟随教程修改代码，将输出结果添加系统时间。

#### 2. 创建Lambda Layer代码

请新建一个命令行终端后，创建存储Lambda层代码的文件夹，并进入。

```sh
cd ~/environment/flask-lwa
mkdir layers
mkdir layers/python
mkdir layers/python/time_utils
cd layers/python/time_utils
```


{{% workshop-alert type="info" %}}
**请注意关于 Lambda 运行时的层路径。当您向函数添加层时，Lambda 会将层内容加载到该执行环境的 `/opt` 目录中。对于每个 Lambda 运行时系统，`PATH` 变量都包括 `/opt` 目录中的特定文件夹路径。为确保 `PATH` 变量能够获取层内容，请根据您运行Lambda Layer的语言环境，遵循对应规则。具体可参考文档[每个 Lambda 运行时的层路径](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/packaging-layers.html#packaging-layers-paths)。**
{{% /workshop-alert %}}


在本节中动手训练营采用Flask框架，因此您需要遵循文档创建带有Python字样的代码路径。随后您可以创建获取系统时间的Python代码文件至对应的文件夹中。


{{% workshop-expand title="获取系统时间代码样例" open="false" %}}


```python
# File Name: get_date_layer.py
import json
from datetime import datetime, timezone, timedelta

def get_current_time():
    bj_time = timezone(timedelta(hours=8))
    now = datetime.now(bj_time)
    date_text = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_text
```


{{% /workshop-expand %}}


#### 3. 修改app.py文件

您需要修改app.py文件，在Get/Post请求引用获取系统时间Lambda层的代码，并修改请求的响应。


{{% workshop-expand title="修改后的app.py样例" open="false" %}}


```python
from flask import (Flask, jsonify)
from time_utils.get_date_layer import get_current_time
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    print(os.system("ls /opt"))
    print(os.system("ls /opt/python"))
    current_time = get_current_time()
    return jsonify(status=200, message=f"hello world,{current_time}")
```


{{% /workshop-expand %}}


#### 4.修改sam模版文件（template.yaml）

您还需要修改template.yaml文件，将获取系统时间Lambda层的代码添加到模版文件中。您可以使用 AWS Serverless Application Model（AWS SAM）自动在应用程序中创建层。`AWS::Serverless::LayerVersion` 资源类型创建一个层版本，您可以从自己的 Lambda 函数配置中引用该版本。有关样例可参考[层与 AWS SAM](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/layers-sam.html)。


{{% workshop-expand title="修改后的template.yaml样例" open="false" %}}


```python
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  Sample SAM Template for flask in Zip

# More info about Globals: https://github.com/awslabs/serverless-application-model/blob/master/docs/globals.rst
Globals:
  Function:
    Timeout: 29

Resources:
  FlaskFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: app/
      Handler: run.sh
      Runtime: python3.12
      MemorySize: 256
      Environment:
        Variables:
          AWS_LAMBDA_EXEC_WRAPPER: /opt/bootstrap
          AWS_LWA_PORT: 8000
      Layers:
        - !Sub arn:aws:lambda:${AWS::Region}:753240598075:layer:LambdaAdapterLayerX86:22
        - !Ref TimeUtils
      Events:
        ApiEvent:
          Type: HttpApi
          
  TimeUtils:
    Type: AWS::Serverless::LayerVersion
    Properties:
      ContentUri: ./layers
      CompatibleRuntimes:
        - python3.9
        - python3.10
        - python3.12
 
Outputs:
  FlaskApi:
    Description: "API Gateway endpoint URL for Prod stage for Flask function"
    Value: !Sub "https://${ServerlessHttpApi}.execute-api.${AWS::Region}.${AWS::URLSuffix}/"
  FlaskFunction:
    Description: "Flask Lambda Function ARN"
    Value: !GetAtt FlaskFunction.Arn
  FlaskIamRole:
    Description: "Implicit IAM Role created for Flask function"
    Value: !GetAtt FlaskFunctionRole.Arn
```


{{% /workshop-expand %}}


代码编辑保存后，等待`sam sync`更新完成。再次访问API Gateway结果，您可以查看到更新后的结果。

![](/workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-3/3-api-gw-results.png)
