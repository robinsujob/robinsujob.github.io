---
title: "更换默认域"
weight: 6
type: workshops
---

在上一节中我们使用了自己的域名作为Amazon WorkMail的域并进行了验证，同时自定义了Mail From域提升了送达率。

在本节中我们将切换自己的域名作为发送邮件的默认域，并创建一个新的用户，同时将原有测试域账户迁移至验证域。

1. 将验证域设置为默认域。在左边菜单栏选择域(**domain**)，选择已经完成验证的域并点击设置为默认(**Set as default**)。

   ![image-20220912142022958](/workshops/workmail/images/5-set-1.png)

2. 在左侧出菜单栏选择**User**，创建一个已经验证域的用户。

   ![image-20220912142241540](/workshops/workmail/images/5-set-2.png)

3. 在邮件设置(**email setup**)的邮件地址栏位(**email address**)中输入名称如”**domain**”并选择已验证域。输入密码并创建用户(**create user**)。

   ![image-20220912151405921](/workshops/workmail/images/5-set-3.png)

4. 在Workmail左侧菜单栏中选择用户(users)即可看到所设置的两个用户，一个是基于测试域的用户，另一个则是基于验证域的用户。

   ![image-20220912151619904](/workshops/workmail/images/5-set-4.png)

5. 使用Web的邮件界面，使用新的验证域用户，从验证域邮箱发送邮件至测试域。

   ![image-20220912151926513](/workshops/workmail/images/5-set-5.png)

   ![image-20220912151947313](/workshops/workmail/images/5-set-6.png)

6. 打开浏览器的无痕标签页查看测试域下的用户邮件【无痕标签页的目的是避免退出先前登陆的WorkMail账户】

   ![image-20220912152121824](/workshops/workmail/images/5-set-7.png)

7. 为测试域的用户更换为验证域。在左侧菜单栏中选择用户(**users**)，勾选测试域的用户并点击上方”**Disable**”。

   ![image-20220912152359068](/workshops/workmail/images/5-set-8.png)

8. 点击“**Disable**”

   ![image-20220912152421317](/workshops/workmail/images/5-set-9.png)

9. 勾选测试域的用户并点击上方”**enable**”

   ![image-20220912152446249](/workshops/workmail/images/5-set-10.png)

10. 将测试域用户的域名更改为验证域

    ![image-20220912152531474](/workshops/workmail/images/5-set-11.png)

11. 此时您已经完成了测试域到默认域的更换，包括原有测试域中的用户。

    ![image-20220912152558383](/workshops/workmail/images/5-set-12.png)

至此，您已经完成所有关于使用自己域名的企业邮箱，最后我们将带领您通过邮件客户端使用WorkMail。
