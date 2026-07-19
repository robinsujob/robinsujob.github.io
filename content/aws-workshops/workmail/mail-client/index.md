---
title: "邮件客户端与WorkMail的集成"
weight: 7
type: workshops
---

Amazon WorkMail支持多种邮件收发方式，您可以使用 Amazon WorkMail Web 客户端登录。 您还可以设置其他电子邮件客户端以与您的 Amazon WorkMail 账户一起使用，例如 [Microsoft Outlook](https://docs.aws.amazon.com/zh_cn/workmail/latest/userguide/outlook-client.html)、[现有的 Android 或 iOS 客户端](https://docs.aws.amazon.com/zh_cn/workmail/latest/userguide/mobile-client.html)、[Windows 10邮件应用](https://docs.aws.amazon.com/zh_cn/workmail/latest/userguide/connect_win10_mail.html)、[macOS 客户端](https://docs.aws.amazon.com/zh_cn/workmail/latest/userguide/connect_mac_mail.html)或 [IMAP 客户端](https://docs.aws.amazon.com/zh_cn/workmail/latest/userguide/using_IMAP.html)。目前，WorkMail还尚未支持POP3客户端。

在本节中，我们将重点介绍[IMAP客户端](https://docs.aws.amazon.com/zh_cn/workmail/latest/userguide/using_IMAP.html)的设置方式。

#### 以Mac OS的邮件APP为例

1. 在启动台（LaunchPad）中搜索“**邮件**”点击，并添加账户

   ![image-20220912231255693](/aws-workshops/workmail/images/6-client-1.png)

2. 在邮件提供商处，选择“其他"邮件帐户

   ![image-20220912231435747](/aws-workshops/workmail/images/6-client-2.png)

3. 复制WorkMail中一个用户的邮件地址，并输入密码

   ![image-20220912233711594](/aws-workshops/workmail/images/6-client-3.png)

   ![image-20220912233748489](/aws-workshops/workmail/images/6-client-4.png)

4. 此时会有错误提示，请选择IMAP账户类型

   ![image-20220912232025855](/aws-workshops/workmail/images/6-client-5.png)

5. 根据WorkMail文档中有关IMAP客户端中提供IMAP和SMTP的信息，复制并粘贴【**注意WorkMail所属区域，请复制与WorkMail一致区域终端节点**】，并点击登录。文档如下：

   https://docs.aws.amazon.com/zh_cn/workmail/latest/userguide/using_IMAP.html

   ![image-20220912232110951](/aws-workshops/workmail/images/6-client-6.png)

   IMAP接收邮件地址: ```imap.mail.us-west-2.awsapps.com```

   SMTP发送邮件地址: ```smtp.mail.us-west-2.awsapps.com```

   ![image-20220912232349870](/aws-workshops/workmail/images/6-client-7.png)

6. 随后可看到邮件界面，配置成功

   ![image-20220912232514448](/aws-workshops/workmail/images/6-client-8.png)

   

#### 以Windows 版本的Outlook 2019为例

1. 在开始菜单处搜索Outlook并点击，并添加账户

   ![image-20220912232724319](/aws-workshops/workmail/images/6-client-9.png)

2. 首次使用将输入邮件地址，复制WorkMail中一个用户的邮件地址

   ![image-20220912231626952](/aws-workshops/workmail/images/6-client-3.png)

   ![image-20220912232850445](/aws-workshops/workmail/images/6-client-10.png)

3. 选择IMAP类型

   ![image-20220912233012544](/aws-workshops/workmail/images/6-client-11.png)

4. 根据WorkMail文档中有关IMAP客户端中提供IMAP和SMTP的信息，复制并粘贴【**注意WorkMail所属区域，请复制与WorkMail一致区域终端节点**】，选择SSL加密方法，并更改端口。并点击下一步。文档如下：

   https://docs.aws.amazon.com/zh_cn/workmail/latest/userguide/using_IMAP.html

   ![image-20220912232110951](/aws-workshops/workmail/images/6-client-6.png)

   IMAP接收邮件地址: ```imap.mail.us-west-2.awsapps.com```

   SMTP发送邮件地址: ```smtp.mail.us-west-2.awsapps.com```

   ![image-20220912233043083](/aws-workshops/workmail/images/6-client-12.png)

5. 随后可看到配置成功界面

   ![image-20220912233302287](/aws-workshops/workmail/images/6-client-13.png)
