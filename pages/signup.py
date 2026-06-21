import streamlit as st
import pandas as pd
import json
import os

if st.session_state.get("logged_in", False):

    st.success(f"Already logged in as {st.session_state.username}")

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
# LOAD USERS SAFELY
# ==========================
try:
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if not isinstance(users, dict):
        users = {}

except:
    users = {}

# ==========================
# DESIGN
# ==========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

.stApp{
    background:#f8fafc;
}
            
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#111827,#030712);
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

[data-testid="stSidebarNav"]{
    background:transparent;
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
# HEADER
# ==========================
st.markdown(
    '<div class="title">💰 FinTrace Pro</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Create your personal finance account</div>',
    unsafe_allow_html=True
)

st.info(
    "Track expenses, income, budgets, savings goals, reports and AI insights in one dashboard."
)

# ==========================
# ABOUT APP
# ==========================
with st.expander("📖 Learn More"):
    st.markdown("""
### Why FinTrace Pro?

✅ Track every rupee

✅ Manage income & expenses

✅ Savings goals

✅ Budget management

✅ Monthly reports

✅ AI insights

✅ Spending predictions

✅ Personal accounts

Each account has its own private financial records and reports.
""")

# ==========================
# SIGNUP FORM
# ==========================
st.subheader("📝 Create Account")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

signup_btn = st.button("🚀 Create Account")

if signup_btn:

    if username.strip() == "":
        st.error("❌ Please enter a username.")

    elif password.strip() == "":
        st.error("❌ Please enter a password.")

    elif password != confirm_password:
        st.error("❌ Passwords do not match.")

    elif username in users:
        st.error("❌ Username already exists.")

    else:

        users[username] = password

        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)

        user_file = os.path.join(
            DATA_FOLDER,
            f"{username}.csv"
        )

        pd.DataFrame(
            columns=[
                "Type",
                "Amount",
                "Category",
                "Description",
                "Wallet",
                "Date"
            ]
        ).to_csv(
            user_file,
            index=False
        )

        st.success("✅ Account Created Successfully!")
        st.balloons()

        st.info("You can now login with your new account.")

# ==========================
# LOGIN BUTTON
# ==========================
st.markdown("---")

st.write("Already have an account?")

if st.button("🔑 Go To Login"):
    st.switch_page("pages/login.py")