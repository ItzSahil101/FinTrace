import streamlit as st
import pandas as pd
import json
import os

# ==========================
# ALREADY LOGGED IN CHECK
# ==========================
from auth import check_login

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
    page_title="FinTrace Pro - Sign Up",
    page_icon="💰",
    layout="centered"
)

# ==========================
# FIX: BASE PATH (IMPORTANT FOR CLOUD + LOCAL)
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_FILE = os.path.join(BASE_DIR, "users.json")
DATA_FOLDER = os.path.join(BASE_DIR, "data")

# ==========================
# FILE INIT
# ==========================
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# ==========================
# LOAD USERS SAFELY
# ==========================
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

users = load_users()

# ==========================
# FIX: NORMALIZE USERNAME
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
}

section[data-testid="stSidebar"] *{
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
# UI
# ==========================
st.markdown('<div class="title">💰 FinTrace Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Create your personal finance account</div>', unsafe_allow_html=True)

st.info("Track expenses, income, budgets, savings goals, reports and AI insights in one dashboard.")

with st.expander("📖 Learn More"):
    st.markdown("""
### Why FinTrace Pro?

✅ Track every rupee  
✅ Manage income & expenses  
✅ Savings goals  
✅ Budget management  
✅ Monthly reports  
✅ AI insights  
""")

# ==========================
# FORM
# ==========================
st.subheader("📝 Create Account")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

# ==========================
# SIGNUP LOGIC (FIXED)
# ==========================
if st.button("🚀 Create Account"):

    username_clean = clean_username(username)

    # validations
    if not username_clean:
        st.error("❌ Please enter username")

    elif len(username_clean) < 4:
        st.error("❌ Username must be at least 4 characters")

    elif not password:
        st.error("❌ Please enter password")

    elif len(password) < 6:
        st.error("❌ Password must be at least 6 characters")

    elif password != confirm_password:
        st.error("❌ Password mismatch")

    elif username_clean in users:
        st.error("❌ Username already exists")

    else:
        # SAVE USER (FIXED)
        users[username_clean] = password
        save_users(users)

        # CREATE USER FILE
        user_file = os.path.join(DATA_FOLDER, f"{username_clean}.csv")

        pd.DataFrame(columns=[
            "Type", "Amount", "Category", "Description", "Wallet", "Date"
        ]).to_csv(user_file, index=False)

        st.success("✅ Account created!")
        st.info("Now go to login page")

# ==========================
# LOGIN BUTTON
# ==========================
st.markdown("---")
st.write("Already have an account?")

if st.button("🔑 Go To Login"):
    st.switch_page("pages/login.py")