import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, todos

def setup_function():
    todos.clear()

def test_full_flow():
    client = app.test_client()

    res = client.get("/api/todos")
    assert res.status_code == 200
    assert res.get_json() == []

    r1 = client.post("/api/todos", json={"title": "早餐"})
    r2 = client.post("/api/todos", json={"title": "寫報告"})
    r3 = client.post("/api/todos", json={"title": "運動"})
    id1 = r1.get_json()["id"]
    id2 = r2.get_json()["id"]

    res = client.get("/api/todos")
    assert len(res.get_json()) == 3

    client.put(f"/api/todos/{id2}/done")
    res = client.get("/api/todos")
    todos_list = res.get_json()
    assert todos_list[1]["done"] == True
    assert todos_list[0]["done"] == False

    client.delete(f"/api/todos/{id1}")
    res = client.get("/api/todos")
    assert len(res.get_json()) == 2
