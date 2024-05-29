from flask import Blueprint, request, jsonify, abort
from models import db, Task
from schemas import TaskSchema

task_bp = Blueprint('task_bp', __name__)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@task_bp.route('/tasks', methods=['POST'])
def add_task():
    title = request.json.get('title')
    description = request.json.get('description')
    if not title:
        abort(400, description="Title is required")

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    
    return task_schema.jsonify(new_task), 201

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return tasks_schema.jsonify(tasks), 200

@task_bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return task_schema.jsonify(task), 200

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    title = request.json.get('title')
    description = request.json.get('description')

    if title:
        task.title = title
    if description:
        task.description = description

    db.session.commit()
    return task_schema.jsonify(task), 200

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
