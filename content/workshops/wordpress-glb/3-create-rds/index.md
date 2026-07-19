---
title: "3. 创建Amazon RDS for MySQL数据库"
weight: 5
type: workshops
---
在本模块中，您将为 WordPress 站点创建 MySQL 数据库。在您创建数据库之前，让我们了解一下为何 Amazon RDS 能很好地满足您的数据库需求。

WordPress的内容需要永久存储在某个地方。WordPress 使用 MySQL 数据库来存储这些内容。维护您的 WordPress 站点数据库至关重要。您的数据库实例中保存关于您的 WordPress 站点的所有重要数据。如果数据库发生故障，您的网站可能也会随之崩溃，您甚至可能会丢失数据。

许多 WordPress 安装指南将用于WordPress的MySQL部署在与WordPress的同一台服务器上。虽然这可能足以满足初始需求，但出于以下几个原因，您可能并不希望 MySQL 数据库与 WordPress 安装到相同服务器上，因为：

- MySQL 和 WordPress 将争用同一服务器上的计算资源，这可能会降低站点性能。
- 随着您的站点变得越来越受欢迎，您无法通过添加额外的 WordPress 服务器来横向扩展 WordPress。
- 您要负责执行所有数据库维护任务，包括数据库备份和安全升级。

通过使用 Amazon RDS for MySQL，可以消除这些问题。数据库与WordPress部署在不同的实例中，因此，它们将不会争用资源。此外，您可以创建多个WordPress服务实例，并分别连接到Amazon RDS for MySQL的实例，从而实现横向扩展站点。最后，Amazon RDS for MySQL 能自动执行备份和安装安全补丁，有效帮助您管理数据库。

在下面的步骤中，您将使用亚马逊云科技管理控制台启动Amazon RDS for MySQL 数据库。

#### 3.1 搜索RDS服务

在页面顶部“服务”处搜索RDS，并点击，进入RDS控制面板

![image-20221012091847879](/workshops/wordpress-glb/assets/3-create-rds/1-search-rds.png)

#### 3.2 创建数据库子网组

为了确保数据库在私有子网中部署，您首先需要在创建数据库之前使用[数据库子网组](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html#USER_VPC.Subnets)来为数据库准备网络环境。数据库子网组是您在 VPC 中创建并随后指定给数据库实例的子网集合。通过数据库子网组，您可以在创建数据库实例时指定特定的 VPC。

在左侧菜单栏选择子网组，单击橙色的"**创建数据库子网组**"按钮。填写子网组名称**wordpress-db-subnet-group**、子网组描述，并选择名称为WordPress的VPC

![image-20221012092130901](/workshops/wordpress-glb/assets/3-create-rds/2-subnet-group.png)

#### 3.3 添加子网至子网组

根据之前创建VPC时记录的子网信息，在添加子网区域中，选择子网所在的可用区。

![image-20221012093846158](/workshops/wordpress-glb/assets/3-create-rds/3.1-add-subnet.png)

在选择子网下拉框中选择不同可用区中的两个私有子网。检查相应信息，并点击橙色“创建”按钮

![image-20221012094400116](/workshops/wordpress-glb/assets/3-create-rds/3.2-verify-subnet.png)

#### 3.4 创建RDS数据库

在左侧菜单栏选择控制面板，单击橙色的“**创建数据库**”按钮开始创建数据库。

![image-20221012102720843](/workshops/wordpress-glb/assets/3-create-rds/4-create-db.png)

#### 3.5 选择数据库引擎

单击橙色的“**创建数据库**”按钮开始创建数据库，选择“标准创建”，之后选择要使用的数据库引擎。WordPress 使用 MySQL，因此选择MySQL引擎。

![image-20221012103105715](/workshops/wordpress-glb/assets/3-create-rds/5-chose-engine.png)

#### 3.6 选择数据库创建模版

在创建向导的模板部分中，预置了生产和开发/测试两种模版。生产模版为您预置了一下配置：

- 更大的数据库实例类，用于提高性能；
- [多可用区部署](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html)，用于在发生基础设施问题时自动执行故障转移和恢复；
- 适用于[磁盘存储的预置 IOPS](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/UserGuide/CHAP_Storage.html#USER_PIOPS)，用于提高 I/O 性能。

本次实验使用**开发/测试模版**,以及**多可用区部署**。

![image-20221117100044015](/workshops/wordpress-glb/assets/3-create-rds/6-rds-template.png)

#### 3.7 设置数据库的实例名称、管理用户和密码

您将为MySQL 您将为 MySQL 部署指定身份验证设置，其中包括数据库名称、主用户名和密码。

在设置部分中，输入**wordpress-db-instance**作为数据库实例标识符，然后指定数据库的主用户名和密码。选择安全程度高的密码以帮助保护您的数据库。**妥善保管并记录用户名和密码，以供后面的模块使用。**

![image-20221012103631934](/workshops/wordpress-glb/assets/3-create-rds/7-rds-password.png)

#### 3.8 选择数据库实例类型以及可用性

设置了用户名和密码后，选择有关 MySQL 部署的关键详细信息，包括实例类、存储以及可用性。本实验选择标准类**db.m6g.large**。

![image-20221012103803375](/workshops/wordpress-glb/assets/3-create-rds/8.1-rds-instance.png)

#### 3.9 数据库实例的网络和配置

接下来，您需要配置连接和网络配置。必须在Amazon VPC中创建 Amazon RDS 实例。请选择先前创建的名为WordPress的VPC，自动选择先前创建的子网组。

![image-20221012103954706](/workshops/wordpress-glb/assets/3-create-rds/9-rds-network.png)

#### 3.10 数据库实例的安全组配置

为该数据库实例新建一个安全组，命名为**wordpress-db-sg**。

![image-20221012104047900](/workshops/wordpress-glb/assets/3-create-rds/10-rds-sg.png)

#### 3.11 配置初始化数据库

最后，RDS 还提供了许多其他配置选项，用于自定义您的部署。您需要在此区域中进行一项更改。单击**其他配置**以展开选项。

将初始数据库名称设置为**wordpress**。这将确保 RDS 在初始化时在 MySQL 实例中创建数据库。在连接到数据库时，您将使用此数据库名称。

![image-20221012104407874](/workshops/wordpress-glb/assets/3-create-rds/11-rds-create-db.png)

#### 3.12 完成创建过程

在创建向导的底部，单击橙色的“**创建数据库**”按钮以创建数据库。您应会看到一条成功通知，提示正在创建数据库。创建时间可能需要花费若干分钟，等待创建的同时您可以进行下一模块的步骤。

![image-20221012110122111](/workshops/wordpress-glb/assets/3-create-rds/12-rds-complete.png)

在本模块中，您使用 Amazon RDS 创建了一个完全托管的 MySQL 数据库。后面您将为EC2实例分配一个弹性IP地址，以固定EC2的公有IP地址。
