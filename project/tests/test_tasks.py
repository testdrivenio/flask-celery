import json
from unittest.mock import patch, call

from project.server.tasks import create_task


def test_home(test_app):
    client = test_app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200


def test_task():
    assert create_task.run(1)
    assert create_task.run(2)
    assert create_task.run(3)


@patch("project.server.tasks.create_task.run")
def test_mock_task(mock_run):
    assert create_task.run(1)
    create_task.run.assert_called_once_with(1)

    assert create_task.run(2)
    assert create_task.run.call_count == 2

    assert create_task.run(3)
    assert create_task.run.call_count == 3


def test_task_status(test_app):
    client = test_app.test_client()

    resp = client.post(
        "/tasks",
        data=json.dumps({"type": 0}),
        content_type='application/json'
    )
    content = json.loads(resp.data.decode())
    task_id = content["task_id"]
    assert resp.status_code == 202
    assert task_id

    resp = client.get(f"tasks/{task_id}")
    content = json.loads(resp.data.decode())
    assert content == {"task_id": task_id, "task_status": "PENDING", "task_result": None}
    assert resp.status_code == 200

    while content["task_status"] == "PENDING":
        resp = client.get(f"tasks/{task_id}")
        content = json.loads(resp.data.decode())
    assert content == {"task_id": task_id, "task_status": "SUCCESS", "task_result": True}
