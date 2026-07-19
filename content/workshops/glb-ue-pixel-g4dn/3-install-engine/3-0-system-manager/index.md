---
title: "3.1配置System Manager"
weight: 1
type: workshops
---
Systems Manager 是一项灵活易用的管理服务，让企业能够安全地管理在本地或亚马逊云科技中运行的工作负载。通过System Manager的会话管理器与Fleet Manager，您可以通过浏览器连接到EC2实例，而无需在防火墙或 Amazon Virtual Private Cloud (Amazon VPC) 安全组上打开特定端口。有关更多信息，请参阅[AWS Systems Manager Session Manager](https://docs.aws.amazon.com/zh_cn/systems-manager/latest/userguide/session-manager.html)与[AWS Systems Manager Fleet Manager](https://docs.aws.amazon.com/zh_cn/systems-manager/latest/userguide/fleet.html)。

以下您将通过System Manager的“快速设置”完成有关Systems Manage的配置性操作。

1. 在控制台搜索**Systems Manager**，并点击，进入Systems Manager控制面板:

![image-20221103181156710](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-0-system-manager/1-system-manager.png)
2. 点击橙色左侧“快速设置”选项。

![image-20221103181248886](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-0-system-manager/2-quick-start.png)
3. 在页面右侧，确认当前区域，点击橙色“开始使用”按钮。

![image-20221103181419903](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-0-system-manager/3-start-png.png)

4. 在第二个跳转界面点击Host Management下的创建按钮。
     ![image-20221103181542389](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-0-system-manager/4-host-mgmt.png)
5. Targets根据需要选择，region即实例所在的region，instances可以选择全部，其他可以保持默认，完成右下角橙色“创建”按钮。

![image-20221103181627271](/workshops/glb-ue-pixel-g4dn/assets/3-install-engine/3-0-system-manager/5-create.png)

完成上述步骤，将会为您创建一个名为AmazonSSMRoleForlnstancesQuickSetup的IAM角色
