import time


def _wait_for_job(client, api_headers, job_id: int, timeout: float = 3.0) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        response = client.get(
            f"/api/v1/analysis/jobs/{job_id}",
            headers=api_headers,
        )
        body = response.json()
        if body["status"] in {"completed", "failed"}:
            return body
        time.sleep(0.05)
    raise AssertionError("analysis job did not finish in time")


def test_analysis_job_completes(client, api_headers):
    client.post("/api/v1/mock-data/load", headers=api_headers)
    posts = client.get("/api/v1/posts", headers=api_headers).json()
    note_ids = [posts[0]["id"], posts[1]["id"]]

    response = client.post(
        "/api/v1/analysis/jobs",
        json={"note_ids": note_ids},
        headers=api_headers,
    )
    assert response.status_code == 200
    job = response.json()
    job = _wait_for_job(client, api_headers, job["id"])

    assert job["status"] == "completed"
    assert job["result"] is not None
    assert len(job["result"]["items"]) == 2
    assert set(job["result"]["items"][0]) >= {
        "summary",
        "sentiment",
        "keywords",
        "topics",
        "content_suggestions",
        "copy_suggestions",
    }
