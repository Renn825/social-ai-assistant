# API 文档

完整交互式文档见 `/docs`。

除 `/api/v1/health` 外，所有接口都需要 `X-API-Key` 请求头。

## 健康检查

```http
GET /api/v1/health
```

## 导入本地样例数据

```http
POST /api/v1/imports
Content-Type: application/json
X-API-Key: dev-api-key

{
  "posts_file": "xiaohongshu_posts.csv",
  "comments_file": "xiaohongshu_comments.csv"
}
```

## 查询帖子

```http
GET /api/v1/posts?platform=xiaohongshu&limit=20
X-API-Key: dev-api-key
```

## 创建分析任务

```http
POST /api/v1/analysis/jobs
Content-Type: application/json
X-API-Key: dev-api-key

{
  "note_ids": [1, 2, 3]
}
```

## 查询分析任务

```http
GET /api/v1/analysis/jobs/1
X-API-Key: dev-api-key
```

## 生成分析报告

```http
POST /api/v1/reports
Content-Type: application/json
X-API-Key: dev-api-key

{
  "platform": "xiaohongshu",
  "report_date": "2026-09-02",
  "style": "weekly",
  "format": "markdown"
}
```

## 生成周报

```http
POST /api/v1/reports/weekly?platform=xiaohongshu
X-API-Key: dev-api-key
```

## 下载报告

```http
GET /api/v1/reports/1/download?format=markdown
X-API-Key: dev-api-key
```

支持的格式：`markdown`、`html`、`json`。
