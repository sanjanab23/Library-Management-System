# Library Management System Dashboard

This project is a web-based Library Management System Dashboard built with Streamlit and PostgreSQL. It allows you to manage books, members, and borrow records in a library database. The application provides functionalities to add, view, and delete records.

## Features

- **Home Page**: Displays an animation and serves as the landing page.
- **Books Management**: Add, view, and delete book records.
- **Members Management**: Add, view, and delete member records.
- **Borrow Records Management**: Add, view, and delete borrow records.

## Installation


1. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up PostgreSQL:**

    Make sure you have PostgreSQL installed and running on your machine. Create a database named `librarydb`:

    ```sql
    CREATE DATABASE librarydb;
    ```

    Update the `config` dictionary in the `app.py` file with your PostgreSQL credentials if necessary:

    ```python
    config = {
        'user':'postgres'#change accordingly , 
        'password':'root' #change accordingly, 
        'host': 'localhost',
        'port': 5432,
        'database': 'librarydb'
    }
    ```

## Usage

1. **Run the Streamlit application:**

    ```bash
    streamlit run [name].py
    ```

2. **Navigate to the application in your web browser:**

    ```
    http://localhost:8501
    ```

3. **Use the sidebar to navigate between the different sections:**

    - **Home**: Displays an animation.
    - **Books**: Add, view, and delete book records.
    - **Members**: Add, view, and delete member records.
    - **Borrow Records**: Add, view, and delete borrow records.

## Project Structure

- `[name].py`: Main application file containing the Streamlit app and all database functions.
- `requirements.txt`: List of Python dependencies required for the project.

## Dependencies

- `streamlit`
- `psycopg2-binary`
- `pandas`
- `requests`
- `streamlit-lottie`


