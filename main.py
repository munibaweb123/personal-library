import streamlit as st
import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            genre TEXT NOT NULL,
            read_status BOOLEAN NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Load books from the database
def load_library():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# Add book to the database
def add_book(title, author, year, genre, read_status):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)",
                   (title, author, year, genre, read_status))
    conn.commit()
    conn.close()

# Remove book from the database
def remove_book(book_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# Search books in the database
def search_books(query):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%'+query+'%', '%'+query+'%'))
    books = cursor.fetchall()
    conn.close()
    return books

# Update book details
def update_book(book_id, title, author, year, genre, read_status):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title = ?, author = ?, year = ?, genre = ?, read_status = ? WHERE id = ?",
                   (title, author, year, genre, read_status, book_id))
    conn.commit()
    conn.close()

# Initialize database
init_db()

st.title('📖 Personal Library Manager')
menu = st.sidebar.radio('Select an option', ['📚 View Library', '➕ Add Book', '➖ Remove Book', '🔎 Search Book', '✏️ Update Book', '🗃️ Save & Exit'])

# View Library
if menu == '📚 View Library':
    st.sidebar.header('📚 Your Library')
    books = load_library()
    if books:
        st.table(books)
    else:
        st.write('📚 No books in your library')

# Add Book
elif menu == '➕ Add Book':
    st.sidebar.header('Add a new book')
    title = st.text_input('Title')
    author = st.text_input('Author')
    year = st.number_input('Year', min_value=2000, max_value=2050, step=1)
    genre = st.text_input('Genre')
    read_status = st.checkbox('Mark as read')

    if st.button('➕ Add Book'):
        add_book(title, author, year, genre, read_status)
        st.success('✅ Book added successfully!')
        st.rerun()

# Remove Book
elif menu == '➖ Remove Book':
    st.sidebar.header('Remove a book')
    books = load_library()
    if books:
        book_dict = {f"{book[1]} by {book[2]}": book[0] for book in books}
        selected_book = st.selectbox('Select a book to remove', list(book_dict.keys()))
        if st.button('➖ Remove Book'):
            remove_book(book_dict[selected_book])
            st.success('✅ Book removed successfully!')
            st.rerun()
    else:
        st.warning('No books in your library!')

# Search Book
elif menu == '🔎 Search Book':
    st.sidebar.header('Search a book')
    search_term = st.text_input('Enter title or author name')
    if st.button('🔍 Search'):
        results = search_books(search_term)
        if results:
            st.table(results)
        else:
            st.warning('⚠️ No books found!')

# Update Book
elif menu == '✏️ Update Book':
    st.sidebar.header('Update Book Details')
    books = load_library()
    if books:
        book_dict = {f"{book[1]} by {book[2]}": book[0] for book in books}
        selected_book = st.selectbox('Select a book to update', list(book_dict.keys()))

        # Get book details
        book_id = book_dict[selected_book]
        book_details = [book for book in books if book[0] == book_id][0]

        # Update inputs
        title = st.text_input('Title', value=book_details[1])
        author = st.text_input('Author', value=book_details[2])
        year = st.number_input('Year', min_value=2000, max_value=2050, step=1, value=book_details[3])
        genre = st.text_input('Genre', value=book_details[4])
        read_status = st.checkbox('Mark as read', value=bool(book_details[5]))

        if st.button('✏️ Update Book'):
            update_book(book_id, title, author, year, genre, read_status)
            st.success('✅ Book updated successfully!')
            st.rerun()
    else:
        st.warning('⚠️ No books in your library!')

# Save and Exit
elif menu == '🗃️ Save & Exit':
    st.success('🗃️ Library saved successfully!')
