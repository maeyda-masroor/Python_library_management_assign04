import sqlite3
from datetime import datetime, timedelta
import pandas as pd


def borrow_book(mem_id, book_id):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    
    # Check book availability
    cursor.execute("SELECT available_copies FROM Books WHERE book_id=?", (book_id,))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")  # 7 days borrow period
        cursor.execute("INSERT INTO BorrowedBooks (mem_id, book_id, due_date) VALUES (?, ?, ?)", (mem_id, book_id, due_date))
        cursor.execute("UPDATE Books SET available_copies = available_copies - 1 WHERE book_id=?", (book_id,))
        conn.commit()
    conn.close()

# Return Book
def return_book(borrow_id, book_id):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()

    # Update return date
    return_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("UPDATE BorrowedBooks SET return_date=?, status='Returned' WHERE borrow_id=?", 
                   (return_date, borrow_id))
    cursor.execute("UPDATE Books SET available_copies = available_copies + 1 WHERE book_id=?", (book_id,))
    conn.commit()
    conn.close()
