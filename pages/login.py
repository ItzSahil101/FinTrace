import streamlit as st
import json
import os

from auth import create_login, check_login

# ==========================
# BASE PATH FIX (IMPORTANT)
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")

# ==========================
# AUTO LOGIN CHECK
# ==========================
user = check_login()

if user:
    st.session_state.logged_in = True
    st.session_state.username = user

    st.success(f"Already logged in as {user}")

    if st.button("🏠 Go To Dashboard"):
        st.switch_page("FinTrace.py")

    st.stop()

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="FinTrace Pro - Login",
    page_icon="💰",
    layout="centered"
)

# ==========================
# SAFE LOAD USERS
# ==========================
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

users = load_users()

# ==========================
# CLEAN USERNAME FUNCTION
# ==========================
def clean_username(name):
    return name.strip().lower()

# ==========================
# CSS (UNCHANGED)
# ==========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#111827,#030712) !important;
    min-height:100vh;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

[data-testid="stSidebarNav"] a{
    color:white !important;
}

.title{
    text-align:center;
    font-size:36px;
    font-weight:800;
    color:#0f172a;
}

.subtitle{
    text-align:center;
    color:#64748b;
    margin-bottom:20px;
}

.stButton button{
    width:100%;
    height:52px;
    border:none;
    border-radius:14px;
    background:linear-gradient(135deg,#22c55e,#16a34a);
    color:white;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# UI HEADER
# ==========================
st.markdown('<div class="title">💰 FinTrace Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Welcome back to your finance dashboard</div>', unsafe_allow_html=True)

st.info("Track expenses, income, budgets, savings goals, reports and AI insights in one place.")

# ==========================
# LOGIN FORM
# ==========================
st.subheader("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

# ==========================
# LOGIN LOGIC (FIXED)
# ==========================
if st.button("🔑 Login"):

    username_clean = clean_username(username)

    if not username_clean or not password:
        st.warning("⚠️ Please fill all fields.")

    elif username_clean not in users:
        st.warning("⚠️ Account not found.")

    elif users[username_clean] != password:
        st.error("❌ Wrong password.")

    else:
        create_login(username_clean)

        st.session_state.logged_in = True
        st.session_state.username = username_clean

        st.success("✅ Login successful")
        st.switch_page("FinTrace.py")
        st.stop()

# ==========================
# SIGNUP LINK
# ==========================
st.markdown("---")
st.write("Don't have an account?")

if st.button("📝 Go To Sign Up"):
    st.switch_page("pages/signup.py")