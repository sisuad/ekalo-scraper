# KiddoWorksheets 爬虫

[中文文档](README_zh.md) | [English](README.md)

一个用于从 KiddoWorksheets.com 下载教育工作表的 Python 网络爬虫。

## 功能特性

- 从 KiddoWorksheets.com 抓取工作表
- 下载 PDF 工作表和直接的图片文件（PNG, JPG 等）
- **支持配置下载格式（PDF/PNG）**
- 按教育类别整理文件
- 生成包含所有工作表信息的 JSON 元数据文件
- Docker 化支持，便于部署和提供一致的运行环境

## 快速开始

### 使用 Docker（推荐）

1. **使用 Docker Compose 构建并运行：**
   ```bash
   docker-compose up -d
   ```
   *注意：服务已配置为优先使用现有镜像，避免重复构建。*

2. **或者手动构建并运行：**
   ```bash
   # 构建镜像
   docker build -t kiddoworksheets-scraper .
   
   # 运行容器
   docker run -v $(pwd)/worksheets:/app/worksheets -v $(pwd)/worksheets.json:/app/worksheets.json kiddoworksheets-scraper
   ```

### 直接使用 Python

1. **安装依赖：**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行爬虫：**
   ```bash
   # 可选：设置环境变量
   export DOWNLOAD_PDFS=false
   export DOWNLOAD_PNGS=true
   
   python scraper.py
   ```

## 配置说明

你可以通过环境变量来控制下载哪些类型的文件。

### 环境变量
| 变量名 | 默认值 | 说明 |
|----------|---------|-------------|
| `DOWNLOAD_PDFS` | `false` | 设置为 `true` 以启用 PDF 下载 |
| `DOWNLOAD_PNGS` | `true` | 设置为 `true` 以启用 PNG 下载 |

### Docker 配置
你可以在 `docker-compose.yml` 中设置这些变量，或者创建一个 `.env` 文件：
```yaml
environment:
  - DOWNLOAD_PDFS=false
  - DOWNLOAD_PNGS=true
```

## 输出内容

- **`worksheets/`** - 包含已下载工作表文件的目录
- **`worksheets.json`** - 按类别组织的元数据 JSON 文件

## Docker 文件说明

- **`Dockerfile`** - 基于 Python 3.12 slim 镜像的多阶段构建文件
- **`docker-compose.yml`** - 简易编排文件，包含卷挂载配置。已优化以复用现有镜像。
- **`.dockerignore`** - 排除 Docker 上下文中不需要的文件
- **`requirements.txt`** - Python 依赖列表

## 依赖库

- `requests` - 处理 HTTP 请求
- `beautifulsoup4` - 解析 HTML/XML
- `lxml` - XML 解析后端

## 致谢

本项目是基于 Abenezer46 的 [ekalo-scraper](https://github.com/Abenezer46/ekalo-scraper) 进行的修改和优化。特别感谢原作者的贡献。

## 许可证

本项目基于 [MIT License](LICENSE) 授权。
