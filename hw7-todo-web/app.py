from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 記憶體存資料，不用資料庫
todos = []
next_id = 1

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/api/todos", methods=["POST"])
def add_todo():
    global next_id
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "標題不能是空的"}), 400
    todo = {"id": next_id, "title": title, "done": False}
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201

@app.route("/api/todos/<int:todo_id>/done", methods=["PUT"])
def mark_done(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            return jsonify(todo)
    return jsonify({"error": "找不到這個待辦"}), 404

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    for todo in todos:
        if todo["id"] == todo_id:
            todos = [t for t in todos if t["id"] != todo_id]
            return jsonify({"message": "已刪除"})
    return jsonify({"error": "找不到這個待辦"}), 404

if __name__ == "__main__":
    app.run(debug=True)