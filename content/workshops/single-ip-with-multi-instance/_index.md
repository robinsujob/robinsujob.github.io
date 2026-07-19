---
title: "【电商运营】单IP多人运维环境部署"
weight: 9
type: workshops
shortTitle: "单 IP 多实例运维"
homeTitle: "电商运营 - 单IP多人运维环境部署"
summary: "通过 CloudFormation、NAT Gateway 和 Systems Manager，为多台 Windows EC2 建立共享固定出口 IP 的安全运维环境。"
workshopRoot: true
---
#### 本方案通过一键式的CloudFormation部署，部署单个NAT网关与私有子网的若干EC2实例，运维人员可通过System Manager的端口转发来实现远程登录。该方案可以实现以下目标：

- 通过单个NAT网关及其弹性IP，保证所有私有子网中的EC2实例具有唯一互联网出口，且所有实例的出口互联网IP地址为同一个。

- 通过System Manager Session Manager（会话管理器）的端口转发构建会话隧道（Tunnel），通过隧道连接至私有子网中的EC2 Windows实例

使用 [会话管理器 ](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)来连接您的边缘设备和 Amazon Elastic Compute Cloud (Amazon EC2) 实例，通过交互式、一键式基于浏览器的 shell 或通过 AWS CLI。会话管理器提供安全且可审计的边缘设备和实例管理，无需打开入站端口、维护堡垒主机或管理 SSH 密钥。

#### 通过本方案可以解决以下问题：

- 多人无法同时登录Windows实例
- 开启多个Windows实例时互联网IP地址不一致

该方案架构如图所示：
![](/workshops/single-ip-with-multi-instance/assets/deploy/architecture.png)

#### 费用

本方案主要的费用取决于您所部署的区域、开启实例的大小、硬盘空间、使用时长以及流量费用组成。主要有以下几类服务组成：

- NAT网关
  - 运行时长费用
  - 数据流量处理费用
- 计算资源（实例）
  - 实例类型
  - 实例运行时长
  - 磁盘大小
- 互联网出站流量费用

以us-east-1（弗吉尼亚北部），开启t3.medium机型两台，30GB gp3磁盘，运行24小时为例（不包含数据流量）

- NAT网关
  - 运行时长费用：24h x 0.045 USD = 1.08 USD (网关每小时使用成本)
- 计算资源（实例）
  - 实例类型 x 实例运行时长：2  x 0.06 USD  x 24 hours = 2.88 USD
  - 磁盘大小：
    - 24 total EC2 hours / 730 hours in a month = 0.03 instance months
    - 30 GB x 0.03 instance months x 0.08 USD x 2 = 0.14 USD (EBS Storage Cost)
- 共计：4.1 USD / 1day

**更多费用信息，请参考亚马逊云服务计价器：https://calculator.aws/**

- NAT网关：https://calculator.aws/#/addService/VPC
- 计算资源（实例）：https://calculator.aws/#/addService/ec2-enhancement

#### 参考文档

- [使用 AWS System Manager Sessions Manager 的端口转发功能](https://aws.amazon.com/cn/blogs/china/new-port-forwarding-using-aws-system-manager-sessions-manager/)
- [使用 AWS Systems Manager 转发 Amazon EC2 实例端口](https://aws.amazon.com/cn/blogs/china/forward-amazon-ec2-instance-port-using-aws-systems-manager/)

---

*Contact: Robin Su(usuzhe@amazon.com)*

*Last Update: 2022/12/29*
