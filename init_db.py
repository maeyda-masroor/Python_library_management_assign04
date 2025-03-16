import sqlite3

def init():
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS LIB(
        LIB_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT UNIQUE NOT NULL,
        PASSWORD TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS MEMBERS (
                        MEM_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT NOT NULL,
                        EMAIL TEXT UNIQUE NOT NULL)''')

    # Books Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS BOOKS (
                        BOOK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        TITLE TEXT NOT NULL,
                        AUTHOR TEXT NOT NULL,
                        YEAR INTEGER NOT NULL,
                        GENERE TEXT,
                        available_copies INTEGRER NOT NULL,
                        totalcopies Integer NOT NULL,
                        READ_STATUS BOOLEAN DEFAULT 0)''')

    # Borrowed Books Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS BorrowedBooks (
                        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        mem_id INTEGER,
                        book_id INTEGER,
                        borrow_date DATE DEFAULT CURRENT_DATE,
                        due_date DATE,
                        return_date DATE NULL,
                        status TEXT DEFAULT 'Borrowed',
                        FOREIGN KEY (mem_id) REFERENCES Members(mem_id),
                        FOREIGN KEY (book_id) REFERENCES Books(book_id)
                        )''')
                    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Fines (
                        fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        borrow_id INTEGER,
                        fine_amount INTEGER DEFAULT 0,
                        fine_paid BOOLEAN DEFAULT 0,
                        FOREIGN KEY (borrow_id) REFERENCES BorrowedBooks(borrow_id)
                        )''')

    conn.commit()
    conn.close()
