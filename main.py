import init_db as db
import streamlit as st
import Librarian as lib
import Member as mem
import Books as book
import matplotlib.pyplot as plt
import BorrowedBook as bb

db_init = db.init()
st.title("Library Management System")


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None


choice = st.sidebar.radio("Choose Action", ["Librarian Login", "Member Login", "Register Librarian", "Register Member"])
  
    
if choice == "Librarian Login":
    st.subheader("Librarian Input")
    username = st.text_input("username")
    password = st.text_input("password",type="password")

    if st.button("Login"):
        if lib.authenticate_librarian(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.user_role = "Librarian"
            st.success(f"Welcome, Librarian {username}!")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

elif choice == "Member Login":
    st.subheader("Librarian Input")
    name = st.text_input("username")
    email = st.text_input("email")

    if st.button("Login"):
        if mem.authenticate_member(name,email):  # Check if email exists
            st.session_state.authenticated = True
            st.session_state.username = email
            st.session_state.user_role = "Member"
            st.success(f"Welcome, {email}!")
            st.rerun()
        else:
            st.error("Invalid Email")
    
elif choice == "Register Librarian":
    st.subheader("📝 Register Librarian")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
        
    if st.button("Register"):
        if new_password == confirm_password:
            lib.register_librarian(new_username, new_password)
            st.success("Librarian registration successful! Please log in.")
        else:
            st.error("Passwords do not match!")

elif choice == "Register Member":
    st.subheader("Register Member")
    name = st.text_input("Member Name")
    email = st.text_input("Member Email")
    
    if st.button("Register Member"):
        mem.register_member(name, email)
        st.success(f"Member '{name}' registered successfully!")

if st.session_state.authenticated:
    st.sidebar.subheader(f"{st.session_state.user_role}: {st.session_state.username}")

if st.session_state.user_role == "Librarian":
    dashboard_choice = st.sidebar.selectbox("Dashboard", ["Add Book", "View Books", "Remove Book", "Statistics", "Search Book","View Borrowed Books", "Logout"])

    if dashboard_choice == "Add Book":
        st.subheader("Add a Book")
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
        genre = st.text_input("Genre")
        read_status = st.checkbox("Mark as Read")

        if st.button("Add Book"):
            book.add_book(title, author, genre, year, read_status)
            st.success(f"Book '{title}' added successfully!")
            st.rerun()

    elif dashboard_choice == "Remove Book":
        book_id = st.number_input("Enter Book ID to Remove", min_value=1, step=1)

        if st.button("Remove Book"):
            book.remove_book(book_id)
            st.success("Book removed successfully!")
            st.rerun()   
    elif dashboard_choice == "View Books":
        st.subheader("📚 All Books in Library")
        books = book.fetch_books()
        st.dataframe(books)

    
    elif dashboard_choice == "Search Book":
        st.subheader("🔍 Search for a Book")
        query = st.text_input("Enter Title, Author, or Genre")
        
        if st.button("Search"):
            results = book.search_books(query)
            if not results.empty:
                st.dataframe(results)
            else:
                st.warning("No books found!")

    elif dashboard_choice == "Statistics":
        st.subheader("📊 Library Statistics")
        total_books, read_books, percentage_read = book.book_statistics()

        st.write(f"📘 **Total Books:** {total_books}")
        st.write(f"✅ **Books Read:** {read_books} ({percentage_read:.2f}%)")

        fig, ax = plt.subplots()
        ax.bar(["Total Books", "Read Books"], [total_books, read_books], color=["blue", "green"])
        ax.set_ylabel("Number of Books")
        ax.set_title("Library Book Statistics")

        st.pyplot(fig)
     
    elif dashboard_choice == "View Borrowed Books":
        st.subheader("📖 Borrowed Books & Fines")
        borrowed_books = bb.fetch_borrowed_books()
        st.dataframe(borrowed_books)

        borrow_id = st.number_input("Enter Borrow ID to Pay Fine", min_value=1, step=1)
        if st.button("Mark Fine as Paid"):
            bb.pay_fine(borrow_id)
            st.success("Fine marked as paid!")
 
    elif dashboard_choice == "Logout":
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.username = None
        st.success("Logged out successfully!")
        st.rerun()

elif st.session_state.user_role == "Member":
        member_dashboard_choice = st.sidebar.selectbox("Member Dashboard", ["View Books", "Search Book", "Logout"])

        if member_dashboard_choice == "View Books":
           st.subheader("📚 All Books in Library")
           books = book.fetch_books()
           st.dataframe(books)

        elif member_dashboard_choice == "Search Book":
            st.subheader("🔍 Search for a Book")
            query = st.text_input("Enter Title, Author, or Genre")
        
            if st.button("Search"):
                results = book.search_books(query)
                if not results.empty:
                    st.dataframe(results)
                else:
                    st.warning("No books found!") 
                    
        elif member_dashboard_choice == "Logout":
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.username = None
            st.success("Logged out successfully!")
            st.rerun()

