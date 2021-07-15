def test_main(test_client):
    # Swagger docs are available.
    response = test_client.get("/docs")
    assert response.status_code == 200
