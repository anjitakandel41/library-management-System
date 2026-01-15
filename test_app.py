
import pytest
from app import app
import json
import os

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------- STUDENT REGISTRATION TEST ----------
def test_student_registration(client):
    response = client.post("/register", data={
        "fName": "Test",
        "lName": "Student",
        "email": "student_test@gmail.com",
        "password": "Test@123",
        "role": "student"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Registered successfully" in response.data


def test_duplicate_student_registration(client):
    client.post("/register", data={
        "fName": "Test",
        "lName": "Student",
        "email": "dup@gmail.com",
        "password": "Test@123",
        "role": "student"
    })

    response = client.post("/register", data={
        "fName": "Test",
        "lName": "Student",
        "email": "dup@gmail.com",
        "password": "Test@123",
        "role": "student"
    }, follow_redirects=True)

    assert b"User already exists" in response.data


def test_student_registration_empty_fields(client):
    response = client.post("/register", data={
        "fName": "",
        "lName": "",
        "email": "",
        "password": "",
        "role": "student"
    }, follow_redirects=True)

    assert response.status_code == 200


def test_student_registration_invalid_email(client):
    response = client.post("/register", data={
        "fName": "Invalid",
        "lName": "Email",
        "email": "invalidemail.com",
        "password": "Test@123",
        "role": "student"
    }, follow_redirects=True)

    assert response.status_code == 200


def test_student_registration_without_role(client):
    response = client.post("/register", data={
        "fName": "Default",
        "lName": "Student",
        "email": "defaultrole@gmail.com",
        "password": "Test@123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Registered successfully" in response.data


def test_student_registration_empty_password(client):
    response = client.post("/register", data={
        "fName": "No",
        "lName": "Password",
        "email": "nopassword@gmail.com",
        "password": "",
        "role": "student"
    }, follow_redirects=True)

    assert response.status_code == 200
