import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, todos

def setup_function():
    todos.clear()

def test_add_todo():
    client = app.test_client()
    res = client.post("/api/todos", json={"title": "寫作業"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "寫作業"
    assert data["done"] == False

def test_add_empty_todo():
    client = app.test_client()
    res = client.post("/api/todos", json={"title": ""})
    assert res.status_code == 400

def test_mark_done():
    client = app.test_client()
    res = client.post("/api/todos", json={"title": "買東西"})
    todo_id = res.get_json()["id"]
    res = client.put(f"/api/todos/{todo_id}/done")
    assert res.status_code == 200
    assert res.get_json()["done"] == True

def test_delete_todo():
    client = app.test_client()
    res = client.post("/api/todos", json={"title": "掃地"})
    todo_id = res.get_json()["id"]
    res = client.delete(f"/api/todos/{todo_id}")
    assert res.status_code == 200
    res2 = client.get("/api/todos")
    assert len(res2.get_json()) == 0