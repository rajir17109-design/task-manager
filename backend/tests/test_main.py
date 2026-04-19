import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Use separate test database (won't touch your real data)
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Override the database with test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables in test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# ========================
# TEST 1: Register User
# ========================
def test_register_user():
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    print("✅ Register test passed!")

# ========================
# TEST 2: Register Same Username Again
# ========================
def test_register_duplicate_username():
    # First registration
    client.post("/register", json={
        "username": "duplicateuser",
        "email": "dup@example.com",
        "password": "testpass123"
    })
    # Try same username again
    response = client.post("/register", json={
        "username": "duplicateuser",
        "email": "dup2@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]
    print("✅ Duplicate username test passed!")

# ========================
# TEST 3: Login Success
# ========================
def test_login_success():
    # Register first
    client.post("/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "mypassword"
    })
    # Now login
    response = client.post("/login", json={
        "username": "loginuser",
        "password": "mypassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    print("✅ Login success test passed!")

# ========================
# TEST 4: Login Wrong Password
# ========================
def test_login_wrong_password():
    client.post("/register", json={
        "username": "wrongpassuser",
        "email": "wrong@example.com",
        "password": "correctpassword"
    })
    response = client.post("/login", json={
        "username": "wrongpassuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]
    print("✅ Wrong password test passed!")

# ========================
# Helper: Get auth token
# ========================
def get_token(username="taskuser", email="task@example.com", password="pass123"):
    client.post("/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    response = client.post("/login", json={
        "username": username,
        "password": password
    })
    return response.json()["access_token"]

# ========================
# TEST 5: Create Task
# ========================
def test_create_task():
    token = get_token("createtaskuser", "createtask@example.com")
    response = client.post("/tasks",
        json={"title": "My First Task", "description": "Test description"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "My First Task"
    assert data["completed"] == False
    print("✅ Create task test passed!")

# ========================
# TEST 6: Get All Tasks
# ========================
def test_get_tasks():
    token = get_token("gettaskuser", "gettask@example.com")
    # Create a task first
    client.post("/tasks",
        json={"title": "Task to Get"},
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get("/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert data["total"] >= 1
    print("✅ Get tasks test passed!")

# ========================
# TEST 7: Mark Task Complete
# ========================
def test_mark_task_complete():
    token = get_token("completeuser", "complete@example.com")
    # Create task
    create_res = client.post("/tasks",
        json={"title": "Task to Complete"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_res.json()["id"]

    # Mark as complete
    response = client.put(f"/tasks/{task_id}",
        json={"completed": True},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["completed"] == True
    print("✅ Mark complete test passed!")

# ========================
# TEST 8: Delete Task
# ========================
def test_delete_task():
    token = get_token("deleteuser", "delete@example.com")
    # Create task
    create_res = client.post("/tasks",
        json={"title": "Task to Delete"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_res.json()["id"]

    # Delete it
    response = client.delete(f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]
    print("✅ Delete task test passed!")

# ========================
# TEST 9: Access Without Token
# ========================
def test_access_without_token():
    response = client.get("/tasks")
    assert response.status_code == 401
    print("✅ No token test passed!")

# Cleanup test database after all tests
def teardown_module(module):
    Base.metadata.drop_all(bind=engine)
    engine.dispose()  # Close all connections first
    import time
    time.sleep(0.5)  # Wait for Windows to release the file
    if os.path.exists("./test.db"):
        try:
            os.remove("./test.db")
        except PermissionError:
            pass  # Ignore if still locked
    print("🧹 Test database cleaned up!")