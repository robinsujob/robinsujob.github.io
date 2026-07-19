---
title: "4.1 使用Lambda Web Adapter容器化方式部署SpringBoot应用"
weight: 1
type: workshops
---
#### 1. 在AWS Cloud9中创建项目文件

在命令行中输入以下命令，创建用于容器化部署Lambda Web Adapter的Spring Boot应用。

```shell
cd /home/ec2-user/environment
wget /aws-workshops/glb-sam-lwa/assets/code/springboot.zip
unzip springboot.zip -d springboot-lwa
```

#### 2. 打开Spring Boot的主入口文件

在左侧文件目录栏中，查找`Application.java`文件，目录结构如图所示，并双击打开。

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/1-application-file.png)

此时应当会提示激活**增强开发**功能，请点击绿色按钮激活，并刷新AWS Cloud9 IDE页面。

增强开发功能是AWS Cloud9 提供额外的开发支持，以改善使用 Java 时的开发体验。主要的生产力特性包括代码补全（code completion,）、错误筛选、代码洞察（code lenses），以及调试选项，如断点和步进。

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/2-active-java-enhancement.png)

#### 3. 在本地测试主入口文件

请在AWS Cloud9 的页面上方点击**绿色“Run”**按钮，测试主入口文件。Cloud9将自动帮您进行编译，稍等片刻，程序应当会自动运行。

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/3-run-java.png)

查看命令行的提示，如果Spring Boot应用运行成功，您可以**点击“Preview “按钮**，并点击”**Preview Running Application**“测试Spring Boot项目。

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/4-preview-java.png)

您应当可以在页面中看到“Hello, world!"字样，您也可以修改访问的子路径，例如“/pets”，进入到其他数据接口中。

| ![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/5-test-hello-world.png) | ![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/6-test-pets.png) |
| ------------------------------------------------------------ | ----------------------------------------------------- |

测试完毕您可以关闭下方的`java - auto`窗口以结束进程。

#### 4. 构建Docker镜像，并在本地测试

您可以在项目的`app`目录下找到`Dockerfile`文件，查看如何将Spring Boot项目将Lambda Web Adapter进行容器化集成。Dockerfile内容如下：

```shell
FROM public.ecr.aws/sam/build-java8.al2:latest as build-image
WORKDIR "/task"
COPY src src/
COPY pom.xml ./
RUN mvn -q clean package

FROM public.ecr.aws/docker/library/amazoncorretto:8u322-al2
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.3 /lambda-adapter /opt/extensions/lambda-adapter
ENV PORT=8000
WORKDIR /opt
COPY --from=build-image /task/target/petstore-0.0.1-SNAPSHOT.jar /opt
CMD ["java", "-jar", "petstore-0.0.1-SNAPSHOT.jar", "--server.port=${PORT}"]
```

您可进入Spring Boot项目的app目录中，在命令行输入以下命令，进行容器的构建。

```shell
cd /home/ec2-user/environment/springboot-lwa/app
docker build -t springboot:test .
```

随后您可以运行`docker run`命令，**这意味着您可以将该容器部署到EC2、Farget、EKS等无需修改任何代码**：

```shell
docker run -p 8000:8000 springboot:test
```

随后，您可以打开另外一个命令行窗口，并通过`curl`指令测试该容器可以正常运行。

```shell
curl 127.0.0.1:8000/pets
```

#### 5. 使用SAM进行测试并部署Lambda Web Adapter

您可以在`springboot-lwa`查看已经预置好的SAM模版文件。

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  sam-app

  Sample SAM Template for sam-app

Globals:
  Function:
    Timeout: 10

Resources:
  PetstoreFunction:
    Type: AWS::Serverless::Function
    Properties:
      PackageType: Image
      MemorySize: 2048
      Tracing: Active
      Environment:
        Variables:
          RUST_LOG: info
          READINESS_CHECK_PATH: /healthz
          REMOVE_BASE_PATH: /v1
      AutoPublishAlias: live
      DeploymentPreference:
        Type: AllAtOnce
      ProvisionedConcurrencyConfig:
        ProvisionedConcurrentExecutions: 1
      Events:
        Root:
          Type: HttpApi
          Properties:
            Path: /v1
            Method: ANY
        Petstore:
          Type: HttpApi
          Properties:
            Path: /v1/{proxy+}
            Method: ANY
    Metadata:
      DockerTag: java8.al2-maven-v1
      DockerContext: ./app
      Dockerfile: Dockerfile

  MyScalableTarget:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 100
      MinCapacity: 1
      ResourceId: !Sub function:${PetstoreFunction}:live # You need to specify an alis or version here
      RoleARN: !Sub arn:aws:iam::${AWS::AccountId}:role/aws-service-role/lambda.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_LambdaConcurrency
      ScalableDimension: lambda:function:ProvisionedConcurrency
      ServiceNamespace: lambda
    DependsOn: PetstoreFunctionAliaslive # This is your function logical ID + "Alias" + what you use for AutoPublishAlias

  MyTargetTrackingScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: utilization
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref MyScalableTarget
      TargetTrackingScalingPolicyConfiguration:
        TargetValue: 0.70 # Any value between 0 and 1 can be used here
        CustomizedMetricSpecification:
          Dimensions:
            - Name: FunctionName
              Value: !Ref PetstoreFunction
            - Name: Resource
              Value: !Sub "${PetstoreFunction}:live"
          MetricName: ProvisionedConcurrencyUtilization
          Namespace: AWS/Lambda
          Statistic: Maximum
          Unit: Count

Outputs:
  PetstoreApi:
    Description: "API Gateway endpoint URL for Prod stage for Petstore function"
    Value: !Sub "https://${ServerlessHttpApi}.execute-api.${AWS::Region}.${AWS::URLSuffix}/v1/pets"
```

首先请使用`sam build`命令、`sam local start-api`命令进行SAM的本地的测试。

```shell
cd /home/ec2-user/environment/springboot-lwa
sam build
sam local start-api --warm-containers EAGER
```

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/6-sam-local-api.png)

您可以通过打开新的终端，并使用`curl`命令测试对应结果。

```shell
curl 127.0.0.1:3000/v1/pets
```

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/7-invoke-local-sam.png)

测试完毕后，您可以使用`sam deploy --guide`将Sprint Boot项目部署到Lambda，并通过API Gateway进行触发。

请输入项目名称，并保持默认区域，所有的选项都选择`y`。

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/8-sam-deploy-guide.png)

并选择自动为您创建托管的ECR仓库。

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/9-set-ecr.png)

生成changset后，继续进行部署：

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/10-change-set.png)

部署完成后，会输出API Gateway的URL：

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/11-sam-output-api-gw.png)

您可以通过打开该链接，在浏览器中访问通过Lambda Web Adapter改造后的Spring Boot项目。

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/5-1/12-browser-api-gw.png)
