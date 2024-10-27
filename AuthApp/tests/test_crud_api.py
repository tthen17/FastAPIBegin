def test_register(test_client, user_payload):
    response = test_client.post("/register", json=user_payload)
    assert response.status_code == 200
    assert response.json() == {"message": "user created successfully"}

# def test_login(test_client, user_payload):
#     response = test_client.get("/login")
#     assert response.status_code == 200