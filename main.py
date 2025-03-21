import os
import streamlit as st
from database import create_table, add_book, viewall_books, search_book, update_book, delete_book
import datetime

create_table()

current_year = datetime.datetime.now().year

if not os.path.exists("covers"):
    os.makedirs("covers")

st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")

# Custom styling
st.markdown(
    """
    <style>
    .big-title { font-size: 36px; font-weight: bold; text-align: center; }
    .sub-title { font-size: 20px; text-align: center; }
    .feature-card { border-radius: 10px; padding: 15px; background-color: #708090; }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Menu
st.sidebar.title("Menu")
st.sidebar.subheader("Choose an action:")
page = st.sidebar.radio("", ["Home", "Add Books", "All Books", "Update Books", "Delete Books"])

if page == "Home":
    st.title("Personal Library Manager📚")

    # Hero Section
    st.markdown("---")  
    st.markdown("<p class='big-title'>📚 Welcome to Personal Library Manager</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Easily manage, search, and track your book collection with this simple tool.</p>", unsafe_allow_html=True)

    st.write("---")  # Horizontal line

    # Search Bar
    search_term = st.text_input("🔍Search for a book...")

    if st.button("Search🔍"):
        if search_term.strip():
            results = search_book(search_term)
            if results:
                st.write("### 📚 Search Results:")
                for book in results:
                    title, author, year, genre, read, cover = book[1], book[2], book[3], book[4], book[5], book[6]
                    if cover and os.path.exists(cover):
                        st.image(cover, width=160)
                    st.write(f"📖 **{title}** by {author} ({year})")
                    st.write(f"📝 **Genre:** {genre} | **Read:** {read.capitalize()}")
            else:
                st.warning("⚠️ No books found.")
        else:
            st.error("⚠️ Please enter a search term.")

    # Features Section
    st.subheader("✨ Key Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='feature-card'>📖 Add new books easily</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='feature-card'>📂 View & manage your library</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='feature-card'>🛠️ Update and delete books.</div>", unsafe_allow_html=True)

    st.write("---")

elif page == "Add Books":
    st.title("Add Books")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Enter Publication Year", min_value=1000, max_value=current_year, step=1)
    genre = st.text_input("Genre")
    read = st.radio("Read", ["Yes", "No"])
    cover_image = st.file_uploader("Upload Book Cover (JPG/PNG)", type=["jpg", "png"])

    if st.button("Add Book"):
        if not title or not author or not genre or not read:
            st.error("⚠️ Please fill in all fields before adding the book.")
        else:
            cover_path = None  
            if cover_image is not None:
                cover_path = os.path.join("covers", cover_image.name).replace("\\", "/")
                with open(cover_path, "wb") as f:
                    f.write(cover_image.getbuffer())

            add_book(title, author, year, genre, read.lower(), cover_path)
            st.success(f"✅ '{title}' by {author} added successfully!")
            st.balloons()

elif page == "All Books":
    st.title("All Books📖")
    books = viewall_books()

    if not books:
        st.warning("⚠️ No books found in your library.")
    else:
        st.write("📚 Your Library:")
        for book in books:
            title, author, year, genre, read, cover = book[1], book[2], book[3], book[4], book[5], book[6]
            if cover and os.path.exists(cover):
                st.image(cover, width=160)
            st.write(f"📖 **{title}** by {author} ({year})")
            st.write(f"📝 **Genre:** {genre} | **Read:** {read.capitalize()}")
            st.markdown("---")


elif page == "Update Books":
    st.title("Update Books🛠️")
    books = viewall_books()
    if books:
        book_id = st.number_input("Enter the ID of the book you want to update", min_value=1, max_value=len(books), step=1)
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Enter Publication Year", min_value=1000, max_value=current_year, step=1)
        genre = st.text_input("Genre")
        read = st.radio("Read", ["Yes", "No"])
        if st.button("Update Book"):
            update_book(title, author, year, genre, read.lower(), book_id)
            st.success(f"✅ Book with ID {book_id} updated successfully!")
            st.balloons()

elif page == "Delete Books":
    st.title("🗑️ Delete Books")
    books = viewall_books()
    if books:
        book_titles = [book[1] for book in books]
        selected_title = st.selectbox("Select a book to delete", book_titles)
        if st.button("Delete"):
            delete_book(selected_title)
            st.success(f"✅ '{selected_title}' deleted successfully!")
            st.snow()

st.write("📌 Made with ❤️ using Streamlit")