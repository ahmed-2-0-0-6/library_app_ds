import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os

# Load .env file (for secrets like password)
load_dotenv()

# Connect to database
def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# --- Streamlit UI ---
st.title("📚 Add New Book")

title = st.text_input("Book Title")
author = st.text_input("Author")
year = st.text_input("Year Published")

if st.button("➕ Add Book"):
    if not title or not author or not year:
        st.warning("Please fill in all fields.")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()  # ✅ create cursor first

            sql = "INSERT INTO Books (title, author, year_published) VALUES (%s, %s, %s)"
            values = (title, author, int(year))
            cursor.execute(sql, values)
            conn.commit()

            st.success("✅ Book added successfully!")

            # Clean-up
            cursor.close()
            conn.close()

        except ValueError:
            st.error("⚠️ Year must be a number.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
