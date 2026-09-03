# API 文档

完整交互式文档见 `/docs`。

除 `/api/v1/health` 外，所有接口都需要 `X-API-Key` 请求头。

## 载入模拟数据

```http
POST /api/v1/mock-data/load
X-API-Key: dev-api-key-change-me
```

## 创建采集任务

```http
POST /api/v1/posts/collect
Content-Type: application/json
X-API-Key: dev-api-key-change-me

{
  "platform": "xiaohongshu",
  "keyword": "AI 工具",
  "limit": 20
}
```

## 创建分析任务

```http
POST /api/v1/analysis/jobs
Content-Type: application/json
X-API-Key: dev-api-key-change-me

{
  "note_ids": [1, 2, 3]
}
```

## 生成分析报告

```http
POST /api/v1/reports
Content-Type: application/json
X-API-Key: dev-api-key-change-me

{
  "platform": "xiaohongshu",
  "report_date": "2026-09-02",
  "style": "weekly",
  "format": "markdown"
}
```

## Agent 对话

```http
POST /api/v1/assistant/chat
Content-Type: application/json
X-API-Key: dev-api-key-change-me

{
  "message": "帮我生成一份 AI 工具周报"
}
```
