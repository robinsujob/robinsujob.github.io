---
title: "3.总结"
weight: 5
type: workshops
---
在前面的内容中，您通过开启一个Amazon SageMaker Notebook，导入 Jupyter Notebook 代码运行并测试了AIGC模型。
随后将模型部署至 Amazon SageMaker Inference Endpoint，并通过在 Coud9 创建 Web 应用调用Amazon SageMaker Inference Endpoint。后续您可以进一步调优模型并进行测试，包括添加对中文语言对支持。

有关SageMaker的产品介绍以及有关文档可参考：

- 产品介绍：https://aws.amazon.com/cn/sagemaker/
- 产品文档：https://docs.aws.amazon.com/zh_cn/sagemaker/index.html

您可以通过以下信息查看更多关于 Stable Diffusion 的内容：

Stable Diffusion 最新版本：https://huggingface.co/spaces/stabilityai/stable-diffusion

更多关于Stable Diffusion的内容请参考官方文档，如有与本文档不一致，请以官方文档内容为准。 

- https://huggingface.co/blog/stable_diffusion 

- https://stability.ai/blog/stable-diffusion-public-release 

  

-----

如需清除本次实验开启的资源，请在控制台逐一删除 Cloud9 环境、S3 存储桶，以及 SageMaker里创建的 Notebook，Endpoint 以及 Model 等资源： 

[1] [删除Cloud9](https://docs.aws.amazon.com/zh_cn/cloud9/latest/user-guide/delete-environment.html)

[2] [删除SageMaker有关资源](https://docs.aws.amazon.com/zh_cn/sagemaker/latest/dg/ex1-cleanup.html)

[3] [清空S3桶中的模型文件](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/empty-bucket.html)

[4] [删除S3桶](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/delete-bucket.html)

---

*Contact: Robin Su(usuzhe@amazon.com), Luna Lu (luhaoy@amazon.com)*

*Last Update: 2023/05/18*
