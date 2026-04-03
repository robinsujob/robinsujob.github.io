# Robin's Space (Hugo Stack)

个人站点 — Hugo Stack 主题版本。

## 快速开始

### 环境要求

- Hugo Extended ≥ v0.157.0（当前 v0.159.2）

### 本地预览

```bash
cd /data/code/hugo-stack-site

# 前台运行（Ctrl+C 停止）
hugo server --bind 0.0.0.0 --port 4002

# 后台运行
nohup hugo server --bind 0.0.0.0 --port 4002 > /tmp/hugo-serve.log 2>&1 &
```

访问 http://localhost:4002 或 Tailscale 内网 IP:4002

### 停止服务

```bash
lsof -ti:4002 | xargs kill
```

### 构建（不启动服务）

```bash
hugo
# 输出到 public/
```

## 目录结构

```
hugo-stack-site/
├── config/_default/
│   ├── hugo.toml        # 基础配置
│   ├── params.toml      # 主题参数（avatar、sidebar、widgets）
│   ├── markup.toml      # Markdown 渲染配置
│   └── menu.toml        # 导航菜单 + 社交链接
├── content/
│   ├── post/            # 博客文章（page bundle 格式）
│   └── page/            # 独立页面（About/Projects/Archives/Search）
├── static/images/       # 图片资源
├── assets/img/          # 主题资源（avatar）
├── themes/hugo-theme-stack/  # Stack 主题
└── README.md
```

## 文章列表

| 文章 | 日期 | 分类 |
|---|---|---|
| China CloudFront SSL Plugin V2 | 2025-08-19 | AWS > CloudFront |
| SageMaker GGUF 模型推理 | 2025-02-12 | AWS > SageMaker |
| API Gateway CORS 配置 | 2024-10-28 | AWS > API Gateway |
| WordPress GenAI Plus | 2024-04-29 | AWS, AI |
| CloudFront SSL 插件部署指南 | 2023-11-15 | AWS > CloudFront |
| ControlNet 艺术二维码 | 2023-09-01 | AI > Stable Diffusion |
| Photography: City Lights | 2024-01-15 | Photography |

## 添加新文章

在 `content/post/` 下创建目录 + `index.md`：

```bash
mkdir -p content/post/my-new-post
```

```yaml
---
title: "文章标题"
date: 2025-01-01
description: "简短描述"
image: /images/posts/my-post/cover.jpg
categories:
  - AWS
tags:
  - tag1
  - tag2
slug: my-new-post
---

正文内容...
```

## 添加摄影作品

同样在 `content/post/` 下创建，category 设为 Photography：

```yaml
---
title: "相册名称"
date: 2025-01-01
categories:
  - Photography
tags:
  - street
  - travel
---

![照片1](/images/photography/photo1.jpg)
![照片2](/images/photography/photo2.jpg)
```

Stack 内置 lightbox，多张图片自动生成画廊效果。

## 三站对比

| 站点 | 端口 | 框架 | 主题 | 路径 |
|---|---|---|---|---|
| Minimal Mistakes | :4000 | Jekyll | MM | /data/code/git-page/ |
| Chirpy | :4001 | Jekyll | Chirpy | /data/code/chirpy-site/ |
| **Stack** | **:4002** | **Hugo** | **Stack** | **/data/code/hugo-stack-site/** |
