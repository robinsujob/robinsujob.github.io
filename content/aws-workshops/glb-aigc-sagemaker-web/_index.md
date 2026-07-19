---
title: "端到端体验AIGC-从SageMaker到Web应用"
weight: 5
type: workshops
shortTitle: "AIGC：SageMaker 到 Web"
homeTitle: "端到端体验AIGC-从SageMaker到Web应用"
summary: "使用 SageMaker Notebook 运行 Stable Diffusion，并在 Cloud9 构建可调用模型的 Flask Web 应用。"
workshopRoot: true
---
##  AIGC 是什么？

AI Generated Content (AIGC，人工智能自动生成内容)，是继专业生产内容（PGC,  Professional-generated Content）、用户生产内容（UGC, User-generated  Content）之后的新型内容创作方式，可以在创意、表现力、迭代、传播、个性化等方面，充分发挥技术优势，打造新的数字内容生成与交互形态。随着科技的发展，AI写作、AI配乐、AI视频生成、 AI语音合成、以及近段时间火遍全网的AI绘画，都为创作领域带来一波热议, 只要简单输入几个关键词几秒钟之内一幅画作就能诞生。



## 如何通过SageMaker实现AIGC？

[Amazon SageMaker](https://aws.amazon.com/cn/sagemaker/) 是一项完全托管的机器学习服务。借助 SageMaker的多种功能，数据科学家和开发人员可以快速轻松地构建和训练机器学习模型，然后直接部署至生产环境就绪的托管环境。SageMaker涵盖了 ML 的整个工作流，可以标记和准备数据、选择算法、训练模型、调整和优化模型以便部署、预测和执行操作。

在本次动手训练营中，您将了解到如何使用[Amazon SageMaker Notebook](https://docs.aws.amazon.com/sagemaker/latest/dg/nbi.html) 运行AIGC模型，并将 AIGC 模型部署至 [SageMaker Inference Endpoint](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html)（推理终端节点），并通过输入关键词直接调用这些模型并生成用户需要的图片。

另外，在本次动手训练营中，您还可以了解到如何在您的Web应用程序代码中调用 SageMaker Inference Endpoint。您将在[AWS Cloud9](https://aws.amazon.com/cn/cloud9/)中编写、调试和运行您的Web应用代码。它是一种基于云的集成开发环境 (IDE)，您只需要一个浏览器，即可编写、运行和调试代码。

---

*Contact: Robin Su(usuzhe@amazon.com), Luna Lu (luhaoy@amazon.com)*

*Last Update: 2023/05/30*
