---
title: "在WorkMail上使用自己的邮件域"
weight: 4
type: workshops
---

在上一节中，我们初始化了我们的Amazon WorkMail，并使用测试邮件域发送了一封测试邮件。本节我们将带领您通过**Amazon Route53**为您的Amazon WorkMail创建自己的邮件域。

使用测试域的帐户每天只能发送200 个收件人，并且因为测试邮件域不能长期使用，我们建议您添加自己的域验证，并使用它作为默认域。

本节的[前提条件](../prerequisites/)是您必须拥有自己的域名。

#### 添加自己的邮件域名并验证

1. 在组织（**Organization**）控制台中，点击左侧菜单栏的域(**Domain**)。

   ![image-20220911162415569](/workshops/workmail/images/2-domain-1.png)

1. 在导航窗格中选择添加域（**add domain**）

   ![image-20220911162642246](/workshops/workmail/images/2-domain-2.png)

3. 随后您可以填写您拥有的域名，或者选择已经由Route53托管的域。并输入二级域名的名称【可选，取决于您的设计】

   ![image-20220911164638898](/workshops/workmail/images/2-domain-3.png)

   ![image-20220911164713145](/workshops/workmail/images/2-domain-4.png)

4. 如果您的域托管在其他厂商则会出现下方图片中的蓝色提示”**Configure this domain manually**”【**需手动配置**】，如果您的域托管在Route 53则会出现下方图片中的绿色提示”**Domain added**”，此时点击右上方橙色按键”**Update All in Route 53**”即可一键**自动**设置。

   ![image-20220911165017391](/workshops/workmail/images/2-domain-5.png)

   ![image-20220912234332900](/workshops/workmail/images/2-domain-6.png)

5. 点击"**Update All in Route 53**"之后，我们可以看到提示，稍等片刻，您可以看到“Domain ownership”、“WorkMail configuration”、“Improved security “的部分都已通过，您可以在Route53中校验添加的域名验证记录。

   ![image-20220911165447879](/workshops/workmail/images/2-domain-7.png)

   ![image-20220911165823241](/workshops/workmail/images/2-doamin-8.png)

目前，您已经完成有关域名验证的大部分内容，随后我们将遵循最佳实践，提升送达率。
