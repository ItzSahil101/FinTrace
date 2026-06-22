import streamlit as st
import os
import json
import pandas as pd

# =========================
# FIXED BASE PATH (IMPORTANT)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_FILE = os.path.join(BASE_DIR, "users.json")
DATA_FOLDER = os.path.join(BASE_DIR, "data")

ADMIN_PASSWORD = "kanepokhari7s"

# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="Admin Panel", page_icon="🔐", layout="wide")

st.title("🔐 Admin Panel - FinTrace")

# =========================
# LOAD USERS (SAFE)
# =========================
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

users = load_users()

# =========================
# DEBUG (REMOVE LATER IF YOU WANT)
# =========================
st.write("📍 USERS FILE:", USERS_FILE)

# =========================
# LOGIN STATE
# =========================
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.admin_logged_in:

    st.warning("⚠️ Admin Access Only")
    st.info('Hint: "sahil password"')

    password = st.text_input("Enter Admin Password", type="password")

    if st.button("Login"):

        if password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.success("✅ Access Granted")
            st.rerun()

        else:
            st.error("❌ Wrong password")

    st.stop()

# =========================
# DASHBOARD
# =========================
st.success("Welcome Admin 👑")

# =========================
# USERS VIEW
# =========================
st.subheader("👤 All Users")

if users:
    st.json(users)
else:
    st.warning("No users found")

# =========================
# FILE LIST
# =========================
st.subheader("📁 All User Data Files")

if os.path.exists(DATA_FOLDER):
    user_files = os.listdir(DATA_FOLDER)
else:
    user_files = []

selected_file = st.selectbox(
    "Select file to view",
    user_files if user_files else ["No files"]
)

if selected_file != "No files":

    file_path = os.path.join(DATA_FOLDER, selected_file)

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.dataframe(df)
    else:
        st.error("File not found")

# =========================
# DELETE FILE
# =========================
st.subheader("🗑️ Delete User Data")

delete_file = st.selectbox(
    "Select file to delete",
    user_files if user_files else ["No files"],
    key="delete"
)

if st.button("Delete Selected File"):

    if delete_file != "No files":
        path = os.path.join(DATA_FOLDER, delete_file)

        if os.path.exists(path):
            os.remove(path)
            st.success(f"Deleted {delete_file}")
            st.rerun()
        else:
            st.error("File already missing")

# =========================
# LOGOUT
# =========================
if st.button("🚪 Logout"):
    st.session_state.admin_logged_in = False
    st.rerun()