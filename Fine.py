import sqlite3
from datetime import datetime, timedelta
import pandas as pd

def view_fine():
    conn = sqlite3.connect("lib.db")
    df = pd.read_sql("SELECT * FROM FINES", conn)
    conn.close()
    return df

# Calculate and Update Fine
def calculate_fine(borrow_id):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT due_date FROM BorrowedBooks WHERE borrow_id=?", (borrow_id,))
    due_date = cursor.fetchone()[0]
    
    due_date = datetime.strptime(due_date, "%Y-%m-%d")
    return_date = datetime.now()
    
    fine = 0
    if return_date > due_date:
        overdue_days = (return_date - due_date).days
        fine = overdue_days * 10  # ₹10 per day
    
    cursor.execute("INSERT INTO Fines (borrow_id, fine_amount) VALUES (?, ?)", (borrow_id, fine))
    conn.commit()
    conn.close()
    return fine

# Pay Fine
def pay_fine(fine_id):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Fines SET fine_paid = 1 WHERE fine_id=?", (fine_id,))
    conn.commit()
    conn.close()
