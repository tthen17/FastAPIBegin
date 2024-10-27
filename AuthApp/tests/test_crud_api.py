def test_register(test_client, user_payload):
    response = test_client.post("/register", json=user_payload)
    assert response.status_code == 200
    assert response.json() == {"message": "user created successfully"}
    

def test_login(test_client, user_payload_login):
    response = test_client.post("/login", json=user_payload_login)
    assert response.status_code == 200

def test_change_password(test_client, user_payload_updated):
    response = test_client.post("/changepassword", json=user_payload_updated)
    assert response.status_code == 200
    assert response.json() == {"message": "Password changed successfully"}

def test_get_users(test_client):
    response = test_client.get("/getusers")
    assert response.status_code == 200