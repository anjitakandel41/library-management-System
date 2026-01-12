<<<<<<< HEAD
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

# ---------------------------
# UNIT TEST: REGISTER
# ---------------------------
def test_register(client):
    response = client.post(
        "/register",
        data={
            "fName": "Auto",
            "lName": "Tester",
            "email": "unit@test.com",
            "password": "12345",
            "role": "student"
        },
        follow_redirects=True   # IMPORTANT
    )

    # ✅ EXPECTED OUTPUT
    assert response.status_code == 200
    assert b"Login" in response.data   # page shown after register


=======
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

# ---------------------------
# UNIT TEST: REGISTER
# ---------------------------
def test_register(client):
    response = client.post(
        "/register",
        data={
            "fName": "Auto",
            "lName": "Tester",
            "email": "unit@test.com",
            "password": "12345",
            "role": "student"
        },
        follow_redirects=True   # IMPORTANT
    )

    # ✅ EXPECTED OUTPUT
    assert response.status_code == 200
    assert b"Login" in response.data   # page shown after register


>>>>>>> 16aa79e (Add static folder with CSS and JS)
