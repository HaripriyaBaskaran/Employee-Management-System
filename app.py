from flask import Flask, render_template, request, redirect, url_for
from employee import db, Employee

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    department = request.form['department']
    new_employee = Employee(name, department)
    db.session.add(new_employee)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<int:id>', methods=['POST'])
def update_employee(id):
    employee = Employee.query.get(id)
    employee.name = request.form['name']
    employee.department = request.form['department']
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
