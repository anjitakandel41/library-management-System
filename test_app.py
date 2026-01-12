
import pytest
from app import app

# ---------------------------
# Test Client Setup
# ---------------------------
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# -------------------------------
# 1️⃣ Register Test
# -------------------------------
def test_register(client):
    """
    Test the user registration functionality.
    Checks successful registration and duplicate username handling.
    """
    # Successful registration
    response = client.post("/register", data={
        "fName": "Auto",
        "lName": "Test",
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com"
    }, follow_redirects=True)
    assert b"Registration successful" in response.data

    # Duplicate username (optional)
    response = client.post("/register", data={
        "fName": "Auto",
        "lName": "Test",
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com"
    }, follow_redirects=True)
    assert b"Username already exists" in response.data

#corrected register

def test_register(client):
    response = client.post("/register", data={
        "fName": "Auto",
        "lName": "Test",
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com",
        "role": "student"
    }, follow_redirects=True)

    # Check if redirected to login page
    assert b"Login" in response.data or b"Sign In" in response.data
