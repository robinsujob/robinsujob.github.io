---
title: "3.3 测试及部署项目"
weight: 3
type: workshops
---
本节我们将在上节的基础上，使用SAM测试及部署项目。

#### 1. 执行 sam build 命令

执行 sam build 命令

```shell
sam build
```

#### 2. 测试

执行 `sam local invoke` 启动一个docker容器对项目进行测试

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-3/1-sam-local-invoke.png)

查看`docker images`，可以找到构建的镜像列表

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-3/2-docker-images.png)

#### 3. 部署

执行`sam deploy --guided` 

```shell
sam deploy --guided
```

输入项目名称，所有的选项都选择`y`。

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-3/3-sam-deploy.png)


{{% workshop-alert type="warning" title="在`HelloWorldFunction may not have authorization defined, Is this okay`部分，如果选择跳过会报`Error: Security Constraints Not Satisfied!` 错误参考：https://stackoverflow.com/questions/61841136/what-is-the-cause-of-the-security-constraints-not-satisfied-error-when-using-sam" %}}
[](/aws-workshops/glb-sam-lwa/3-sam-development/3-3-test-and-deploy/#7)
{{% /workshop-alert %}}


生成changset后，继续进行部署

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-3/4-deploy-changeset.png)

部署完成后，会输出API Gateway的URL

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-3/5-deploy-output.png)

在浏览器中访问，结果如Lambda中定义的json体

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-3/6-view-url.png)

部署完成后，进入Lambda服务。新创建的Lambda会自动绑定对应的API Gateway 触发器

![](/aws-workshops/glb-sam-lwa/assets/4-sam-development/4-3/7-lambda-api-trigger.png)
