def test_load_mock_data(client, api_headers):
    response = client.post("/api/v1/mock-data/load", headers=api_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["notes_created"] == 5
    assert body["comments_created"] == 10

    posts_response = client.get("/api/v1/posts", headers=api_headers)
    assert posts_response.status_code == 200
    posts = posts_response.json()
    assert len(posts) == 5

    post_id = posts[0]["id"]
    detail_response = client.get(f"/api/v1/posts/{post_id}", headers=api_headers)
    assert detail_response.status_code == 200
    assert len(detail_response.json()["comments"]) > 0
