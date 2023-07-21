# Django API for Patient and Doctor Records

This project is a Django RESTful API that manages patient and doctor records in different departments. The API allows doctors to associate patients with respective departments and manage patient records. Patients can access their own records, while doctors can access their patients' records within the same department.

## Features

Two user groups: Patients and Doctors 

Models: Patient, Doctor, Department, and PatientRecord

Token-based authentication using Django Knox

Endpoints for CRUD operations on Patients, Doctors, Departments, and Patient Records

Only authorized users can access relevant endpoints based on their roles and associations

## Installation
Clone the repository:

git clone https://github.com/your-username/your-repository.git

cd your-repository

Create a virtual environment (optional but recommended):

python -m venv env

source env/bin/activate      # For Linux/Mac

env\Scripts\activate        # For Windows

Install the required dependencies:

pip install -r requirements.txt

Set up the database:

python manage.py makemigrations

python manage.py migrate

Create a superuser:

python manage.py createsuperuser

Run the development server:

python manage.py runserver

Access the API at http://localhost:8000/ and the admin panel at http://localhost:8000/admin/.

## Endpoints

/doctors: Get all doctors list (GET) and create a new doctor (POST).

/doctors/<pk>: Get, update, or delete a specific doctor by ID.

/patients: Get all patients list (GET) and create a new patient (POST).

/patients/<pk>: Get, update, or delete a specific patient by ID.

/patient_records: Get all patient records (GET) and create a new record (POST).

/patient_records/<pk>: Get, update, or delete a specific patient record by ID.

/departments: Get all departments (GET) and create a new department (POST).

/departments/<pk>/doctors: Get all doctors in a specific department (GET) and update the department (PUT).

/departments/<pk>/patients: Get all patients in a specific department (GET) and update the department (PUT).

/login: Obtain an access token using user credentials (GET).

/register: Create a new user (POST).

/logout: Delete user token to log out (POST).

## Permissions

Doctors can access /doctors, /doctors/<pk>, /departments/<pk>/doctors, and /patient_records.

Patients can access /patients, /patients/<pk>, and /departments/<pk>/patients.

Doctors and Patients can access /patient_records/<pk>.

Anyone can access /departments, /login, /register, and /logout.

## Technologies Used

Django and Django Rest Framework for building the API

SQLite3 for the database (you can switch to other databases like MySQL or PostgreSQL)

Knox for token-based authentication

CORS middleware for handling Cross-Origin Resource Sharing

## Contributions

Contributions to the project are welcome! Please feel free to create pull requests or report any issues you encounter.


## Acknowledgments
Thank you for checking out this Django API project! If you have any questions or need further assistance, please don't hesitate to contact me.
 