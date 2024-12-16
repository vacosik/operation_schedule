from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
db = SQLAlchemy(app)

# Модель бази даних
class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    operating_room = db.Column(db.String(10), nullable=False)
    operation_name = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    surgeon = db.Column(db.String(50), nullable=False)
    anesthesiologist = db.Column(db.String(50), nullable=False)
    first_assistant = db.Column(db.String(50))
    second_assistant = db.Column(db.String(50))

# Ініціалізація бази даних
with app.app_context():
    db.create_all()

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# API для отримання операцій
@app.route('/api/operations', methods=['GET'])
def get_operations():
    operations = Operation.query.all()
    return jsonify([
        {
            'id': op.id,
            'date': op.date,
            'time': op.time,
            'operating_room': op.operating_room,
            'operation_name': op.operation_name,
            'priority': op.priority,
            'surgeon': op.surgeon,
            'anesthesiologist': op.anesthesiologist,
            'first_assistant': op.first_assistant,
            'second_assistant': op.second_assistant
        } for op in operations
    ])

# API для додавання операції
@app.route('/api/operations', methods=['POST'])
def add_operation():
    data = request.get_json()
    new_operation = Operation(
        date=data['date'],
        time=data['time'],
        operating_room=data['operating_room'],
        operation_name=data['operation_name'],
        priority=data['priority'],
        surgeon=data['surgeon'],
        anesthesiologist=data['anesthesiologist'],
        first_assistant=data['first_assistant'],
        second_assistant=data['second_assistant']
    )
    db.session.add(new_operation)
    db.session.commit()
    return jsonify({'message': 'Operation added successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
