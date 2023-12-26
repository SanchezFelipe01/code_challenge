from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'departments' 
    __table_args__ = {'schema': 'public'}  
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(255), nullable=True)


class Job(db.Model):
    __tablename__ = 'jobs'  
    __table_args__ = {'schema': 'public'} 

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(255), nullable=True)


class Employee(db.Model):
    __tablename__ = 'hired_employees'  
    __table_args__ = {'schema': 'public'}  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    datetime = db.Column(db.String(255), nullable=True)
    department_id = db.Column(db.Integer, nullable=True)
    job_id = db.Column(db.Integer, nullable=True)