import os
from flask import Flask, render_template
from config.db_config import Config
from models.models import db, Department, Job, Employee
from sqlalchemy.sql import text
import pandas as pd

import logic.helpers as helpers


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

current_directory = os.path.dirname(os.path.abspath(__file__))
csv_departments_path = os.path.join(current_directory, '..', 'files', 'departments.csv')
csv_jobs_path  = os.path.join(current_directory, '..', 'files', 'jobs.csv')
csv_employees_path = os.path.join(current_directory, '..', 'files', 'hired_employees.csv')


@app.route('/')
def home():
    return render_template('main_page.html')

### DEPARTMENTS ###

@app.route('/import_departments_csv')
def import_departments_csv():
   return helpers.import_departments_csv(db, Department, csv_departments_path)


@app.route('/get_all_departments')
def get_all_departments():
    return helpers.get_all_departments(Department)
    

@app.route('/delete_all_departments')
def delete_all_departments():
    return helpers.delete_all_departments(db, Department)


### JOBS ###
    
@app.route('/import_jobs_csv')
def import_jobs_csv():
    return helpers.import_jobs_csv(db, Job, csv_jobs_path)


@app.route('/get_all_jobs')
def get_all_jobs():
    return helpers.get_all_jobs(Job)
    
@app.route('/delete_all_jobs')
def delete_all_jobs():
    return helpers.delete_all_jobs(db, Job)


### EMPLOYEES ###
    
@app.route('/import_employees_csv')
def import_employees_csv():
    return helpers.import_employees_csv(db, Employee, csv_employees_path)

@app.route('/get_all_employees')
def get_all_employees():
    return helpers.get_all_employees(Employee)

@app.route('/delete_all_employees')
def delete_all_employees():
    return helpers.delete_all_employees(db, Employee)


# Ruta de Flask para mostrar empleados con condiciones complejas
@app.route('/recruitments')
def get_quarterly_recruitments():
    return helpers.recruitments_by_quarter(db, Department, Job, Employee)

    

@app.route('/people_by_departments')
def get_people_by_departments():
    return helpers.people_by_department(db, Department, Employee)


if __name__ == '__main__':
    app.run(debug=True)
