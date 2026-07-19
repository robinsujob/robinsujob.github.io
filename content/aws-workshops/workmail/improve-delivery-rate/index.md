---
title: "提升邮件送达率"
weight: 5
type: workshops
---

在上一节中，您使用了自己的域名作为了WorkMail的域。在本节中我们将遵循最佳实践提升邮件的送达率。

多数电子邮件服务器都设置了相关规则，要求电子邮件发送自经过验证的发件人。[Easy DKIM](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/easy-dkim.html) 和 [SPF 记录](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/spf.html)有助于您建立良好声誉，增进电子邮件接收方对您的信任。

有时，如果 MAIL FROM 地址与电子邮件发送者的地址不一致，电子邮件服务器就会阻止邮件。[将自定义 MAIL FROM 域和 Amazon SES 结合使用](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/mail-from.html)后，您可以验证 MAIL FROM 标头中使用的经过验证的域的子域，这符合某些电子邮件服务器允许发送到该服务器上的地址的要求。

有关更详尽的关于最佳实践的参考，请点击以下链接了解：

https://aws.amazon.com/cn/premiumsupport/knowledge-center/ses-best-practices/

如果您使用Route53托管域名，在执行”**Update All in Route 53**”时，DKIM与SPF已经为您自动更新。在此步，您仅需在托管区域中手动添加MAIL FROM域。



1. 完成域名验证后，在页面底部”**Improved email delivery**“部分下拉**Details**，点击链接**Amazon SES**，进入到SES控制台

   ![image-20220911182348140](/aws-workshops/workmail/images/2-domain-9.png)

2. 在页面底部**Custom MAIL from domain**部分，点击**Edit**

   ![image-20220911183934187](/aws-workshops/workmail/images/2-domain-10.png)

3. 勾选**Use a Custom MAIL FROM domain**，并在**MAIL FROM domain**栏位中填写”**mailfrom**”，并点击**Save Change**

   ![image-20220912132746437](/aws-workshops/workmail/images/2-domain-11.png)

4. 此时会弹出MAIL FROM对应的MX与TXT记录，如果您使用时Route53托管的域名，您可以点击"Publish DNS records to Route53“自动更新记录，或将记录手动添加到您的DNS托管服务商

   ![image-20220911184435535](/aws-workshops/workmail/images/2-domain-12.png)

5. 添加完成稍等片刻，SES控制面板的Custom MAIL FROM domain部分会成为Success

   ![image-20220912132626038](/aws-workshops/workmail/images/2-domain-13.png)

6. 在Amazon WorkMail的Domain部分，”**Improved email delivery**“也会通过

   ![image-20220912133425605](/aws-workshops/workmail/images/2-domain-14.png)

至此，您完成了所有关于域验证和提升邮件送达率的部分。
