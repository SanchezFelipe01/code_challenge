# Code Challenge

This project reads data from three **.CSV** files and store it in a local **PostgreSQL database**. Once the data is ingested some operations are made to generate two specific outputs required by the stakeholders.

This project uses popular libraries like **Flask**, **SQLAlchemy** and **Pandas**.

Follow the next steps to execute the project:

## Clone the Project

Select a folder to store the code, the use the following command to clone the repository:
```bash
git clone https://github.com/SanchezFelipe01/code_challenge.git
```

## Database Setup

1. **Install PostgreSQL:**
   Ensure that PostgreSQL is installed on your machine. You can download it from the [PostgreSQL Official Website](https://www.postgresql.org/download/).

2. **Create the Database:**
   Create a database in PostgreSQL with the name of your choice. You can use the command-line interface (`psql`) or a graphical tool like PgAdmin.

3. **Username and Password:**
   Make sure you have a user and password with sufficient privileges to access and modify the database you created.

## Setting up a Virtual Environment

It's recommended to set up a virtual environment to manage project dependencies. Follow these steps:

1. **Install virtualenv (if not installed):**
   ```bash
   pip install virtualenv
   ```

2. **Navigate to your project directory:**
    ```bash
    cd path\to\your\project
    ```

3. **Create a new environment:**
   ```bash
   python -m venv .\venv
   ```
     o

   ```bash
   py -m venv .\venv
   ```

4. **Activate the new environment:**
    ```bash
    .\venv\Scripts\Activate
    ```

## Installing Dependencies

Use the following command to install the project dependencies. It's recommended to set up a virtual environment before installing dependencies.

```bash
pip install -r requirements.txt
```

## Setting up the `db_config.py` File

The `db_config.py` file contains the connection information for the database, modify it if necessary.

In this case, the first _postgres_ is the username, _12345_ is the password and the second _postgres_ is the database name.

```python
# db_config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## Start the application

Open a terminal and go to your project root folder, then execute this command:
```bash
py .\app\__init_.py
```

After that, in your browser go to **http://127.0.0.1:5000/**. Now you can interact with the application.