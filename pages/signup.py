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
# FILES
# ==========================
USERS_FILE = "users.json"
DATA_FOLDER = "data"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# ==========================
# LOAD USERS
# ==========================
try:
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    if not isinstance(users, dict):
        users = {}
except:
    users = {}

# ==========================
# CSS (ONLY SIDEBAR DARK)
# ==========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

/* MAIN PAGE = KEEP LIGHT (DO NOTHING) */

/* SIDEBAR DARK */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#111827,#030712) !important;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* sidebar nav */
[data-testid="stSidebarNav"]{
    background:transparent;
}

[data-testid="stSidebarNav"] a{
    color:white !important;
}

/* TITLE */
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

/* BUTTON */
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

signup_btn = st.button("🚀 Create Account")

if signup_btn:

    if username.strip() == "":
        st.error("❌ Please enter username")

    elif password.strip() == "":
        st.error("❌ Please enter password")

    elif password != confirm_password:
        st.error("❌ Password mismatch")

    elif username in users:
        st.error("❌ Username already exists")

    else:
        users[username] = password

        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)

        user_file = os.path.join(DATA_FOLDER, f"{username}.csv")

        pd.DataFrame(columns=[
            "Type","Amount","Category","Description","Wallet","Date"
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