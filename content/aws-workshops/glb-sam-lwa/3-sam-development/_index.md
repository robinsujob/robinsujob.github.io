---
title: "3. AWS SAM CLI 入门"
weight: 4
type: workshops
---
AWS Serverless Application Model (AWS SAM) 是一个开源框架，用于使用基础设施即代码 (IaC) 构建无服务器应用程序。通过使用 AWS SAM，开发人员可以声明AWS CloudFormation资源和专门的无服务器资源，这些资源在部署过程中会转换为基础设施。该框架包括两个主要组件： AWS SAM CLI和 AWS SAM 项目。

#### AWS SAM CLI
AWS SAM CLI 是一种在 SAM 应用程序项目目录上运行命令并最终将其转换为无服务器应用程序的工具。它允许您构建、转换、部署、调试、打包、初始化和同步 AWS SAM 应用程序项目目录。

常见的 AWS SAM CLI 如下，更多的 SAM CLI 指令可参考[文档](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)

|       AWS SAM CLI       |                                   命令                                    |
|:-----------------------:|:-----------------------------------------------------------------------:| 
|      **sam build**      |                  让应用程序为开发工作流程的后续步骤（如本地测试或部署到AWS云上）做好准备                  |
|     **sam delete**      | 删除 AWS CloudFormation 堆栈、打包并部署到 S3 和 ECR 的项目以及 SAM 模板文件来删除 AWS SAM 应用程序 |
|     **sam deploy**      |                                 部署应用程序                                  |
|      **sam init**       |                          提供用于初始化新的无服务器应用程序的选项                           |
|  **sam local invoke**   |                               在本地一次性调用函数                                |
| **sam local start-api** |                      通过本地 HTTP 服务器调用Lambda函数进行本地测试                      |
|      **sam sync**       |                           将本地应用程序的更改同步到AWS云上                            |
|    **sam validate**     |                           验证 AWS SAM 模板文件是否有效                           |

#### AWS SAM 项目
AWS SAM 项目是运行 sam init 时创建的应用程序项目目录。AWS SAM 项目包括诸如 AWS SAM template之类的文件,该模板包括模板规范(用于声明资源的简化语法)。

在本节中，您将通过创建和部署简单的 hello world 示例来了解 SAM 项目，以及如何通过SAM CLI测试和部署无服务器应用程序。
