def test_generate_markdown_report(client, api_headers):
    client.post("/api/v1/mock-data/load", headers=api_headers)
    response = client.post(
        "/api/v1/reports",
        json={
            "platform": "xiaohongshu",
            "style": "weekly",
            "format": "markdown",
        },
        headers=api_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["format"] == "markdown"
    assert "分析报告" in body["content"]


def test_generate_html_report(client, api_headers):
    client.post("/api/v1/mock-data/load", headers=api_headers)
    response = client.post(
        "/api/v1/reports",
        json={
            "platform": "xiaohongshu",
            "style": "weekly",
            "format": "html",
        },
        headers=api_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["format"] == "html"
    assert "<html" in body["content"]
