---
title: "9.【探索】有关RDS多可用区实例部署的故障转移测试"
weight: 11
type: workshops
---
在[第3节3.8步](/aws-workshops/wordpress-glb/3-create-rds/#3.8)，我们选择了多可用区实例部署创建了RDS数据库实例。在多可用区数据库实例部署中，Amazon RDS 会自动在不同可用区中配置和维护一个同步备用副本。主数据库实例将跨可用区同步复制到备用副本，以提供数据冗余并在系统备份期间将延迟峰值降至最小。

![image-1](/aws-workshops/wordpress-glb/assets/9-az-failover/9-Picture1.png)

在具有多可用区的Amazon RDS中，详情部分呈现了主要可用区和辅助可用区。

![image-2](/aws-workshops/wordpress-glb/assets/9-az-failover/9-Picture2.png)

上图中已经显示，可用区(主节点)：ap-northeast-1a，辅助区(备用节点)：ap-northeast-1c。现在让我们通过重新启动模拟一个场景，我们将使辅助区域成为可用区。选择重启实例，通过重启故障转移来测试。

![image-3](/aws-workshops/wordpress-glb/assets/9-az-failover/9-Picture3.png)

在可以连接到数据库实例的EC2上，我们可以执行一跳循环语句，观察RDS主备切换的过程。

```shell
while true; do host $数据库实例终端节点 ; sleep 1; done
```

![image-4](/aws-workshops/wordpress-glb/assets/9-az-failover/9-Picture4.png)

可以看到RDS的终端节点IP从刚开始的10.0.144.174改成 10.0.141.121，完成了一次切换。

![image-5](/aws-workshops/wordpress-glb/assets/9-az-failover/9-Picture5.png)

完成故障转移后，RDS 控制台还需要一段时间才能反映新的可用区。再次打开实例详情，可以看到可用区与辅助区域已经更改了，可用区变为辅助区域，辅助区域变为可用区，完成了切换。

![image-6](/aws-workshops/wordpress-glb/assets/9-az-failover/9-Picture6.png)

故障转移时间通常为 60–120 秒。通过测试我们可以看出，Amazon RDS 会自动处理故障转移，因此，您可以尽快恢复数据库操作而无需管理干预。托管的RDS多可用区实例部署节省了我们在数据库高可用场景下的维护成本。我们不需要考虑主备切换时数据库终端节点的变化，也不需要考虑主备数据库之间的备份方式。
