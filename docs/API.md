# API 文档

完整交互式文档见 `/docs`。

## 创建采集任务

```http
POST /api/v1/posts/collect
Content-Type: application/json

{
  "platform": "xiaohongshu",
  "keyword": "AI 工具",
  "limit": 20
}
```

## 生成分析报告

```http
POST /api/v1/reports
Content-Type: application/json

{
  "platform": "xiaohongshu",
  "report_date": "2026-09-02",
  "style": "weekly"
}
```

## Agent 对话

```http
POST /api/v1/assistant/chat
Content-Type: application/json

{
  "message": "帮我生成一份 AI 工具周报"
}
```

