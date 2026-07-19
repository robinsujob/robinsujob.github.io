---
title: "7. 配置 WordPress"
weight: 9
type: workshops
---
到目前为止，您已完成了许多配置设置。您创建了 RDS 实例和 EC2 实例。您已允许从 EC2 实例通过网络访问 RDS 实例。您还学习了如何通过 SSH或者会话连接器访问 EC2 实例。

在本模块中，您将完成剩余的工作，以将 WordPress 网站上线。本模块结束后，您可从世界各地通过浏览器访问您安装好的 WordPress 网站。

#### 7.1 测试WordPress默认页面

通过在浏览器中访问 EC2 实例的公有 DNS，您可以看到 Apache Web 服务器正在运行，并且安全组已正确配置。

转到 [EC2 实例页面](https://ap-northeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-northeast-1#Instances:v=3;instanceState=running)并找到您的实例。在下面的**详细信息**中，找到实例的**公有 (IPv4)地址**。

![image-1](/workshops/wordpress-glb/assets/7-configure-wordpress/7-Picture1.png)

复制IP地址，在 Web 浏览器中输入此值。然后，您会看到 WordPress安装页面。

![image-20221118100121425](/workshops/wordpress-glb/assets/7-configure-wordpress/7-Picture2.png)

#### 7.2 使用WordPress安装界面添加数据库信息

点击现在开始，在数据库配置页面填写对应信息。

* **数据库名**：在第3节3.7步：[创建数据库输入的数据库名](/workshops/wordpress-glb/3-create-rds/#3.7)

* **用户名及密码**：在第3节3.7步：[创建的主用户名及密码](/workshops/wordpress-glb/3-create-rds/#3.7)

* **数据库主机**：主机名为数据库实例的终端节点，在数据库实例的详细信息中查看。

填写完毕后，点击提交，连接数据库成功。您可以自行配置后续有关WordPress的设定。

**注意：我们建议遵循最小权限原则，创建一个专用于WordPress的数据库用户，而不是使用RDS数据库的管理用户。详情可以参考[第8节提升数据库的安全性](/workshops/wordpress-glb/8-improve-security/)，并在此步替换连接的数据库用户名和密码。**

![image-3](/workshops/wordpress-glb/assets/7-configure-wordpress/7-Picture3.png)

![image-4](/workshops/wordpress-glb/assets/7-configure-wordpress/7-Picture4.png)

![image-5](/workshops/wordpress-glb/assets/7-configure-wordpress/7-Picture5.png)


以上就是所有步骤。至此，您安装好了可公开访问的在线 WordPress 网站，它使用 Amazon RDS 上的完全托管的 MySQL 数据库。
