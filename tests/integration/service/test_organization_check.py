def test_organization_check(test_client):

    # Create some steps to properly test the script.
    response = test_client.get("/services/")