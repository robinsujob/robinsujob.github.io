---
title: "8.【提升数据库的安全性】为WordPress数据库创建专属的用户"
weight: 10
type: workshops
---
保护数据库免遭未经授权的访问至关重要。在本节中，我们将通过设定专用的用户而不是超级用户来实现对数据库的访问限制。

#### 8.1 配置环境变量

在会话窗口中输入以下命令，为 MySQL 主机设置环境变量。请确保将**您的数据库终端节点地址**替换为您的 RDS 实例的主机名。

```shell
export MYSQL_HOST=您的数据库终端节点地址
```

接下来，在终端中运行以下命令以连接到MySQL数据库。将"用户名"和"密码"替换为您在4.4节第七步：创建数据库输入对用户名和密码

```shell
mysql--user=用户名 --passowrd=密码 wordpress;
```

![image-1](/workshops/wordpress-glb/assets/8-improve-security/8-Picture1.png)

#### 8.2 创建数据库用户并授予权限

最后，为您的WordPress应用程序创建一个数据库用户，并授予其访问"wordpress"数据库的权限。

```shell
CREATE USER 'wordpress' IDENTIFIED BY 'wordpress-pass';
GRANT ALL PRIVILEGES ON wordpress.* TO wordpress;
FLUSH PRIVILEGES;
Exit
```

请使用强度更高的密码来保护数据库，不要使用"wordpress-pass"这样的简单密码。

请记下您配置的用户名和密码，在设置 WordPress 安装时将需要这些信息。

![image-2](/workshops/wordpress-glb/assets/8-improve-security/8-Picture2.png)
