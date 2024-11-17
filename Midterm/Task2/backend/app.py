from flask import Flask, request, jsonify, abort
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

class Student:
    def __init__(self, id, name, student_id):
        self.id = id
        self.name = name
        self.student_id = student_id

# 使用列表来存储学生对象，并初始化ID
students = []
next_id = 1

def add_example_students():
    global next_id
    examples = [
        {"name": "王一", "student_id": "20240001"},
        {"name": "王二", "student_id": "20240002"},
        {"name": "王三", "student_id": "20240003"}
    ]
    for example in examples:
        new_student = Student(id=next_id, name=example['name'], student_id=example['student_id'])
        students.append(new_student)
        next_id += 1

add_example_students();

@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    global next_id
    if request.method == 'POST':
        data = request.get_json()
        new_student = Student(id=next_id, name=data['name'], student_id=data['student_id'])
        students.append(new_student)
        next_id += 1
        return jsonify({
            "id": new_student.id,
            "name": new_student.name,
            "student_id": new_student.student_id
        }), 201

    if request.method == 'GET':
        query = request.args.get('query')
        if query:
            found_students = [student for student in students if query in (student.name, student.student_id)]
            return jsonify([{
                "id": student.id,
                "name": student.name,
                "student_id": student.student_id
            } for student in found_students])
        return jsonify([{
            "id": student.id,
            "name": student.name,
            "student_id": student.student_id
        } for student in students])

@app.route('/students/<int:student_id>', methods=['GET', 'PUT', 'DELETE'])
def student(student_id):
    student = next((student for student in students if student.id == student_id), None)
    if not student:
        abort(404)

    if request.method == 'GET':
        return jsonify({
            "id": student.id,
            "name": student.name,
            "student_id": student.student_id
        })

    if request.method == 'PUT':
        data = request.get_json()
        student.name = data.get('name', student.name)
        student.student_id = data.get('student_id', student.student_id)
        return jsonify({
            "id": student.id,
            "name": student.name,
            "student_id": student.student_id
        })

    if request.method == 'DELETE':
        students.remove(student)
        return jsonify({'result': 'Student deleted'})

if __name__ == '__main__':
    app.run(debug=True)