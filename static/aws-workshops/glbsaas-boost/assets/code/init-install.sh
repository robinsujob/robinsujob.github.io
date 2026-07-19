#!/bin/bash
read -p "输入您的邮箱，用于接收SaaS Boost登陆用户名和密码: " email
echo -e "1\n\nworkshop\n$email\n$email\n\nn\nn\ny\n" > saas-boost-init.data