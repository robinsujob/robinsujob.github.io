---
title: "3.2 通过SAM命令生成项目"
weight: 2
type: workshops
---
#### 1. 执行 sam init 命令

回到初始路径，并执行 `sam init`，选择 `AWS Quick Start Templates` 和 `Hello World Example`

```shell
cd ~/environment/
sam init
```

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-2/1-sam-init.png)

这里不使用默认的Python，而是使用nodejs, 选择Zip方式部署：

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-2/2-choose-zip.png)

为避免与上一节项目名称冲突，这里命名为`sam-app2`。

进行创建：

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-2/3-create-sam-app2.png)

创建完成后，目录结构如下：

```shell
Admin:~/environment/sam-app2 $ tree
.
├── README.md
├── events
│   └── event.json
├── hello-world
│   ├── app.js
│   ├── package.json
│   └── tests
│       └── unit
│           └── test-handler.js
├── samconfig.toml
└── template.yaml

4 directories, 7 files
```

## 项目说明
`hello-world/app.js`声明了Lambda代码，它返回一个固定的json体：

```shell
exports.lambdaHandler = async (event, context) => {
    try {
        // const ret = await axios(url);
        response = {
            'statusCode': 200,
            'body': JSON.stringify({
                message: 'hello world',
                // location: ret.data.trim()
            })
        }
    } catch (err) {
        console.log(err);
        return err;
    }

    return response
};
```

`template.yaml`文件结构和上一节基本类似，注意到其中有额外的Events模块

```yaml
Events:
  HelloWorld:
    Type: Api # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
    Properties:
      Path: /hello
      Method: get
```

如果有Lambda的使用经历，可能会注意到Lambda有`Trigger`配置

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-2/4-lambda-trigger.png)

此`Events`字段描述了触发Lambda的资源(Api对应AWS API Gateway)。因此本项目不仅会部署Lambda函数，而且会一同部署API Gateway。架构如下

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-2/5-trigger-architecture.png)

更多可以触发函数的事件源可以参考：https://docs.aws.amazon.com/zh_cn/serverless-application-model/latest/developerguide/sam-property-function-eventsource.html
