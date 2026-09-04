# 求职项目交接文档

## 一句话目标

求职方向是“AI Agent + 传统后端业务”，项目配比约 Agent 60%、传统后端业务 40%；传统后端以 Java 为主，AI 侧补充 Python/FastAPI 项目。

## 必须维护的两个项目

1. 企业智能知识库与流程自动化平台
   - 定位：Java 企业后端 + RAG + 工作流审批 + Agent。
   - 重点：知识库、流程自动化、RAG、MCP、Human-in-the-loop。

2. 社媒数据智能分析与生成助手
   - 定位：Python/FastAPI + LangGraph + 数据采集 + AI 分析与内容生成。
   - 当前仓库就是该项目，见当前目录。

## 当前仓库状态

- 项目：社媒数据智能分析与生成助手
- 路径：`C:\code\work\social-ai-assistant`
- GitHub：https://github.com/Renn825/social-ai-assistant
- 分支：`master`
- 远程：`origin`

## 当前项目已实现能力

- 本地 CSV 样例数据导入。
- 数据清洗、去重、结构化入库。
- LangGraph 分析：摘要、情感、主题、洞察。
- 周报生成，支持 Markdown / HTML / JSON。
- 帖子分页与时间过滤查询。
- API Key 鉴权。
- Docker Compose + Alembic 迁移。

## 关键入口文件

- `app/main.py`
- `app/api/router.py`
- `app/services/local_import.py`
- `app/services/analysis.py`
- `app/services/report.py`
- `docs/API.md`
- `docs/ARCHITECTURE.md`
- `docs/PRODUCT_DESIGN.md`

## 运行方式

```bash
cd C:\code\work\social-ai-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

或：

```bash
docker compose up --build
```

## 必须遵守的工程规则

- 每次代码或文档修改后，都要 `git commit`。
- 每次提交后，推送到 GitHub：`git push origin master`。
- 代码改动必须配套或更新测试。
- 交付前必须运行验证。
- 回复用户默认使用中文。

## 参考仓库

- `references/MediaCrawler`：后续接入真实社媒采集。
- `references/fastapi-langgraph-template`：FastAPI + LangGraph 工程结构参考。

## 下一步建议

1. 补齐本地测试环境并运行 `pytest`。
2. 接入真实 MediaCrawler 采集。
3. 增加报告定时任务。
4. 考虑加入 RAG 问答或简单 Web 看板。
5. 回到“企业智能知识库与流程自动化平台”项目，完成 Java 项目复现。
