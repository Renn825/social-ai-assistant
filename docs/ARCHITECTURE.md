# 系统架构

## 总体设计

系统分为五层：

1. 采集层：MediaCrawler / Playwright 获取公开内容。
2. 数据层：本地 CSV 导入、清洗、去重、入库，使用 SQLModel + PostgreSQL/SQLite。
3. 智能层：LLM 负责摘要、情感分析、主题提取、周报和文案生成。
4. Agent 层：LangGraph 编排摘要、情感、主题和洞察节点。
5. 服务层：FastAPI 提供 REST API，APScheduler 负责定时任务。

## 数据流

```text
CSV 样例数据
  -> 数据清洗
  -> 去重入库
  -> LangGraph 分析
  -> 周报生成
  -> Markdown/HTML/JSON 输出
```

## 扩展点

- 将 `app/services/crawler.py` 中的 MediaCrawler 调用替换为真实解析逻辑。
- 在 `app/services/analysis.py` 中扩展 LangGraph 节点，例如加入 RAG 或人工审批。
- 在 `app/services/ai.py` 中增加流式输出、重试、模型降级。
