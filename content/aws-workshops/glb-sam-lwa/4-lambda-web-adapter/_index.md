---
title: "4. 使用Lambda Web Adapter迁移Web应用"
weight: 5
type: workshops
---
在本章节您将使用Lambda Web Adapter了解以下内容：
1. 创建一个Spring Boot样例程序，并使用Lambda Web Adapter容器化的方式部署
2. 创建一个Flask样例程序，并使用Lambda Web Adapter压缩包（ZIP）的方式部署
3. 通过SAM sync命令进行云上开发
4. 创建一个Lambda层（Layer）用于Flask应用，并了解层在Lambda开发中的用途

---

AWS Lambda Web Adapter 允许开发人员使用熟悉的框架（例如 Express.js、Next.js、Flask、SpringBoot、ASP.NET 和 Laravel，任何支持 HTTP 1.1/1.0 的框架）构建 Web 应用程序 (http api) 并在 AWS Lambda 上运行。 相同的 docker 映像可以在 AWS Lambda、Amazon EC2、AWS Fargate 和本地计算机上运行。 

![](/aws-workshops/glb-sam-lwa/assets/5-lambda-web-adapter/lambda-adapter-overview.png)

### 使用方式

AWS Lambda Web Adaptor 可与打包为 docker 映像和 Zip 包的 Lambda 函数配合使用。 

#### 打包为 Docker 镜像或 OCI 镜像的Lambda 函数

要将 Lambda Web Adaptor 与 docker 映像结合使用，您可以将您的 Web 应用程序 (http api) 打包到 Dockerfile 中，然后添加一行以将 Lambda Web Adaptor 二进制文件复制到容器内的 /opt/extensions： 

```Shell
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.3 /lambda-adapter /opt/extensions/lambda-adapter
```

默认情况下，Lambda Web Adapter假定Web应用程序正在监听端口8080。如果不是，您可以通过配置指定端口。

预编译的Lambda Web Adapter二进制文件已经作为容器打包，可在ECR公共存储库中找到:`public.ecr.aws/awsguru/aws-lambda-adapter`。该存储库还提供了支持x86_64和arm64 CPU架构的多架构镜像。

#### 打包为Zip压缩包的AWS托管运行时的Lambda函数

AWS Lambda Web Adapter 也适用于 AWS 托管的 Lambda 运行时，您需要完成以下三个步骤：

1. 将Lambda Web Adapter层附加到您的函数。

**AWS全球区域（不包含US Gov区域）**


- x86_64: `arn:aws:lambda:${AWS::Region}:753240598075:layer:LambdaAdapterLayerX86:22`
- arm64: `arn:aws:lambda:${AWS::Region}:753240598075:layer:LambdaAdapterLayerArm64:22`

**AWS中国区域**


- cn-north-1 (北京)
   - x86_64: `arn:aws-cn:lambda:cn-north-1:041581134020:layer:LambdaAdapterLayerX86:22`
- cn-northwest-1 (宁夏)
   - x86_64: `arn:aws-cn:lambda:cn-northwest-1:069767869989:layer:LambdaAdapterLayerX86:22`

2. 将 Lambda 环境变量  `AWS_LAMBDA_EXEC_WRAPPER` 配置为 `/opt/bootstrap`。

3. 将Lambda的Handler文件设置为您的 Web 应用程序启动脚本，例如 `run.sh`。

有关Lambda Web Adapter的更多信息，您可以参考：https://github.com/awslabs/aws-lambda-web-adapter
