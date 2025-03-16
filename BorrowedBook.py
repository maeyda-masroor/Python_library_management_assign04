import sqlite3
from datetime import datetime, timedelta
import pandas as pd


def borrow_book(mem_id, book_id):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    
    # Check book availability
    cursor.execute("SELECT copies_available FROM Books WHERE book_id=?", (book_id,))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        cursor.execute("INSERT INTO BorrowedBooks (mem_id, book_id) VALUES (?, ?)", (mem_id, book_id))
        cursor.execute("UPDATE Books SET copies_available = copies_available - 1 WHERE book_id=?", (book_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def return_book(borrow_id, book_id):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()

    # Fetch Borrow Date
    cursor.execute("SELECT borrow_date FROM BorrowedBooks WHERE borrow_id=?", (borrow_id,))
    borrow_date = cursor.fetchone()[0]
    
    borrow_date = datetime.strptime(borrow_date, "%Y-%m-%d")
    due_date = borrow_date + timedelta(days=7)  # 7-day borrowing period
    return_date = datetime.now()
    
    fine = 0
    if return_date > due_date:
        overdue_days = (return_date - due_date).days
        fine = overdue_days * 10  # ₹10 per day after 7 days

    cursor.execute("UPDATE BorrowedBooks SET return_date = ?, fine = ? WHERE borrow_id=?", 
                   (return_date.strftime("%Y-%m-%d"), fine, borrow_id))
    cursor.execute("UPDATE Books SET copies_available = copies_available + 1 WHERE book_id=?", (book_id,))
    conn.commit()
    conn.close()

def pay_fine(borrow_id):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE BorrowedBooks SET fine_paid = 1 WHERE borrow_id=?", (borrow_id,))
    conn.commit()
    conn.close()

def fetch_borrowed_books():
    conn = sqlite3.connect("lib.db")
    df = pd.read_sql('''SELECT BorrowedBooks.borrow_id, Members.name, Books.title, Books.author, BorrowedBooks.borrow_date, 
                        BorrowedBooks.return_date, BorrowedBooks.fine, BorrowedBooks.fine_paid
                        FROM BorrowedBooks 
                        JOIN Members ON BorrowedBooks.MEM_ID = Members.MEM_ID 
                        JOIN Books ON BorrowedBooks.book_id = Books.book_id''', conn)
    conn.close()
    return df

