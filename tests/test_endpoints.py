from types import SimpleNamespace

from main import app
from app.api.dependency.auth import get_current_user


# Test 1: Missing JWT
def test_me_without_token(client):

    response = client.get("/api/auth/me")

    assert response.status_code == 401


# Test 2: Invalid JWT
def test_me_invalid_token(client):

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code == 401


# Test 3: Invalid registration input This test focuses on Pydantic validation.
def test_register_invalid_data(client):

    response = client.post(
        "/api/auth/register",
        json={
            "username": "ab",
            "password": "123"
        }
    )

    assert response.status_code == 422 #Unprocessable Entity


# Test 4: Admin-only employee creation
def test_user_cannot_add_employee(client):

    async def fake_user():
        #SimpleNamespace creates an object with attributes
        return SimpleNamespace(
            id=1,
            username="testuser",
            role="user"
        )

    app.dependency_overrides[get_current_user] = fake_user

    try:
        response = client.post(
            "/api/employee_salary/add_employee_deatils",
            json={}
        )

        assert response.status_code == 403

    finally:
        app.dependency_overrides.pop(
            get_current_user,
            None
        )


# Test 5: Admin-only salary increment
def test_user_cannot_increment_salary(client):

    async def fake_user():
        return SimpleNamespace(
            id=1,
            username="testuser",
            role="user"
        )

    app.dependency_overrides[get_current_user] = fake_user

    try:
        response = client.post(
            "/api/employee_salary/1/increment",
            json={"percent": 10}
        )

        assert response.status_code == 403

    finally:
        app.dependency_overrides.pop(
            get_current_user,
            None
        )


# Test 6: Missing token for reports
def test_report_without_token(client):

    response = client.get("/api/report/")
 
    assert response.status_code == 401