---
title: "3.5 通用自然语言理解"
weight: 5
type: workshops
---
支持各种中文文本理解任务，如文本分类、情感分析、提取和可定制的标签系统。用于文本分类、情感分析、文本匹配和实体识别等场景。

#### 3.5.1 API 请求参数说明

该API在不同的任务下有不同的输入参数。


##### 文本分类

* HTTP 方法： POST

* 请求参数

|名称|类型|是否必选|说明|
|:-----:|-----:|:-----:|:-----:|
|subtask_type|String|是|固定为“文本分类”|
|text|String|是|待分类的文本|
|choices|List|是|候选标签，参考**请求示例**|
|question|String|是|用于指导模型的提示文本|

* 请求示例

```
{
    "subtask_type": "文本分类",
    "text": "待分类的文本",
    "choices": [{
        "entity_type": "投资",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "科技",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "体育",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "美食",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "旅游",
        "label": 0,
        "entity_list": []
    }],
    "question": "这是篇什么类型的新闻"
}
```


##### 情感分类

* HTTP 方法： POST

* 请求参数

|名称|类型|是否必选|说明|
|:-----:|-----:|:-----:|:-----:|
|subtask_type|String|是|固定为“情感分类”|
|text|String|是|待分类的文本|
|choices|List|是|候选情感标签，参考**请求示例**|
|question|String|是|用于指导模型的提示文本|

* 请求示例

```
{
    "subtask_type": "情感分类",
    "text": "待分类的用户评论",
    "choices": [{
        "entity_type": "积极",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "中性",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "消极",
        "label": 0,
        "entity_list": []
    }],
    "question": "这句话的情感极性是什么"
}
```


##### 文本匹配

* HTTP 方法： POST

* 请求参数

|名称|类型|是否必选|说明|
|:-----:|-----:|:-----:|:-----:|
|subtask_type|String|是|固定为“文本匹配”|
|text|String|是|第一个文本|
|choices|List|是|每个元素的entity_type是提示词与第二个文本的拼接，例如“可以推断出：第二个文本”或“可以理解为：第二个文本”，参考**请求示例**|
|question|String|是|用于指导模型的提示文本|

* 请求示例

```
{
    "subtask_type": "文本匹配",
    "text": "在白云的蓝天下，一个孩子伸手摸着停在草地上的一架飞机的螺旋桨。",
    "choices": [{
        "entity_type": "可以推断出：一个孩子正伸手摸飞机的螺旋桨。",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "不能推断出：一个孩子正伸手摸飞机的螺旋桨。",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "很难推断出：一个孩子正伸手摸飞机的螺旋桨。",
        "label": 0,
        "entity_list": []
    }],
    "question": "同义文本"
}

```


##### 实体识别

* HTTP 方法： POST

* 请求参数

|名称|类型|是否必选|说明|
|:-----:|-----:|:-----:|:-----:|
|subtask_type|String|是|固定为“实体识别”|
|text|String|是|待分类的文本|
|choices|List|是|每个元素的entity_type是想要提取的实体类型，参考**请求示例**|

* 请求示例

```
{
    "subtask_type": "实体识别",
    "text": "我们是首家支持英特尔、AMD 和 Arm 处理器的主要云提供商",
    "choices": [{
        "entity_type": "地址",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "公司名",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "人物姓名",
        "label": 0,
        "entity_list": []
    }]
}
```

#### 3.5.2 开始使用


1)	点击API右侧的向下箭头，展开通用人像分割的请求方法。
2)	点击右侧的测试（Try it out）按钮
3)	测试**文本分类**：在Request body中输入以下的请求数据进行测试，并查看测试结果。

```json
{
    "subtask_type": "文本分类",
    "text": "无论您是在寻找计算能力、数据库、存储、内容分发、人工智能与机器学习，大数据分析还是其他功能，亚马逊云科技都有相应的服务来帮助您建立具有更高灵活性、可扩展性和可靠性的复杂应用。",
    "choices": [{
        "entity_type": "农业工程",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "哲学",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "教育学",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "计算机",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "理学",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "农学",
        "label": 0,
        "entity_list": []
    }],
    "question": "这篇文章属于哪个学科"
}
```

4)	确认格式正确后，点击下方的 **Execute**。
5)	在 **Responses body** 中查看返回的JSON结果。您还可以通过右侧复制或下载按钮保存处理结果。在 **Response headers** 中查看响应头的相关信息。

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.5/3.5-Picture1.png)

6)	测试**情感分类**：在Request body中输入以下的请求数据进行测试，并查看测试结果。

```json
{
    "subtask_type": "情感分类",
    "text": "这不仅体现在行业覆盖的丰富度上――游戏、电商等互联网行业的出海热情持续高涨，而传统制造业如今也希望借助“出海”，实现由“中国制造”向“中国品牌”的转型。",
    "choices": [{
        "entity_type": "积极",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "中性",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "消极",
        "label": 0,
        "entity_list": []
    }],
    "question": "这句话的情感极性是什么"
}
```

7)	确认格式正确后，点击下方的 **Execute**。
8)	在 **Responses body** 中查看返回的JSON结果。您还可以通过右侧复制或下载按钮保存处理结果。在 **Response headers** 中查看响应头的相关信息。

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.5/3.5-Picture2.png)

9)	测试**文本匹配**：在Request body中输入以下的请求数据进行测试，并查看测试结果。

```json
{
    "subtask_type": "文本匹配",
    "text": "在白云的蓝天下，一个孩子伸手摸着停在草地上的一架飞机的螺旋桨。",
    "choices": [{
        "entity_type": "可以推断出：一个孩子正伸手摸飞机的螺旋桨。",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "不能推断出：一个孩子正伸手摸飞机的螺旋桨。",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "很难推断出：一个孩子正伸手摸飞机的螺旋桨。",
        "label": 0,
        "entity_list": []
    }],
    "question": "同义文本"
}

```

10)	确认格式正确后，点击下方的 **Execute**。
11)	在 **Responses body** 中查看返回的JSON结果。您还可以通过右侧复制或下载按钮保存处理结果。在 **Response headers** 中查看响应头的相关信息。

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.5/3.5-Picture3.png)

12)	测试**实体识别**：在Request body中输入以下的请求数据进行测试，并查看测试结果。

```json
{
    "subtask_type": "实体识别",
    "text": "我们是首家支持英特尔、AMD 和 Arm 处理器的主要云提供商",
    "choices": [{
        "entity_type": "地址",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "公司名",
        "label": 0,
        "entity_list": []
    }, {
        "entity_type": "人物姓名",
        "label": 0,
        "entity_list": []
    }]
}
```

13)	确认格式正确后，点击下方的 **Execute**。
14)	在 **Responses body** 中查看返回的JSON结果。您还可以通过右侧复制或下载按钮保存处理结果。在 **Response headers** 中查看响应头的相关信息。

![image.png](/aws-workshops/glb-ai-solution-kit/assets/3-use-aikit/3.5/3.5-Picture4.png)
