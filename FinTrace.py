import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os, json

from phase1 import (
    show_search,
    show_edit_transaction,
    show_delete_transaction,
    show_monthly_summary,
    show_savings_rate,
    show_budget_alert,
    show_wallets
)

from phase2 import (
    financial_goals,
    emergency_fund,
    recurring_transactions,
    export_pdf,
    monthly_reports
)

from phase3 import (
    show_ai_insights,
    show_spending_prediction,
    show_auto_category_detection,
    show_smart_recommendations
)

from auth import check_login
from auth import logout

user = check_login()

if user is None:

    st.session_state.logged_in = False

    if "username" in st.session_state:
        del st.session_state["username"]

    st.switch_page("pages/login.py")
    st.stop()

st.session_state.logged_in = True
st.session_state.username = user

st.session_state.logged_in = True
st.session_state.username = user

username = st.session_state.username


st.set_page_config(page_title="FinTrace Pro", page_icon="💰", layout="wide")

DATA_FOLDER = "data"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

DATA_FILE = os.path.join(
    DATA_FOLDER,
    f"{username}.csv"
)

CAT_FILE = os.path.join(
    DATA_FOLDER,
    f"{username}_categories.json"
)


if not os.path.exists(DATA_FILE):
    pd.DataFrame(
    columns=[
        "Type",
        "Amount",
        "Category",
        "Description",
        "Wallet",
        "Date"
    ]
).to_csv(DATA_FILE,index=False)

if not os.path.exists(CAT_FILE):
    with open(CAT_FILE, "w") as f:
        json.dump([], f)

try:
    with open(CAT_FILE, "r") as f:
        saved_categories = json.load(f)
    if not isinstance(saved_categories, list):
        saved_categories = []
except:
    saved_categories = []

bg = "#f8fafc"
card = "#ffffff"
text = "#0f172a"

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

/* Main app */
.stApp{
    background:#f8fafc !important;
}

/* Main content area */
.main .block-container{
    background:#f8fafc !important;
    padding-top:2rem;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#111827,#030712) !important;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* Sidebar navigation */
[data-testid="stSidebarNav"]{
    background:transparent !important;
}

[data-testid="stSidebarNav"] *{
    color:white !important;
}

/* Metric cards */
div[data-testid="stMetric"]{
    background:white !important;
    border-radius:18px;
    padding:20px;
    box-shadow:0 2px 12px rgba(0,0,0,.05);
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stDateInput input{
    background:white !important;
}

/* Selectboxes */
[data-baseweb="select"]{
    background:white !important;
    border-radius:10px;
}

/* Buttons */
.stButton button{
    width:100%;
    height:52px;
    border:none;
    border-radius:14px;
    background:linear-gradient(135deg,#22c55e,#16a34a);
    color:white !important;
    font-weight:700;
}

/* Dataframe */
[data-testid="stDataFrame"]{
    border-radius:14px;
    overflow:hidden;
}

/* Expander */
.streamlit-expanderHeader{
    font-weight:600;
}

/* Keep Plotly charts normal */
.js-plotly-plot{
    background:white !important;
}

</style>
""", unsafe_allow_html=True)

st.title("💰 FinTrace Pro")

df = pd.read_csv(DATA_FILE)

st.sidebar.title("🚀 FinTrace")

st.sidebar.success(f"👤 {username}")

if st.sidebar.button("🚪 Logout"):

    logout()

    st.session_state.clear()

    st.switch_page("pages/login.py")

    st.stop()

# page = st.sidebar.radio(
#     "Navigate",
#     [
#         "Dashboard",
#         "Add Transaction",
#         "Analytics",
#         "Budget",
#         "Manage",
#         "Extra Features"
#     ]
# )

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Add Transaction",
        "Analytics",
        "Budget",
        "Manage",
        "Extra Features"
    ]
)

if page == "Dashboard":

    income = df[df["Type"]=="Income"]["Amount"].sum() if len(df) else 0
    expense = df[df["Type"]=="Expense"]["Amount"].sum() if len(df) else 0
    balance = income - expense

    a,b,c = st.columns(3)

    a.metric("Balance", f"Rs.{balance:,.0f}")
    b.metric("Income", f"Rs.{income:,.0f}")
    c.metric("Expense", f"Rs.{expense:,.0f}")

    show_monthly_summary(df)
    show_savings_rate(df)

    st.subheader("Recent Transactions")

    if len(df):
        st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)
    else:
        st.info("No transactions available")

elif page == "Add Transaction":

    st.subheader("Add New Transaction")

    if "form_reset" not in st.session_state:
        st.session_state.form_reset = 0

    ttype = st.radio(
        "Transaction Type",
        ["Expense", "Income"],
        horizontal=True,
        key=f"type_{st.session_state.form_reset}"
    )

    amount = st.number_input(
        "Amount",
        min_value=1.0,
        key=f"amount_{st.session_state.form_reset}"
    )

    if saved_categories:
        category = st.selectbox(
            "Category",
            saved_categories + ["Other"],
            key=f"category_{st.session_state.form_reset}"
        )
    else:
        category = st.text_input(
            "Category",
            key=f"category_{st.session_state.form_reset}"
        )

    if category == "Other":
        category = st.text_input(
            "New Category",
            key=f"new_category_{st.session_state.form_reset}"
        )

    description = st.text_input(
        "Description",
        key=f"description_{st.session_state.form_reset}"
    )

    wallet = st.selectbox(
        "Wallet",
        ["Cash", "eSewa", "Khalti", "Bank"],
        key=f"wallet_{st.session_state.form_reset}"
    )


    tx_date = st.date_input(
        "Date",
        date.today(),
        key=f"date_{st.session_state.form_reset}"
    )

    # Current Balance
    income_total = df[df["Type"] == "Income"]["Amount"].sum()
    expense_total = df[df["Type"] == "Expense"]["Amount"].sum()
    current_balance = income_total - expense_total

    st.info(f"💰 Current Balance: Rs.{current_balance:,.2f}")

    if st.button(
        "Save Transaction",
        key=f"save_{st.session_state.form_reset}"
    ):

        # Prevent overspending
        if ttype == "Expense" and amount > current_balance:

            st.error(
                f"❌ Insufficient Balance! Available Balance: Rs.{current_balance:,.2f}"
            )

        else:

            row = pd.DataFrame([{
                "Type": ttype,
                "Amount": amount,
                "Category": category,
                "Description": description,
                "Wallet": wallet,
                "Date": tx_date
            }])

            df = pd.concat([df, row], ignore_index=True)

            df.to_csv(
                DATA_FILE,
                index=False
            )

            if category and category not in saved_categories:
                saved_categories.append(category)

                with open(CAT_FILE, "w") as f:
                    json.dump(saved_categories, f)

            st.success("✅ Transaction Added")

            st.session_state.form_reset += 1

            st.rerun()

elif page == "Analytics":

    st.subheader("Analytics")

    expense_df = df[df["Type"]=="Expense"]

    if len(expense_df):

        pie = px.pie(
            expense_df,
            values="Amount",
            names="Category",
            hole=.55,
            title="Expense Breakdown"
        )

        st.plotly_chart(pie, use_container_width=True)

        bar = px.bar(
            expense_df.groupby("Category")["Amount"].sum().reset_index(),
            x="Category",
            y="Amount",
            title="Category Spending"
        )

        st.plotly_chart(bar, use_container_width=True)

    else:
        st.info("No expense data yet")

elif page == "Budget":

    st.subheader("Budget Goal")

    budget = st.number_input(
        "Monthly Budget",
        min_value=1000.0,
        value=20000.0
    )

    expense = df[df["Type"]=="Expense"]["Amount"].sum() if len(df) else 0

    st.progress(min(expense/budget,1.0))

    st.write(f"Spent: Rs.{expense:,.2f}")
    st.write(f"Remaining: Rs.{max(budget-expense,0):,.2f}")

    st.divider()

    show_budget_alert(df)

elif page == "Manage":

    st.subheader("Manage Transactions")

    if len(df):

        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Export CSV",
            df.to_csv(index=False).encode(),
            "fintrace_export.csv",
            "text/csv"
        )

        

        st.subheader("⚙️ Management Tools")

        manage_tool = st.radio(
            "Choose Tool",
            [
                "Search",
                "Edit",
                "Delete",
                "Wallets"
            ],
            horizontal=True
        )

        st.divider()

        if manage_tool == "Search":
            show_search(df)

        elif manage_tool == "Edit":
            show_edit_transaction(df, DATA_FILE)

        elif manage_tool == "Delete":
            show_delete_transaction(df, DATA_FILE)

        elif manage_tool == "Wallets":
            show_wallets(df)

    else:
        st.info("No data found")

elif page == "Extra Features":

    st.title("🚀 Extra Features")

    feature = st.radio(
        "Select Feature",
        [
            "🎯 Goals",
            "🚨 Emergency Fund",
            "🔁 Recurring",
            "📄 PDF Export",
            "📊 Monthly Reports",
            "🧠 AI Insights",
            "🔮 Prediction",
            "🏷 Auto Category",
            "💡 Recommendations"
        ]
    )

    if feature == "🎯 Goals":
        financial_goals(df)

    elif feature == "🚨 Emergency Fund":
        emergency_fund(df)

    elif feature == "🔁 Recurring":
        recurring_transactions(df)

    elif feature == "📄 PDF Export":
        export_pdf(df)

    elif feature == "📊 Monthly Reports":
        monthly_reports(df)

    elif feature == "🧠 AI Insights":
        show_ai_insights(df)

    elif feature == "🔮 Prediction":
        show_spending_prediction(df)

    elif feature == "🏷 Auto Category":
        show_auto_category_detection(df)

    elif feature == "💡 Recommendations":
        show_smart_recommendations(df)

st.markdown("---")
st.caption("FinTrace Pro • Developed by Sahil Jogi")
