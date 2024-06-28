import streamlit as st
import psycopg2
import pandas as pd
import requests
from streamlit_lottie import st_lottie

config = {
    'user': 'postgres', 
    'password': 'root', 
    'host': 'localhost',
    'port': 5432,
    'database': 'librarydb'
}

def loti(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def create_connection():
    """Create a connection to the PostgreSQL database."""
    try:
        db = psycopg2.connect(**config)
    except psycopg2.OperationalError as e:
        if "database \"librarydb\" does not exist" in str(e):
            db = psycopg2.connect(user=config['user'], password=config['password'], host=config['host'], port=config['port'])
            create_database(db)
            db.close()
            db = psycopg2.connect(**config)
    return db

def create_database(db):
    """Create the 'librarydb' database if it doesn't exist."""
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE librarydb")
    cursor.close()
    db.commit()

def create_books_table(db):
    """Create the books table in the database."""
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        genre VARCHAR(255),
        published_year INT,
        isbn VARCHAR(255),
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    db.commit()
    cursor.close()
    st.write("Books table created successfully.")

def create_members_table(db):
    """Create the members table in the database."""
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255),
        contact_number VARCHAR(255),
        address VARCHAR(255),
        date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    db.commit()
    cursor.close()
    st.write("Members table created successfully.")

def create_borrow_records_table(db):
    """Create the borrow_records table in the database."""
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrow_records (
        id SERIAL PRIMARY KEY,
        book_id INT REFERENCES books(id),
        member_id INT REFERENCES members(id),
        borrow_date DATE,
        return_date DATE,
        due_date DATE
    )
    """)
    db.commit()
    cursor.close()
    st.write("Borrow records table created successfully.")

def insert_book_record(db, title, author, genre, published_year, isbn):
    """Insert a new book record into the 'books' table."""
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO books (title, author, genre, published_year, isbn)
    VALUES (%s, %s, %s, %s, %s)
    """, (title, author, genre, published_year, isbn))
    db.commit()
    cursor.close()
    st.write("Book record inserted successfully.")

def fetch_all_books(db):
    """Fetch all records from the 'books' table."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    return books

def delete_book_record(db, delete_option, delete_value):
    """Delete a book record from the 'books' table based on ID or title."""
    cursor = db.cursor()
    if delete_option == "ID":
        cursor.execute("DELETE FROM books WHERE id = %s", (delete_value,))
    elif delete_option == "Title":
        cursor.execute("DELETE FROM books WHERE title = %s", (delete_value,))
    db.commit()
    cursor.close()
    st.write("Book record deleted successfully.")

def insert_member_record(db, name, email, contact_number, address):
    """Insert a new member record into the 'members' table."""
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO members (name, email, contact_number, address)
    VALUES (%s, %s, %s, %s)
    """, (name, email, contact_number, address))
    db.commit()
    cursor.close()
    st.write("Member record inserted successfully.")

def fetch_all_members(db):
    """Fetch all records from the 'members' table."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    cursor.close()
    return members

def delete_member_record(db, delete_option, delete_value):
    """Delete a member record from the 'members' table based on ID or name."""
    cursor = db.cursor()
    if delete_option == "ID":
        cursor.execute("DELETE FROM members WHERE id = %s", (delete_value,))
    elif delete_option == "Name":
        cursor.execute("DELETE FROM members WHERE name = %s", (delete_value,))
    db.commit()
    cursor.close()
    st.write("Member record deleted successfully.")

def insert_borrow_record(db, book_id, member_id, borrow_date, due_date):
    """Insert a new borrow record into the 'borrow_records' table."""
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO borrow_records (book_id, member_id, borrow_date, due_date)
    VALUES (%s, %s, %s, %s)
    """, (book_id, member_id, borrow_date, due_date))
    db.commit()
    cursor.close()
    st.write("Borrow record inserted successfully.")

def fetch_all_borrow_records(db):
    """Fetch all records from the 'borrow_records' table."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM borrow_records")
    borrow_records = cursor.fetchall()
    cursor.close()
    return borrow_records

def delete_borrow_record(db, delete_option, delete_value):
    """Delete a borrow record from the 'borrow_records' table based on ID or book ID."""
    cursor = db.cursor()
    if delete_option == "ID":
        cursor.execute("DELETE FROM borrow_records WHERE id = %s", (delete_value,))
    elif delete_option == "Book ID":
        cursor.execute("DELETE FROM borrow_records WHERE book_id = %s", (delete_value,))
    db.commit()
    cursor.close()
    st.write("Borrow record deleted successfully.")

def main():
    st.set_page_config(page_title="Library Management System", page_icon=":books:", layout="wide")
    st.title("Library Management System")

    db = create_connection()

    st.sidebar.title("Navigation")
    options = ["Home", "Books", "Members", "Borrow Records"]
    choice = st.sidebar.radio("Go to", options)

    if choice == "Home":
        st.subheader("Home")
        st_lottie(loti("https://assets10.lottiefiles.com/packages/lf20_ybiszbil.json"), height=300, key="home_animation")

    elif choice == "Books":
        st.subheader("Books Management")
        action = st.selectbox("Select Action", ["Add Book", "View All Books", "Delete Book"])

        if action == "Add Book":
            st.subheader("Add New Book")
            with st.form("book_form"):
                title = st.text_input("Title")
                author = st.text_input("Author")
                genre = st.text_input("Genre")
                published_year = st.number_input("Published Year", min_value=0, max_value=9999)
                isbn = st.text_input("ISBN")
                submit_button = st.form_submit_button(label="Add Book")

                if submit_button:
                    insert_book_record(db, title, author, genre, published_year, isbn)

        elif action == "View All Books":
            books = fetch_all_books(db)
            df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Published Year", "ISBN", "Date Added"])
            st.dataframe(df)

        elif action == "Delete Book":
            st.subheader("Delete Book")
            delete_option = st.selectbox("Delete by", ["ID", "Title"])
            delete_value = st.text_input(f"Enter {delete_option}")
            if st.button("Delete Book"):
                delete_book_record(db, delete_option, delete_value)

    elif choice == "Members":
        st.subheader("Members Management")
        action = st.selectbox("Select Action", ["Add Member", "View All Members", "Delete Member"])

        if action == "Add Member":
            st.subheader("Add New Member")
            with st.form("member_form"):
                name = st.text_input("Name")
                email = st.text_input("Email")
                contact_number = st.text_input("Contact Number")
                address = st.text_area("Address")
                submit_button = st.form_submit_button(label="Add Member")

                if submit_button:
                    insert_member_record(db, name, email, contact_number, address)

        elif action == "View All Members":
            members = fetch_all_members(db)
            df = pd.DataFrame(members, columns=["ID", "Name", "Email", "Contact Number", "Address", "Date Joined"])
            st.dataframe(df)

        elif action == "Delete Member":
            st.subheader("Delete Member")
            delete_option = st.selectbox("Delete by", ["ID", "Name"])
            delete_value = st.text_input(f"Enter {delete_option}")
            if st.button("Delete Member"):
                delete_member_record(db, delete_option, delete_value)

    elif choice == "Borrow Records":
        st.subheader("Borrow Records Management")
        action = st.selectbox("Select Action", ["Add Borrow Record", "View All Borrow Records", "Delete Borrow Record"])

        if action == "Add Borrow Record":
            st.subheader("Add New Record")
            with st.form("borrow_form"):
                book_id = st.number_input("Book ID", min_value=1)
                member_id = st.number_input("Member ID", min_value=1)
                borrow_date = st.date_input("Borrow Date")
                due_date = st.date_input("Due Date")
                submit_button = st.form_submit_button(label="Add Record")

                if submit_button:
                    insert_borrow_record(db, book_id, member_id, borrow_date, due_date)

        elif action == "View All Borrow Records":
            borrow_records = fetch_all_borrow_records(db)
            df = pd.DataFrame(borrow_records, columns=["ID", "Book ID", "Member ID", "Borrow Date", "Return Date", "Due Date"])
            st.dataframe(df)

        elif action == "Delete Borrow Record":
            st.subheader("Delete Borrow Record")
            delete_option = st.selectbox("Delete by", ["ID", "Book ID"])
            delete_value = st.text_input(f"Enter {delete_option}")
            if st.button("Delete Record"):
                delete_borrow_record(db, delete_option, delete_value)

    db.close()

if __name__ == "__main__":
    main()
