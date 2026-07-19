---
title: "2. 环境准备"
weight: 3
type: workshops
---
# 使用AWS Cloud9进行Serverless开发

在开始进行实验之前，您需要准备好云端开发环境。在本次动手训练营中您将使用AWS Cloud9来进行Serverless相关应用的开发。

AWS Cloud9 是一种基于云的集成开发环境 (IDE)，您只需要一个浏览器，即可编写、运行和调试代码。它包括一个代码编辑器、调试程序和终端，并且预封装了适用于 JavaScript、Python、PHP 等常见编程语言的基本工具，您无需安装文件或配置开发计算机，即可开始新的项目。

在本节中，您将创建一个 Cloud9 环境用于后续的动手训练营的操作。

#### 1. 进入Cloud9服务

在查找服务处搜索Cloud9，并点击进入服务面板。

![](/workshops/glb-sam-lwa/assets/3-init-environment/1-cloud9.png)

#### 2. 创建Cloud9 环境

点击右上角橙色”创建环境“按钮。

![](/workshops/glb-sam-lwa/assets/3-init-environment/2-create-cloud9.png)

在创建环境界面中，为您的 AWS Cloud9 环境分配一个账户内唯一且符合命名要求的名称。例如：**Serverless-Dev**，机型选择m5.large。

![](/workshops/glb-sam-lwa/assets/3-init-environment/3-cloud9-config.png)

其他部分配置保持默认，在页面底部点击橙色的 **创建** 按钮创建环境。 环境的创建将花费1-2分钟的时间。

![](/workshops/glb-sam-lwa/assets/3-init-environment/4-confirm-create.png)

#### 3. 进入Cloud9 环境

在 AWS Cloud9 主页面**环境**列表里，点击 **打开** 打开创建的环境。

![](/workshops/glb-sam-lwa/assets/3-init-environment/5-open-cloud9.png)

您可以看到如图所示的开发界面。

![](/workshops/glb-sam-lwa/assets/3-init-environment/6-ide.png)

#### 4. 修改Cloud9磁盘大小

默认Cloud 9的EBS卷是10GB，后续实验预计需要30GB空间，我们将使用脚本将Cloud9的EBS磁盘扩容至30GB。

创建`resize.sh`，并将以下内容粘贴至文件中：

```shell

#!/bin/bash

# Specify the desired volume size in GiB as a command line argument. If not specified, default to 20 GiB.
SIZE=${1:-20}

# Get the ID of the environment host Amazon EC2 instance.
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
INSTANCEID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/instance-id 2> /dev/null)
REGION=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/placement/region 2> /dev/null)

# Get the ID of the Amazon EBS volume associated with the instance.
VOLUMEID=$(aws ec2 describe-instances \
  --instance-id $INSTANCEID \
  --query "Reservations[0].Instances[0].BlockDeviceMappings[0].Ebs.VolumeId" \
  --output text \
  --region $REGION)

# Resize the EBS volume.
aws ec2 modify-volume --volume-id $VOLUMEID --size $SIZE

# Wait for the resize to finish.
while [ \
  "$(aws ec2 describe-volumes-modifications \
    --volume-id $VOLUMEID \
    --filters Name=modification-state,Values="optimizing","completed" \
    --query "length(VolumesModifications)"\
    --output text)" != "1" ]; do
sleep 1
done

# Check if we're on an NVMe filesystem
if [[ -e "/dev/xvda" && $(readlink -f /dev/xvda) = "/dev/xvda" ]]
then
# Rewrite the partition table so that the partition takes up all the space that it can.
  sudo growpart /dev/xvda 1
# Expand the size of the file system.
# Check if we're on AL2 or AL2023
  STR=$(cat /etc/os-release)
  SUBAL2="VERSION_ID=\"2\""
  SUBAL2023="VERSION_ID=\"2023\""
  if [[ "$STR" == *"$SUBAL2"* || "$STR" == *"$SUBAL2023"* ]]
  then
    sudo xfs_growfs -d /
  else
    sudo resize2fs /dev/xvda1
  fi

else
# Rewrite the partition table so that the partition takes up all the space that it can.
  sudo growpart /dev/nvme0n1 1

# Expand the size of the file system.
# Check if we're on AL2 or AL2023
  STR=$(cat /etc/os-release)
  SUBAL2="VERSION_ID=\"2\""
  SUBAL2023="VERSION_ID=\"2023\""
  if [[ "$STR" == *"$SUBAL2"* || "$STR" == *"$SUBAL2023"* ]]
  then
    sudo xfs_growfs -d /
  else
    sudo resize2fs /dev/nvme0n1p1
  fi
fi
```

并在终端中执行：

```shell
chmod +x resize.sh
./resize.sh 30
```

随后您可以通过`df -h`指令查看磁盘大小，并进行确认。

![](/workshops/glb-sam-lwa/assets/3-init-environment/7-resize-ebs.png)

#### 5. 检查已安装好的软件及命令行

Cloud9已经预安装好常见的开发环境，执行以下命令检查对应的版本：

```shell
aws --version
docker --version
sam --version
java --version
python3 --version
```

#### 6. 升级 SAM 版本至最新版本

使用以下命令将SAM更新至最新版本：

```shell
wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install --update
rm -rf aws-sam-cli-linux-x86_64.zip
rm -rf sam-installation
sam --version 
```
