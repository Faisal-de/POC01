from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_key"

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    course = db.Column(db.String(200), nullable=False) # Stores "Python, DevOps"

with app.app_context():
    db.create_all()

# --- AVAILABLE COURSES LIST ---
# You can add more courses here easily
COURSES_LIST = ["Calculus", "Linear Algebra", "Programming Fundamental", "Multivariable Calculus", "English", "Software Engineering", "Data Structures", "Algorithms", "Operating Systems", "Database Systems", "Computer Networks", "Artificial Intelligence", "Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision", "Cybersecurity" ]

# --- ROUTES ---

@app.route('/', methods=['GET'])
def home():
    search_query = request.args.get('search')
    
    if search_query:
        if search_query.isdigit():
            students = Student.query.filter_by(id=int(search_query)).all()
        else:
            students = Student.query.filter(
                (Student.first_name.contains(search_query)) | 
                (Student.last_name.contains(search_query))
            ).all()
    else:
        students = Student.query.all()
        
    # Pass the COURSES_LIST to the HTML so we can show checkboxes
    return render_template('index.html', students=students, courses=COURSES_LIST)

@app.route('/add', methods=['POST'])
def add():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    gender = request.form['gender']
    
    # 🌟 NEW LOGIC: Get list of checked boxes
    selected_courses = request.form.getlist('courses')
    
    # Join them into a string: "DevOps, Python"
    course_string = ", ".join(selected_courses)
    
    if not course_string:
        flash("Please select at least one course!", "danger")
        return redirect('/')

    new_student = Student(
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        phone=phone,
        gender=gender,
        course=course_string
    )
    
    db.session.add(new_student)
    db.session.commit()
    flash("Student Added Successfully!", "success")
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    student = Student.query.get_or_404(id)
    
    if request.method == 'POST':
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.email = request.form['email']
        student.phone = request.form['phone']
        student.gender = request.form['gender']
        
        # Update courses
        selected_courses = request.form.getlist('courses')
        student.course = ", ".join(selected_courses)
        
        db.session.commit()
        flash("Student Updated Successfully!", "warning")
        return redirect('/')
        
    return render_template('update.html', student=student, courses=COURSES_LIST)

@app.route('/delete/<int:id>')
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student Deleted Successfully!", "danger")
    return redirect('/')

if __name__ == "__main__":

    app.run(debug=True)
    print("This is code from Branch 3")
    print("This is code from Branch 2")
    app.run(debug=True)

