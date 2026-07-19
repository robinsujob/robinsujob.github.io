---
title: "前提条件"
weight: 2
type: workshops
---

在本次动手训练营中，您将构建一款属于您自己的企业级邮箱，并使用以您的域名为后缀的电子邮件地址收发邮件。**<u>因此，请准备好一个可以进行DNS解析的域名。</u>**

如果您没有自己的域名，可以参考以下步骤在亚马逊云科技中购买自己心仪的域名，并使用[Amazon Route53](https://aws.amazon.com/cn/route53/)托管您的域名。

## 在亚马逊云科技中注册域名【可选】

1. 单击[此处](https://console.aws.amazon.com/route53/home?region=us-east-1)在新窗口中打开 Route 53 控制台（Route 53 是 亚马逊云科技的 DNS 服务）。您可以使用 Route 53 注册新的域名以及管理域的 DNS 记录。
   选择*域注册*下的**注册域**。

   ![img](/aws-workshops/workmail/images/buydomain-1.png)

2. 单击**注册域**按钮。在下一个屏幕上，在*选择域*框中**输入您需要的域**（图片中显示的是 cloudexamples），然后**选择一个顶级域** (TLD)（例如，.com、.org、.co.uk 等） 单击**检查**按钮以查看该域是否可用。如果该域可用，单击**添加到购物车**按钮，然后滚动至页面底部，单击**继续**。

   **<u>注意：域不属于免费套餐，因此您将需要为注册的任何域付费。</u>**

   ![image-20220910151221570](/aws-workshops/workmail/images/buydomain-2.png)

3. **输入您的联系人详细信息**。这些信息将与您的域名相关联。输入信息后，单击页面底部的**继续**。

   ![image-20220910152139039](/aws-workshops/workmail/images/buydomain-3.png)
   
4. 查看列出的详细信息，如果信息正确，**选中**为*我已阅读并同意* *AWS 域名注册协议*的框。然后单击**完成订单**按钮。

   ![image-20220910152201566](/aws-workshops/workmail/images/buydomain-4.png)

5. 例如，如果您注册了一个拥有[通用顶级域](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/registrar-tld-list.html#registrar-tld-list-generic)的域（例如 .com），那么您将收到要求您确认电子邮件地址的电子邮件。（如果我们已确认电子邮件地址有效，将不会发送电子邮件。） 

   您必须**按照本电子邮件中的链接操作以确认电子邮件地址**，否则将无法注册域。

   对于所有域，您都将在域注册获得批准后收到电子邮件。

   注意：系统将需要几分钟时间来确认您已经成功注册新域。

   ![img](/aws-workshops/workmail/images/buydomain-5.png)

   ![img](/aws-workshops/workmail/images/buydomain-6.png)

## 迁移域名【可选】

如果您已有域名，您可以将您的域名迁移至Amazon Route53进行托管，请参考以下链接进行：

https://aws.amazon.com/cn/getting-started/hands-on/migrate-domain-to-aws-route53/

<div class="workshop-callout workshop-callout--info"><strong>注意</strong><p>域名迁移所花费的时间取决于NS记录更新的时间，托管域名不会立即生效，一般情况从几分钟到数小时不等，这取决于原域名解析商。部分域名解析商，例如GoDaddy最多可能需要48小时才可以生效。待生效以后，针对该域名的解析请求都会由Route53的域名服务器进行响应。</p></div>
