from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Student, Attendance, Grade, User
from datetime import datetime, timedelta
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Sample data population function
def populate_sample_data():
    if Student.query.count() > 0:
        return

    students_data = [
        {"name": "Aarav Sharma", "email": "aarav.sharma@example.com", "student_id": "STU001"},
        {"name": "Priya Patel", "email": "priya.patel@example.com", "student_id": "STU002"},
        {"name": "Rohan Gupta", "email": "rohan.gupta@example.com", "student_id": "STU003"},
        {"name": "Sneha Reddy", "email": "sneha.reddy@example.com", "student_id": "STU004"},
        {"name": "Vikram Singh", "email": "vikram.singh@example.com", "student_id": "STU005"},
        {"name": "Ananya Desai", "email": "ananya.desai@example.com", "student_id": "STU006"},
        {"name": "Kiran Malhotra", "email": "kiran.malhotra@example.com", "student_id": "STU007"},
        {"name": "Aditya Rao", "email": "aditya.rao@example.com", "student_id": "STU008"},
        {"name": "Meera Kapoor", "email": "meera.kapoor@example.com", "student_id": "STU009"},
        {"name": "Siddharth Nair", "email": "siddharth.nair@example.com", "student_id": "STU010"},
        {"name": "Isha Verma", "email": "isha.verma@example.com", "student_id": "STU011"},
        {"name": "Arjun Mehra", "email": "arjun.mehra@example.com", "student_id": "STU012"},
        {"name": "Nisha Bhatia", "email": "nisha.bhatia@example.com", "student_id": "STU013"},
        {"name": "Rahul Khanna", "email": "rahul.khanna@example.com", "student_id": "STU014"},
        {"name": "Tanvi Joshi", "email": "tanvi.joshi@example.com", "student_id": "STU015"},
        {"name": "Yash Thakur", "email": "yash.thakur@example.com", "student_id": "STU016"},
        {"name": "Pooja Menon", "email": "pooja.menon@example.com", "student_id": "STU017"},
        {"name": "Dev Chauhan", "email": "dev.chauhan@example.com", "student_id": "STU018"},
        {"name": "Riya Saxena", "email": "riya.saxena@example.com", "student_id": "STU019"},
        {"name": "Kabir Gill", "email": "kabir.gill@example.com", "student_id": "STU020"},
    ]

    for student_info in students_data:
        student = Student(
            name=student_info["name"],
            email=student_info["email"],
            student_id=student_info["student_id"]
        )
        db.session.add(student)
    db.session.commit()

    statuses = ["Present", "Absent"]
    students = Student.query.all()
    start_date = datetime.strptime("2025-05-15", "%Y-%m-%d")
    for student in students:
        for day in range(10):
            date = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
            status = random.choice(statuses)
            attendance = Attendance(
                student_id=student.id,
                date=date,
                status=status
            )
            db.session.add(attendance)
    db.session.commit()

    subjects = ["Mathematics", "Science", "English", "History", "Computer Science", "Geography", "Physics", "Chemistry"]
    grades = ["A", "B", "C", "D", "F"]
    for student in students:
        student_subjects = random.sample(subjects, 5)
        for subject in student_subjects:
            grade = random.choice(grades)
            grade_entry = Grade(
                student_id=student.id,
                subject=subject,
                grade=grade
            )
            db.session.add(grade_entry)
    db.session.commit()

# Create database tables and populate sample data
with app.app_context():
    db.create_all()
    populate_sample_data()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        student_id = request.form['student_id']
        student = Student(name=name, email=email, student_id=student_id)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully', 'success')
        return redirect(url_for('manage_students'))
    
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.student_id = request.form['student_id']
        db.session.commit()
        flash('Student updated successfully', 'success')
        return redirect(url_for('manage_students'))
    
    return render_template('edit_student.html', student=student)

@app.route('/students/delete/<int:id>')
def delete_student(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully', 'success')
    return redirect(url_for('manage_students'))

@app.route('/attendance', methods=['GET', 'POST'])
def manage_attendance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        date = request.form['date']
        status = request.form['status']
        attendance = Attendance(student_id=student_id, date=date, status=status)
        db.session.add(attendance)
        db.session.commit()
        flash('Attendance recorded', 'success')
        return redirect(url_for('manage_attendance'))
    
    students = Student.query.all()
    attendances = Attendance.query.all()
    return render_template('attendance.html', students=students, attendances=attendances)

@app.route('/grades', methods=['GET', 'POST'])
def manage_grades():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        subject = request.form['subject']
        grade = request.form['grade']
        grade_entry = Grade(student_id=student_id, subject=subject, grade=grade)
        db.session.add(grade_entry)
        db.session.commit()
        flash('Grade recorded', 'success')
        return redirect(url_for('manage_grades'))
    
    students = Student.query.all()
    grades = Grade.query.all()
    return render_template('grades.html', students=students, grades=grades)

if __name__ == '__main__':
    app.run(debug=True)