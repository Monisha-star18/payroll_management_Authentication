
import jwt
import pytest

from app.core import security
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "TestPassword@123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_incorrect_password():
    hashed = hash_password("Correct@123")

    assert verify_password("Wrong@123", hashed) is False


def test_create_jwt_token():
    token = create_access_token(
        username="testuser",
        role="user"
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "testuser"
    assert payload["role"] == "user"
    assert "exp" in payload


def test_invalid_jwt_token():
    with pytest.raises(jwt.PyJWTError):
        decode_access_token("invalid.jwt.token")


def test_expired_jwt_token(monkeypatch):
    
    #monkeypatch is a built-in Pytest fixture used to temporarily change values during testing.
    monkeypatch.setattr(security, "EXPIRE_MINUTES", -1)

    token = security.create_access_token(
        username="testuser",
        role="user"
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        security.decode_access_token(token) #decoding the expired token raises ExpiredSignatureError
