---
title: "3.4 本地运行API Gateway测试"
weight: 4
type: workshops
---
上一节中，我们部署了API Gateway并使用它的URL进行验证测试。接下来我们会带大家在本地启动API服务进行测试。

#### 1. 本地运行 API Gateway
使用 sam local start-api 命令，可以在本地启动一台 API Gateway 实例以进行 HTTP request/response 测试。
在项目目录下运行：

```shell
sam local start-api
```

运行后，sam会查找template.yaml 中 Event字段的Api/HttpApi 字义，并将其映射到HTTP路径下。默认跑在本地3000端口：

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-4/1-sam-local-start.png)

启动新的命令行终端，访问该地址，得到预期的返回结果：

```shell
curl -w '\n' http://127.0.0.1:3000/hello
```

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-4/2-result.png)

在 `start-api`的控制台上，能够实时查看到对应的日志：

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-4/3-logs.png)

#### 2. 代码更新测试
`hello-world/app.js` 文件中定义了接口返回的内容: `message: 'hello world'`, 将其更新：

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-4/4-update-code.png)

此时如果想测试更新的效果，需要重新build，再启动api-server:

```shell
sam build
sam local start-api
```

此时访问本地接口，得到更新后的测试结果：

```shell
curl -w '\n' http://127.0.0.1:3000/hello
```
![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-4/5-updated-result.png)

参考：

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-start-api.html

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-start-api.html
