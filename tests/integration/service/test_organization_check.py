def test_organization_check(test_client, httpserver):

    # Create some steps to properly test the script.
    mock_step = {"command": "foobar"}
    response = test_client.post("/api/steps", json=mock_step)
    assert response.status_code == 200

    mock_step = {"command": "yara_step"}
    # Create step.
    response = test_client.post("/api/steps", json=mock_step)
    assert response.status_code == 200

    fake_url_1 = {
        "download_url": f"http://"
        f"{httpserver.host}:{httpserver.port}/fake_url_1"
    }
    fake_url_2 = {
        "download_url": f"http://"
        f"{httpserver.host}:{httpserver.port}/fake_url_2"
    }
    fake_config_1 = """jobs:
        fake_config_1_job_1:
            steps:
              -  checkout
    """
    fake_config_2 = """jobs:
        fake_config_2_job_2:
            foo:
              -  bar
    """
    fake_github_organization = [
        {"name": "fake_repo_1"},
        {"name": "fake_repo_2"},
    ]
    fake_org_name = "foobar"
    fake_github_token = "foobar"

    httpserver.expect_request("/orgs/foobar/repos").respond_with_json(
        fake_github_organization
    )

    httpserver.expect_request(
        f"/repos/{fake_org_name}/fake_repo_1/contents/.circleci/config.yml"
    ).respond_with_json(fake_url_1)

    httpserver.expect_request(
        f"/repos/{fake_org_name}/fake_repo_2/contents/.circleci/config.yml"
    ).respond_with_json(fake_url_2)

    httpserver.expect_request("/fake_url_1").respond_with_data(fake_config_1)

    httpserver.expect_request("/fake_url_2").respond_with_data(fake_config_2)

    # Test organization repositories steps.
    response = test_client.get(
        f"/service/steps/organization-check?"
        f"organization-name={fake_org_name}&github-token={fake_github_token}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "fake_repo_1": {"fake_config_1_job_1": ["foobar", "yara_step"]},
        "fake_repo_2": {"fake_config_2_job_2": ["foobar", "yara_step"]},
    }
