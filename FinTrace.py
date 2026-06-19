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

from phase2 import run_phase2

from phase3 import run_phase3

st.set_page_config(page_title="FinTrace Pro", page_icon="💰", layout="wide")

DATA_FILE = "transactions.csv"
CAT_FILE = "categories.json"

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
    with open(CAT_FILE,"w") as f:
        json.dump([],f)

with open(CAT_FILE,"r") as f:
    saved_categories = json.load(f)

bg = "#f8fafc"
card = "#ffffff"
text = "#0f172a"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {{
font-family:'Inter',sans-serif;
}}

.stApp {{
background:{bg};
color:{text};
}}

section[data-testid="stSidebar"] {{
background:linear-gradient(180deg,#111827,#030712);
}}

section[data-testid="stSidebar"] * {{
color:white !important;
font-size:16px !important;
}}

div[data-testid="stMetric"] {{
background:{card};
padding:20px;
border-radius:20px;
}}

.stButton button {{
background:linear-gradient(135deg,#22c55e,#16a34a);
color:white;
border:none;
border-radius:14px;
height:52px;
font-weight:700;
width:100%;
}}
</style>
""", unsafe_allow_html=True)

st.title("💰 FinTrace Pro")

df = pd.read_csv(DATA_FILE)

st.sidebar.title("🚀 FinTrace")

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
        "Extra Features",
        "Extra Features 2",
        "Extra Features 3"
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

    if st.button(
        "Save Transaction",
        key=f"save_{st.session_state.form_reset}"
    ):

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

        st.dataframe(df,use_container_width=True)

        st.download_button(
            "Export CSV",
            df.to_csv(index=False).encode(),
            "fintrace_export.csv",
            "text/csv"
        )

    else:
        st.info("No data found")

elif page == "Extra Features":

    st.title("🚀 Phase 1 Features")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Search","Edit","Delete","Wallets"]
    )

    with tab1:
        show_search(df)

    with tab2:
        show_edit_transaction(df, DATA_FILE)

    with tab3:
        show_delete_transaction(df, DATA_FILE)

    with tab4:
        show_wallets(df)
elif page == "Extra Features 2":

    st.title("🚀 Phase 2 Features")

    run_phase2(df)

elif page == "Extra Features 3":

    st.title("🚀 Phase 3 Features")

    run_phase3(df)

st.markdown("---")
st.caption("FinTrace Pro • Developed by Sahil Jogi")
