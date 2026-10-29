
import uuid
from types import SimpleNamespace

import pytest

from app.api.dependency.auth import get_current_user
from main import app


# Generate a unique username for every test
def unique_username():
    return "user_" + uuid.uuid4().hex[:12]


# Generate a unique employee ID
def unique_employee_id():
    return uuid.uuid4().int % 1_000_000_000 + 1


# Reusable admin authentication fixture
@pytest.fixture
def admin_client(client):

    async def fake_admin():
        return SimpleNamespace(
            id=1,
            username="testadmin",
            role="admin"
        )

    app.dependency_overrides[get_current_user] = fake_admin

    try:
        yield client
    finally:
        app.dependency_overrides.pop(
            get_current_user, None
        )


# TEST 1: Register a user
def test_register_user(client):
    username = unique_username()

    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == username
    assert response.json()["role"] == "user"


# TEST 2: Login successfully
def test_login_success(client):
    username = unique_username()
    password = "Test@12345"

    register = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": password
        }
    )
    assert register.status_code == 200

    response = client.post(
        "/api/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


# TEST 3: Incorrect password
def test_login_wrong_password(client):
    username = unique_username()

    register = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": "Correct@123"
        }
    )
    assert register.status_code == 200

    response = client.post(
        "/api/auth/login",
        data={
            "username": username,
            "password": "Wrong@123"
        }
    )

    assert response.status_code == 401


# TEST 4: Get profile with real JWT
def test_get_current_user(client):
    username = unique_username()
    password = "Test@12345"

    register = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": password
        }
    )
    assert register.status_code == 200

    login = client.post(
        "/api/auth/login",
        data={
            "username": username,
            "password": password
        }
    )
    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == username


# TEST 5: No JWT token
def test_without_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


# TEST 6: Admin creates employee
def test_create_employee(admin_client):
    employee_id = unique_employee_id()

    response = admin_client.post(
        "/api/employee_salary/add_employee_deatils",
        json={
            "employee_id": employee_id,
            "employee_name": "Test Employee",
            "gender": "Female",
            "department": "IT"
        }
    )

    assert response.status_code == 200
    assert (
        response.json()["Employee_details"]["employee_id"]
        == employee_id
    )


# TEST 7: Add employee salary
def test_create_employee_salary(admin_client):
    employee_id = unique_employee_id()

    employee = admin_client.post(
        "/api/employee_salary/add_employee_deatils",
        json={
            "employee_id": employee_id,
            "employee_name": "Salary Test",
            "gender": "Male",
            "department": "Finance"
        }
    )
    assert employee.status_code == 200

    response = admin_client.post(
        "/api/employee_salary/add_employee_salary_deatils",
        json={
            "employee_id": employee_id,
            "basic_salary": 20000
        }
    )

    assert response.status_code == 200

    salary = response.json()["Salary_deatiles"]

    assert salary["basic_salary"] == 20000
    assert salary["da"] == 2000
    assert salary["pf"] == 2400
    assert salary["gross_salary"] == 22000


# TEST 8: Get employee
def test_get_employee(admin_client):
    employee_id = unique_employee_id()

    created = admin_client.post(
        "/api/employee_salary/add_employee_deatils",
        json={
            "employee_id": employee_id,
            "employee_name": "Employee Lookup",
            "gender": "Female",
            "department": "HR"
        }
    )
    assert created.status_code == 200

    response = admin_client.get(
        f"/api/employee_salary/{employee_id}"
    )

    assert response.status_code == 200
    assert response.json()["employee_id"] == employee_id
    assert response.json()["employee_name"] == "Employee Lookup"


# TEST 9: Employee not found
def test_employee_not_found(admin_client):
    response = admin_client.get(
        "/api/employee_salary/2147483647"
    )

    assert response.status_code == 404


# TEST 10: Invalid employee ID
def test_invalid_employee_id(admin_client):
    response = admin_client.get(
        "/api/employee_salary/0"
    )

    assert response.status_code == 422


# TEST 11: Invalid salary
@pytest.mark.parametrize(
    "salary",
    [-1000, 0, 5000, 1000000]
)
def test_invalid_salary(admin_client, salary):
    response = admin_client.post(
        "/api/employee_salary/add_employee_salary_deatils",
        json={
            "employee_id": 1,
            "basic_salary": salary
        }
    )

    assert response.status_code == 422


# TEST 12: User cannot create employee
def test_user_cannot_create_employee(client):

    async def fake_user():
        return SimpleNamespace(
            id=2,
            username="normaluser",
            role="user"
        )

    app.dependency_overrides[get_current_user] = fake_user

    try:
        response = client.post(
            "/api/employee_salary/add_employee_deatils",
            json={
                "employee_id": unique_employee_id(),
                "employee_name": "Restricted Test",
                "gender": "Male",
                "department": "IT"
            }
        )

        assert response.status_code == 403

    finally:
        app.dependency_overrides.pop(
            get_current_user, None
        )


# TEST 13: Department totals
def test_department_totals(admin_client):
    response = admin_client.get(
        "/api/employee_salary/"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# TEST 14: Employee report
def test_employee_report(admin_client):
    response = admin_client.get("/api/report/")

    assert response.status_code == 200

    data = response.json()

    assert "total_employee_count" in data
    assert "total_women_employee_count" in data
    assert "total_Men_employee_count" in data
    assert "departments_with_more_than_2_employees" in data
