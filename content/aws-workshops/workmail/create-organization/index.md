---
title: "开始使用 Amazon WorkMail"
weight: 3
type: workshops
---

完成[前提条件](/aws-workshops/workmail/prerequisites/)后，您就可以通过完成以下步骤开始使用 Amazon WorkMail。

#### 步骤 1：登录 Amazon WorkMail 控制台

您必须先登录 Amazon WorkMail 控制台，然后才能添加用户并管理他们的账户和邮箱。

1. 首先我们可以使用以下链接，直接登陆到Amazon WorkMail控制台，本次将在俄勒冈区域（us-west-2）区域进行操作，以下链接将进入**俄勒冈区域的Amazon WorkMail页面**：

   https://us-west-2.console.aws.amazon.com/workmail/v2/home?region=us-west-2#

2. 您也可以使用亚马逊云科技管理控制台 ，在页面顶部搜索WorkMail进入 Amazon WorkMail 控制台

   https://us-west-2.console.aws.amazon.com/console/home?region=us-west-2
   
   ![image-20220910181247043](/aws-workshops/workmail/images/1-create-1.png)

#### 步骤 2：设置您的 Amazon WorkMail 站点

要使用 Amazon WorkMail，您必须首先创建一个组织。 一个亚马逊云账户可以拥有多个 Amazon WorkMail 组织。 创建组织时，您还可以为组织选择域并设置用户目录和加密设置.

1. 创建组织。单击橙色的“**create organization**”按钮。

   ![image-20220910191938439](/aws-workshops/workmail/images/1-create-2.png)

2. 在创建组织时，需为组织选择域。本次实验您选择免费测试域“**Free Test Domain**”并填写名字，例如**XXX-workmail**。其他保持默认，在页面底部点击橙色创建组织“**create organization**”按钮。

   - *使用免费测试 Amazon WorkMail 提供的域。 您可以使用测试域探索 Amazon WorkMail*
   - *测试邮件域不是 用于长期使用。 我们强烈建议您添加您自己的域并将其用作默认域***
   - *测试邮件域发送邮件有一定限制，即每个亚马逊云账户每天使用任何测试邮件域，**最多只能向200个收件人发送邮件***
   - *填写的Alias会成为Web页面登录的入口，**提交后后无法修改***

   ![image-20220910193652581](/aws-workshops/workmail/images/1-create-3.png)

3. 大概等待约30秒时间，当组织的status 是Active即处于活动状态，随后您可以点击您的WorkMail组织，进入到组织控制台中，并向其添加用户(User)。

   ![image-20220910193948353](/aws-workshops/workmail/images/1-create-4.png)

#### 步骤 3：设置您的WorkMail用户

1. 创建组织内的用户。在左侧菜单栏选择“组织”(**Organization**)下的“用户”(**User**)。

   ![image-20220911132305564](/aws-workshops/workmail/images/1-create-5.png)

2. 点击右上角的橙色按钮“**Create User**"，创建一个新的用户。

   ![image-20220911135443537](/aws-workshops/workmail/images/1-create-6.png)

3. 在用户创建用户信息界面中，在用户名(**User name**)字段中，输入用户的名称，如user，名称也会出现在下方电子邮件地址中。在显示名称(**Display name**)框中，输入用户的显示名称。在设置电子邮件(**Email setup**)中，输入密码(**password**)并重复密码(**repeat password**)。最后，点击右下角橙色按钮，创建用户(**create user**)。

   ![image-20220911135738209](/aws-workshops/workmail/images/1-create-7.png)

   ![image-20220911135815475](/aws-workshops/workmail/images/1-create-8.png)

4. 用户(**User**)创建成功。

   ![image-20220911140629039](/aws-workshops/workmail/images/1-create-9.png)

#### 步骤 4：通过Web登陆使用WorkMail

1. 进入web 操作页面。点击左侧菜单的组织(**Organization**) ，在用户登录(**User Login**) 的下方即有web操作Workmail的入口。

   ![image-20220912234146232](/aws-workshops/workmail/images/1-create-10.png)

2. 点击链接，登入Workmail。输入刚刚创建的账号密码。

   ![image-20220911140842323](/aws-workshops/workmail/images/1-create-11.png)

3. 登入之后就可以按照平常的邮件客户端的步骤来操作。选择**new item**中的**new email**创建邮件并发送给另外一个邮箱做测试。

   ![image-20220911140943832](/aws-workshops/workmail/images/1-create-12.png)

   ![image-20220911141219527](/aws-workshops/workmail/images/1-create-13.png)

   ![image-20220911141246155](/aws-workshops/workmail/images/1-create-14.png)
