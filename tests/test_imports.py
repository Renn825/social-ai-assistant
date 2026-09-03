def test_import_local_csv(client, api_headers):
    response = client.post(
        "/api/v1/imports",
        json={
            "posts_file": "xiaohongshu_posts.csv",
            "comments_file": "xiaohongshu_comments.csv",
        },
        headers=api_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["imported_posts"] >= 4
    assert body["imported_comments"] >= 5
