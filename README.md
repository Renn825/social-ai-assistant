# 社媒数据智能分析与生成助手

一个基于 FastAPI、LangGraph 和 PostgreSQL/pgvector 的社媒数据分析 MVP，支持本地样例数据导入、清洗、AI 分析、情感分析、主题提取和周报生成。

## 功能

- 导入小红书/抖音 CSV 样例数据
- 数据清洗、去重、结构化入库
- AI 帖子摘要、评论情感分析、主题提取
- 自动生成 Markdown/HTML/JSON 周报
- 简单的 API Key 鉴权和统一错误处理
- Docker Compose 一键启动 PostgreSQL 和 API

## 快速开始

```bash
cp .env.example .env
docker compose up --build
```

服务启动后访问：

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

本地导入样例数据：

```bash
curl -X POST http://localhost:8000/api/v1/imports \
  -H "X-API-Key: dev-api-key" \
  -H "Content-Type: application/json" \
  -d '{"posts_file":"xiaohongshu_posts.csv","comments_file":"xiaohongshu_comments.csv"}'
```

## 环境变量

见 `.env.example`。

## 目录结构

```text
app/
  api/          # FastAPI 路由
  core/         # 配置、安全、日志
  db/           # 数据库连接和基础模型
  models/       # SQLAlchemy 模型
  schemas/      # Pydantic 模型
  services/     # 数据清洗、导入、AI 分析、报告
data/samples/   # 样例数据
prompts/        # Prompt 模板
tests/          # 测试
outputs/        # 生成报告
```
