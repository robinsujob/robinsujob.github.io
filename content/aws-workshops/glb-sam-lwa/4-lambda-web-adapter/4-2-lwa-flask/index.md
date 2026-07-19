---
title: "4.2 使用Lambda Web Adapter压缩包（ZIP）方式部署Flask应用"
weight: 2
type: workshops
---
#### 1. 在AWS Cloud9中创建项目文件

在命令行中输入以下命令，创建用于压缩包部署Lambda Web Adapter的Flask应用。

```shell
cd /home/ec2-user/environment
wget /aws-workshops/glb-sam-lwa/assets/code/flask.zip
unzip flask.zip -d flask-lwa
```

#### 2. 在本地测试和运行Flask项目

请执行以下命令，安装依赖并在本地测试Flask项目。

```shell
cd /home/ec2-user/environment/flask-lwa/app
pip3 install -r requirements.txt
python3 -m gunicorn -b=:$PORT -w=1 app:app
```

打开另外一个终端（Terminal），使用`curl`指令进行测试。

```
curl 127.0.0.1:8080
```

#### 3. 使用SAM构建并测试Lambda Web Adapter

您可以在`flask-lwa`查看已经预置好的SAM模版文件。

```yaml
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
      Events:
        ApiEvent:
          Type: HttpApi
 
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

请使用`sam build`命令、`sam start local start-api`命令进行SAM的本地的测试。

```shell
cd /home/ec2-user/environment/flask-lwa
sam build --use-container
sam local start-api --region us-west-2
```

您可以通过打开新的终端，并使用`curl`命令测试对应结果。

```shell
curl 127.0.0.1:3000
```

测试结果应当为：

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-2/0-test-result.png)

#### 4. 使用SAM构建并测试Lambda Web Adapter

测试完毕后您可以使用以下指令部署。

```shell
sam deploy --guided
```

请输入项目名称，并保持默认区域，所有的选项都选择`y`。

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-2/1-sam-deploy-guide.png)

生成changset后，继续进行部署：

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-2/2-change-set.png)

部署完成后，会输出API Gateway的URL：

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-2/3-output.png)

您可以通过打开该链接，在浏览器中访问通过Lambda Web Adapter改造后的Flask项目。

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-2/4-results.png)
