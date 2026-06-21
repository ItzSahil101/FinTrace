import streamlit as st
import json
import os

from auth import create_login

if st.session_state.get("logged_in", False):

    st.success(f"Already logged in as {st.session_state.username}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🏠 Go To Dashboard"):
            st.switch_page("FinTrace.py")

    with col2:
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

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
# FILES
# ==========================
USERS_FILE = "users.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

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
# DESIGN
# ==========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

/* MAIN BACKGROUND */
.stApp{
    background:linear-gradient(180deg,#111827,#030712);
}

/* SIDEBAR FIX (IMPORTANT) */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#111827,#030712) !important;
}

/* sidebar text */
section[data-testid="stSidebar"] *{
    color:white !important;
}

/* remove default sidebar nav background */
[data-testid="stSidebarNav"]{
    background:transparent;
}

/* buttons */
.stButton button{
    width:100%;
    height:52px;
    border:none;
    border-radius:14px;
    background:linear-gradient(135deg,#22c55e,#16a34a);
    color:white;
    font-weight:700;
}

.title{
    text-align:center;
    font-size:36px;
    font-weight:800;
    color:white;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)


st.subheader("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

login_btn = st.button("🔑 Login")

if login_btn:

    if username.strip() == "" or password.strip() == "":
        st.warning("⚠️ Please fill all fields.")

    elif username not in users:

        st.warning("⚠️ Account not found.")

        # if st.button("📝 Create Account"):
        #     st.switch_page("pages/signup.py")

    elif users[username] != password:

        st.error("❌ Wrong password.")

    else:

     create_login(username)

     st.session_state.logged_in = True
     st.session_state.username = username
     st.success("✅ Login successful")
     st.switch_page("FinTrace.py")

# ==========================
# SIGNUP BUTTON
# ==========================
st.markdown("---")

st.write("Don't have an account?")

if st.button("📝 Go To Sign Up"):
    st.switch_page("pages/signup.py")