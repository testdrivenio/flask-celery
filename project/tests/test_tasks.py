def test_home(test_app):
    client = test_app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
