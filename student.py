from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)

courses = [
    {
        "id": 1,
        "name": "KPO",
        "teacher": "Anton Kalinin",
        "description": "very good",
        "price": 600
    },
    {
        "id": 2,
        "name": "Python",
        "teacher": "Peter",
        "description": "nice",
        "price": 100
    }
]

# Пример данных о записях на курсы
enrollments = [
    {
        "id": 1,
        "course_id": 1,
        "student_id": 1
    },
    {
        "id": 2,
        "course_id": 2,
        "student_id": 2
    },
    {
        "id": 3,
        "course_id": 1,
        "student_id": 2
    }
]

# Получение списка всех курсов
@app.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(courses)

# Получение информации о конкретном курсе
@app.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = next((course for course in courses if course['id'] == id), None)
    if course:
        return jsonify(course)
    else:
        return jsonify({'error': 'not found'})

# Запись на курс
@app.route('/enrollments', methods=['POST'])
def enroll():
    course_id = request.json.get('course_id')
    student_id = request.json.get('student_id')
    if not course_id or not student_id:
        return jsonify({'error': 'not found'})
    enrollment = {
        'id': len(enrollments) + 1,
        'course_id': course_id,
        'student_id': student_id
    }
    enrollments.append(enrollment)
    return jsonify(enrollment)

# Получение списка курсов, на которые записан студент
@app.route('/enrollments/<int:student_id>', methods=['GET'])
def get_enrollments(student_id):
    student_enrollments = [enrollment for enrollment in enrollments if enrollment['student_id'] == student_id]
    if student_enrollments:
        student_courses = [next((course for course in courses if course['id'] == enrollment['course_id']), None) for enrollment in student_enrollments]
        return jsonify(student_courses)
    else:
        return jsonify({'error': 'not found courses'})

# Отмена записи на курс
@app.route('/enrollments/<int:enrollment_id>', methods=['DELETE'])
def cancel_enrollment(enrollment_id):
    enrollment = next((enrollment for enrollment in enrollments if enrollment['id'] == enrollment_id), None)
    if enrollment:
        enrollments.remove(enrollment)
        return jsonify({'message': 'delete'})
    else:
        return jsonify({'error': 'not found this courses'})

if __name__ == '__main__':
    app.run(debug=True)
