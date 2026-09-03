# 社媒数据智能分析与生成助手

一个面向求职与技术复现的完整 AI 应用骨架，覆盖：

- 社媒公开数据采集
- 数据清洗、去重和存储
- FastAPI 后端接口
- API Key 鉴权
- LLM 内容分析、摘要、情感分析
- 分析任务状态管理
- Markdown / HTML 报告生成
- 文案生成
- Agent 工具调用
- 定时任务
- Docker 部署
- Prompt、API、架构和部署文档

## 快速启动

```bash
cd social-ai-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

默认文档地址：

- Swagger：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/v1/health

## 鉴权

除健康检查外，所有 `/api/v1/*` 接口都需要请求头：

```http
X-API-Key: dev-api-key-change-me
```

该值由 `.env` 中的 `SOCIAL_AI_API_KEY` 配置。若为空，则本地开发时暂不校验。

## 核心接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/v1/health` | 健康检查 |
| POST | `/api/v1/mock-data/load` | 载入模拟笔记和评论 |
| GET | `/api/v1/posts` | 查询已采集内容 |
| GET | `/api/v1/posts/{id}` | 查询单条内容及评论 |
| POST | `/api/v1/posts/collect` | 创建采集任务 |
| GET | `/api/v1/tasks` | 查询采集任务 |
| POST | `/api/v1/analysis/summarize` | AI 内容分析 |
| POST | `/api/v1/analysis/copy` | AI 文案生成 |
| POST | `/api/v1/analysis/jobs` | 创建批量分析任务 |
| GET | `/api/v1/analysis/jobs/{id}` | 查询分析任务状态 |
| GET/POST | `/api/v1/reports` | 查询/生成 Markdown 或 HTML 报告 |
| POST | `/api/v1/assistant/chat` | Agent 对话 |

## 示例请求

```bash
# 载入模拟数据
curl -X POST http://127.0.0.1:8000/api/v1/mock-data/load \
  -H "X-API-Key: dev-api-key-change-me"

# 生成 Markdown 报告
curl -X POST http://127.0.0.1:8000/api/v1/reports \
  -H "X-API-Key: dev-api-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{"platform":"xiaohongshu","style":"weekly","format":"markdown"}'
```

## 环境变量

复制 `.env.example` 为 `.env` 后配置：

- `SOCIAL_AI_API_KEY`：API Key
- `SOCIAL_AI_LLM_API_KEY`：OpenAI 兼容 API Key
- `SOCIAL_AI_LLM_BASE_URL`：模型服务地址
- `SOCIAL_AI_LLM_MODEL`：模型名称
- `SOCIAL_AI_DATABASE_URL`：数据库连接串
- `SOCIAL_AI_MOCK_CRAWLER`：无 MediaCrawler 时使用模拟数据

## 项目结构

```text
app/
├── agents/        # Agent 工具与编排
├── api/           # FastAPI 路由
├── core/          # 配置与数据库
├── models/        # SQLModel 数据模型
├── schemas/       # 请求/响应结构
├── services/      # 采集、清洗、AI、分析、报告
└── tasks/         # 定时任务
prompts/           # Prompt 模板
docs/              # 架构、API、部署文档
tests/             # 测试用例
```

## Docker 部署

```bash
copy .env.example .env
docker compose up --build
```
