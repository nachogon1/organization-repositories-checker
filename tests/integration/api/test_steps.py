def test_steps_lifecycle(test_client):

    mock_step = {
        "command": "foobar"
    }

    # Create step.
    response = test_client.post("/api/steps", json=mock_step)
    assert response.status_code == 200
    result = response.json()
    assert result["command"] == "foobar"

    # Get the step.
    response = test_client.get(f"/api/steps/{result['_id']}")
    assert response.status_code == 200
    result = response.json()
    assert result["command"] == "foobar"

    # Get all steps.
    response = test_client.get(f"/api/steps")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1

    new_step = result.copy()
    new_step["command"] = "test_edit"
    # Edit the step.
    response = test_client.put(f"/api/steps?step-id={result['_id']}", json=new_step)
    assert response.status_code == 200
    assert response.json()["command"] == "test_edit"

    # Check that the step was updated in the db.
    response = test_client.get(f"/api/steps/{result['_id']}")
    assert response.status_code == 200
    result = response.json()
    assert result["command"] == "test_edit"

    # Delete the step
    response = test_client.delete(f"/api/steps/{result['_id']}")
    assert response.status_code == 200
    result = response.json()
    assert result["command"] == "test_edit"

    # Check that the steps were deleted.
    response = test_client.get(f"/api/steps")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 0
