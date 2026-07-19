---
title: "总结与参考"
weight: 12
type: workshops
---
{{% workshop-alert type="success" title="恭喜您！" %}}
您已经完成本次动手训练营，相信您对亚马逊云中的网络、计算资源以及数据库有了深入的了解。
{{% /workshop-alert %}}


本次动手训练营，您在亚马逊云科技上使用VPC向导规划了您在云中网络环境。采用两层架构，在EC2上部署了WordPress，同时使用Amazon RDS用于后端服务的数据库，最后测试了Amazon RDS的多可用区自动故障转移功能。

在动手训练营的最后，为您提供一些参考文档，帮助您更深入的了解亚马逊云科技的服务。

Amazon VPC:

- [服务及定价信息](https://aws.amazon.com/cn/vpc/)
- [Amazon VPC文档(什么是VPC？)](https://docs.aws.amazon.com/zh_cn/vpc/latest/userguide/what-is-amazon-vpc.html)
- [什么是子网？](https://docs.aws.amazon.com/zh_cn/vpc/latest/userguide/configure-subnets.html#subnet-basics)
- [什么是互联网网关（IGW）？](https://docs.aws.amazon.com/zh_cn/vpc/latest/userguide/VPC_Internet_Gateway.html)
- [什么是路由表？](https://docs.aws.amazon.com/zh_cn/vpc/latest/userguide/VPC_Route_Tables.html)

Amazon EC2实例:

- [服务及定价信息](https://aws.amazon.com/cn/ec2/)
- [Amazon EC2文档](https://docs.aws.amazon.com/zh_cn/ec2/)
- [实例类型介绍](https://aws.amazon.com/cn/ec2/instance-types/)
- [实例类型筛选对比](https://console.aws.amazon.com/ec2/home#InstanceTypes:)

Amazon RDS:

- [服务及定价信息](https://aws.amazon.com/cn/rds/)
- [Amazon RDS文档](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/UserGuide/Welcome.html)


---

如果您需要清理本次动手训练营创建的资源，请参考以下文档：

- [删除数据库实例](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/UserGuide/USER_DeleteInstance.html#USER_DeleteInstance.Deleting)
- [终止EC2实例](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/terminating-instances.html#terminating-instances-console)
- [删除VPC](https://docs.aws.amazon.com/zh_cn/vpc/latest/userguide/working-with-vpcs.html#VPC_Deleting)
