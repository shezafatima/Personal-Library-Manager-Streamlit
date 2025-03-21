import sqlite3
import os

# Function to connect to the database
def conn_db():
    connect = sqlite3.connect('library.db')
    cursor = connect.cursor()
    return connect, cursor

# Function to create the books table 
def create_table():
    connect, cursor = conn_db()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            year INTEGER,
            genre TEXT,
            read TEXT,
            cover TEXT  -- Added cover column in table creation
        )
    """)

    # Check if "cover" column exists and add it if missing
    cursor.execute("PRAGMA table_info(books);")
    columns = [column[1] for column in cursor.fetchall()]
    
    if "cover" not in columns:
        cursor.execute("ALTER TABLE books ADD COLUMN cover TEXT;")
        connect.commit()  # Only commit if an update was made
    
    connect.close()

# Function to add a new book to the database
def add_book(title, author, year, genre, read, cover):
    connect, cursor = conn_db()
    cursor.execute("INSERT INTO books (title, author, year, genre, read, cover) VALUES (?, ?, ?, ?, ?, ?)", 
                   (title, author, year, genre, read, cover))
    connect.commit()
    connect.close()

# Function to retrieve all books from the database
def viewall_books():
    connect, cursor = conn_db()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    connect.close()
    return books

# Function to search for books by title or author
def search_book(search_term):
    connect, cursor = conn_db()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f'%{search_term}%', f'%{search_term}%'))
    books = cursor.fetchall()
    connect.close()
    return books

# Function to update book details
def update_book(title, author, year, genre, read, cover, book_id):
    connect, cursor = conn_db()
    cursor.execute("UPDATE books SET title=?, author=?, year=?, genre=?, read=?, cover=? WHERE id=?", 
                   (title, author, year, genre, read, cover, book_id))
    connect.commit()
    connect.close()

# Function to delete a book by its ID 
def delete_book(title):
    connect, cursor = conn_db()
    
    # Get the cover image path before deleting the book
    cursor.execute("SELECT cover FROM books WHERE title=?", (title,))
    cover_path = cursor.fetchone()
    
    # Delete the book from the database
    cursor.execute("DELETE FROM books WHERE title=?", (title,))
    connect.commit()
    connect.close()

    # If a cover image exists, remove the file
    if cover_path and cover_path[0]:
        if os.path.exists(cover_path[0]):
            os.remove(cover_path[0])