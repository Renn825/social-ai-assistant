# 系统架构

## 总体设计

系统分为四层：

1. 采集层：MediaCrawler / Playwright 获取公开内容。
2. 数据层：清洗、去重、入库，使用 SQLModel + PostgreSQL/SQLite。
3. 智能层：LLM 负责摘要、情感分析、报告和文案生成；Agent 负责工具编排。
4. 服务层：FastAPI 提供 REST API，APScheduler 负责定时任务。

## 数据流

```text
采集任务
  -> 数据采集
  -> 去重清洗
  -> 入库
  -> AI 分析/生成
  -> 报告/接口输出
```

## 扩展点

- 将 `app/services/crawler.py` 中的 MediaCrawler 调用替换为真实解析逻辑。
- 在 `app/agents/assistant.py` 中接入 OpenAI function calling 或 LangGraph。
- 在 `app/services/ai.py` 中增加流式输出、重试、模型降级。

