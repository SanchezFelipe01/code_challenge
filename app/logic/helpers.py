import pandas as pd
from sqlalchemy import inspect
import csv
from flask import render_template, jsonify
from sqlalchemy.sql import or_


### CRUD Operations ###

# DEPARTMENTS

def import_departments_csv(db, Department, csv_departments_path: str):
    
    message = ""

    try:
        inspector = inspect(db.engine)

        if not inspector.has_table(Department.__table__.name):
            db.create_all()

        with open(csv_departments_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

            for row in data:
                id_value = int(row[0]) if row[0] else None
                if not record_exists_by_id(db.session, Department, id_value):
                    department_name = row[1] if row[1] else None 

                    department = Department(
                        id=id_value, 
                        department=department_name
                    )

                    db.session.add(department)
            db.session.commit()

        message = "Records successfully imported."

    except Exception as e:
        db.session.rollback()
        message = f"Error while importing the records: {str(e)}"

    return jsonify({"message": message})
    
def get_all_departments(Department):
    try:
        departments = Department.query.all()
        return render_template('departments.html', departments=departments)
    except Exception as e:
        return f"""Error while getting the records: {str(e)}
                    <p><a href="/">Go to Main Page</a></p>
                """
                
    
def delete_all_departments(db, Department):

    message = ""

    try:
        db.session.query(Department).delete()
        db.session.commit()
        message = "All records from departments table have been deleted."
        
    except Exception as e:
        message = f"Error while deleting the records: {str(e)}"
    
    return jsonify({"message": message})

# DEPARTMENTS
    

# JOBS
    
def import_jobs_csv(db, Job, csv_jobs_path):
    
    message = ""
    
    try:
        inspector = inspect(db.engine)

        if not inspector.has_table(Job.__table__.name):
            db.create_all()

        with open(csv_jobs_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

            for row in data:
                id_value = int(row[0]) if row[0] else None
                if not record_exists_by_id(db.session, Job, id_value):
                    job_name = row[1] if row[1] else None

                    job = Job(
                        id=id_value, 
                        job=job_name
                    )

                    db.session.add(job)
            db.session.commit()

        message = "Records successfully imported."
               

    except Exception as e:
        db.session.rollback()
        message = f"Error while importing the records: {str(e)}"
    
    return jsonify({"message": message})
    

def get_all_jobs(Job):
    try:
        jobs = Job.query.all()
        
        return render_template('jobs.html', jobs=jobs)
    except Exception as e:
        return f"""Error while getting the records: {str(e)}
                 <p><a href="/">Go to Main Page</a></p>
                 """
    
def delete_all_jobs(db, Job):
    
    message = ""
    
    try:
        db.session.query(Job).delete()
        db.session.commit()
        message = "All records from jobs table have been deleted."

    except Exception as e:
        message = f"Error while deleting the records: {str(e)}"
    
    return jsonify({"message": message})

# JOBS
    

# EMPLOYEES

def import_employees_csv(db, Employee, csv_employees_path):
    
    message = ""

    try:
        inspector = inspect(db.engine)

        if not inspector.has_table(Employee.__table__.name):
            db.create_all()

        with open(csv_employees_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

            for row in data:
                id_value = int(row[0]) if row[0] else None  
                
                if not record_exists_by_id(db.session, Employee, id_value):
                    name_value = row[1] if row[1] else None  
                    datetime_value = row[2] if row[2] else None 
                    department_value = int(row[3]) if row[3] else None  
                    job_value = int(row[4]) if row[4] else None

                    employee = Employee(
                        id=id_value, 
                        name=name_value, 
                        datetime=datetime_value, 
                        department_id=department_value, 
                        job_id=job_value
                    )

                    db.session.add(employee)

                db.session.commit()

        message = "Records successfully imported."

    except Exception as e:
        db.session.rollback()
        message = f"Error while importing the records: {str(e)}"
    
    return jsonify({"message": message})
    
def get_all_employees(Employee):
    try:
        employees = Employee.query.all()
        return render_template('employees.html', employees=employees, title='Hired employees')
    except Exception as e:
        return f"""Error while getting the records: {str(e)}
                     <p><a href="/">Go to Main Page</a></p>
                """

def get_employees_with_missing_info(Employee):
    try:
        employees = Employee.query.filter(
            or_(
                Employee.name.is_(None),
                Employee.datetime.is_(None),
                Employee.department_id.is_(None),
                Employee.job_id.is_(None),
            )
        ).all()
        return render_template('employees.html', employees=employees, title='Employees with missing information')
    except Exception as e:
        return f"""Error while getting the records: {str(e)}
                     <p><a href="/">Go to Main Page</a></p>
                """


def delete_all_employees(db, Employee):
    
    message = ""
    
    try:
        db.session.query(Employee).delete()
        db.session.commit()
        message = "All records from employees table have been deleted."

    except Exception as e:
        message = f"Error while deleting the records: {str(e)}"
    
    return jsonify({"message": message})
    
# EMPLOYEES   

### CRUD Operations ###


### QUERIES ###

# REQUIREMENT 1
    
def recruitments_by_quarter(db, Department, Job, Employee):

    columns = ['department', 'job', 'Q1', 'Q2', 'Q3', 'Q4']
    df = pd.DataFrame(columns=columns)

    try:
        departments = pd.read_sql_table(Department.__tablename__, db.engine)
        jobs = pd.read_sql_table(Job.__tablename__, db.engine)
        hired_employees = pd.read_sql_table(Employee.__tablename__, db.engine)

        if hired_employees.empty or departments.empty or jobs.empty:
            return render_template('result.html', result=df, title='Recruitments per quarter')

        hired_employees['datetime'] = pd.to_datetime(hired_employees['datetime'])
        hired_employees_2021 = hired_employees[hired_employees['datetime'].dt.year == 2021]

        hired_employees_2021['quarter'] = hired_employees_2021['datetime'].dt.quarter

        merged_df = pd.merge(
            hired_employees_2021, 
            departments, 
            left_on='department_id', 
            right_on='id'
        )
        
        merged_df = pd.merge(
            merged_df, 
            jobs, 
            left_on='job_id', 
            right_on='id'
        )
        
        result_df = (
            merged_df.groupby(['department', 'job', 'quarter'])
                .size().unstack(fill_value=0).reset_index()
        )

        result_df.columns = ['department', 'job', 'Q1', 'Q2', 'Q3', 'Q4']

        result_df = (
            result_df.sort_values(by=['department', 'job'])
                .reset_index(drop=True)
        )

        result_df.index = result_df.index +1
        return render_template('result.html', result=result_df, title='Recruitments per quarter')
    except Exception:
        df.loc[0] = 'Error'
        return render_template('result.html', result=df, title='Recruitments per quarter')

# REQUIREMENT 1

# REQUIREMENT 2

def people_by_department(db, Department, Employee):

    columns = ['id', 'department', 'hired']
    df = pd.DataFrame(columns=columns)

    try:

        departments = pd.read_sql_table(Department.__tablename__, db.engine)
        hired_employees = pd.read_sql_table(Employee.__tablename__, db.engine)

        if hired_employees.empty or departments.empty:
            columns = ['id', 'department', 'hired']
            df = pd.DataFrame(columns=columns)
            return render_template('result.html', result=df, title='People by department')

        hired_employees['datetime'] = pd.to_datetime(hired_employees['datetime'])
        hired_employees_2021 = hired_employees[hired_employees['datetime'].dt.year == 2021]

        merged_df = pd.merge(
            hired_employees_2021, 
            departments, 
            left_on='department_id', 
            right_on='id')

        merge2 = (
            merged_df.groupby(['id_y', 'department'])
                .size().reset_index(name='hired')
        )
        
        avg_num_employees_hired = merge2['hired'].mean()

        people_by_department_df = merge2[merge2['hired'] > avg_num_employees_hired]

        people_by_department_df = (
            people_by_department_df.sort_values(by='hired', ascending=False)
                .reset_index(drop=True)
        )

        people_by_department_df.rename(columns={'id_y': 'id'}, inplace=True)
        people_by_department_df.index = people_by_department_df.index +1
        return render_template('result.html', result=people_by_department_df, title='People by department')

    except Exception:
        df.loc[0] = 'Error'
        return render_template('result.html', result=df, title='People by department')

# REQUIREMENT 2

def people_with_missing_data(db, Employee):

    columns = ['id', 'department', 'datetime']
    df = pd.DataFrame(columns=columns)

    try:

        departments = pd.read_sql_table(Department.__tablename__, db.engine)
        hired_employees = pd.read_sql_table(Employee.__tablename__, db.engine)

        if hired_employees.empty or departments.empty:
            columns = ['id', 'department', 'hired']
            df = pd.DataFrame(columns=columns)
            return render_template('result.html', result=df, title='People by department')

        hired_employees['datetime'] = pd.to_datetime(hired_employees['datetime'])
        hired_employees_2021 = hired_employees[hired_employees['datetime'].dt.year == 2021]

        merged_df = pd.merge(
            hired_employees_2021, 
            departments, 
            left_on='department_id', 
            right_on='id')

        merge2 = (
            merged_df.groupby(['id_y', 'department'])
                .size().reset_index(name='hired')
        )
        
        avg_num_employees_hired = merge2['hired'].mean()

        people_by_department_df = merge2[merge2['hired'] > avg_num_employees_hired]

        people_by_department_df = (
            people_by_department_df.sort_values(by='hired', ascending=False)
                .reset_index(drop=True)
        )

        people_by_department_df.rename(columns={'id_y': 'id'}, inplace=True)
        people_by_department_df.index = people_by_department_df.index +1
        return render_template('result.html', result=people_by_department_df, title='People by department')

    except Exception:
        df.loc[0] = 'Error'
        return render_template('result.html', result=df, title='People by department')

### QUERIES ###


### AUX FUNCTIONS ###

def record_exists_by_id(session, model, record_id):
    table_model = session.get(model, record_id)
    return table_model is not None

### AUX FUNCTIONS ###
