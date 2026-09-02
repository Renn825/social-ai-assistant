# 部署说明

## 本地开发

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

## Docker Compose

```bash
copy .env.example .env
docker compose up --build
```

生产环境至少需要修改：

- 数据库密码
- LLM API Key
- CORS 允许来源
- 关闭 mock crawler
- 配置真实 MediaCrawler 目录

