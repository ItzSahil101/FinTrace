import streamlit as st
import pandas as pd
from datetime import datetime

def show_search(df):
    st.subheader("🔍 Search Transactions")

    query = st.text_input("Search")

    if query:
        filtered = df[
            df.astype(str)
            .apply(lambda row: row.str.contains(query, case=False).any(), axis=1)
        ]

        st.dataframe(
            filtered,
            use_container_width=True
        )

def show_edit_transaction(df, data_file):

    st.subheader("✏️ Edit Transaction")

    if len(df) == 0:
        st.info("No transactions found.")
        return

    row_index = st.selectbox(
        "Select Transaction",
        df.index
    )

    row = df.loc[row_index]

    tx_type = st.selectbox(
        "Type",
        ["Income", "Expense"],
        index=0 if row["Type"] == "Income" else 1,
        key="edit_type"
    )

    amount = st.number_input(
        "Amount",
        value=float(row["Amount"]),
        key="edit_amount"
    )

    category = st.text_input(
        "Category",
        value=str(row["Category"]),
        key="edit_category"
    )

    description = st.text_input(
        "Description",
        value=str(row["Description"]),
        key="edit_description"
    )

    if st.button("Save Changes"):

        df.loc[row_index, "Type"] = tx_type
        df.loc[row_index, "Amount"] = amount
        df.loc[row_index, "Category"] = category
        df.loc[row_index, "Description"] = description

        df.to_csv(
            data_file,
            index=False
        )

        st.success("Transaction Updated")
        st.rerun()

def show_delete_transaction(df, data_file):

    st.subheader("🗑️ Delete Transaction")

    if len(df) == 0:
        st.info("No transactions found.")
        return

    row_index = st.selectbox(
        "Select Row To Delete",
        df.index,
        key="delete_select"
    )

    if st.button("Delete Transaction"):

        df = df.drop(
            index=row_index
        ).reset_index(drop=True)

        df.to_csv(
            data_file,
            index=False
        )

        st.success("Transaction Deleted")
        st.rerun()

def show_monthly_summary(df):

    st.subheader("📊 Monthly Summary")

    if len(df) == 0:
        st.info("No transactions found.")
        return

    try:

        df["Date"] = pd.to_datetime(df["Date"])

        current_month = datetime.now().month
        current_year = datetime.now().year

        month_df = df[
            (df["Date"].dt.month == current_month)
            &
            (df["Date"].dt.year == current_year)
        ]

        income = month_df[
            month_df["Type"] == "Income"
        ]["Amount"].sum()

        expense = month_df[
            month_df["Type"] == "Expense"
        ]["Amount"].sum()

        savings = income - expense

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Income",
            f"Rs.{income:,.0f}"
        )

        c2.metric(
            "Expense",
            f"Rs.{expense:,.0f}"
        )

        c3.metric(
            "Savings",
            f"Rs.{savings:,.0f}"
        )

    except:
        st.warning("Date format issue detected.")

def show_savings_rate(df):

    st.subheader("💹 Savings Rate")

    if len(df) == 0:
        return

    income = df[
        df["Type"] == "Income"
    ]["Amount"].sum()

    expense = df[
        df["Type"] == "Expense"
    ]["Amount"].sum()

    if income > 0:

        rate = (
            (income - expense)
            / income
        ) * 100

        st.metric(
            "Savings Rate",
            f"{rate:.1f}%"
        )

def show_budget_alert(df):

    st.subheader("⚠️ Budget Alert")

    budget = st.number_input(
        "Monthly Budget",
        min_value=1000.0,
        value=20000.0,
        key="budget_phase1"
    )

    expense = df[
        df["Type"] == "Expense"
    ]["Amount"].sum()

    percent = (expense / budget) * 100

    st.progress(
        min(percent / 100, 1.0)
    )

    st.write(
        f"Used {percent:.1f}% of budget"
    )

    if percent >= 90:
        st.error(
            "Budget usage exceeded 90%"
        )
    elif percent >= 75:
        st.warning(
            "Budget usage exceeded 75%"
        )
    else:
        st.success(
            "Budget is under control"
        )

def show_wallets(df):

    st.subheader("💳 Wallet Overview")

    if "Wallet" not in df.columns:

        st.info(
            "Wallet support will activate once wallet transactions are added."
        )

        return

    wallet_summary = (
        df.groupby("Wallet")["Amount"]
        .sum()
        .reset_index()
    )

    st.dataframe(
        wallet_summary,
        use_container_width=True
    )

def show_wallets(df):

    st.subheader("💳 Wallet Overview")

    if "Wallet" not in df.columns:
        st.info("Wallet support will activate once wallet transactions are added.")
        return

    if len(df) == 0:
        st.info("No data available.")
        return

    # ---------------- REAL WALLET CALCULATION ----------------

    income_df = df[df["Type"] == "Income"].groupby("Wallet")["Amount"].sum()
    expense_df = df[df["Type"] == "Expense"].groupby("Wallet")["Amount"].sum()

    wallets = set(income_df.index).union(set(expense_df.index))

    data = []

    for w in wallets:
        income = income_df.get(w, 0)
        expense = expense_df.get(w, 0)
        balance = income - expense

        data.append({
            "Wallet": w,
            "Income": income,
            "Expense": expense,
            "Balance": balance
        })

    wallet_df = pd.DataFrame(data)

    # ---------------- DISPLAY TABLE ----------------
    st.dataframe(wallet_df, use_container_width=True)

    # ---------------- VISUAL ----------------
    st.bar_chart(wallet_df.set_index("Wallet")["Balance"])

    # ---------------- ALERTS ----------------
    lowest_wallet = wallet_df.loc[wallet_df["Balance"].idxmin()]

    if lowest_wallet["Balance"] < 0:
        st.error(f"⚠️ {lowest_wallet['Wallet']} is in negative balance!")

    # ---------------- TOTAL ----------------
    total_balance = wallet_df["Balance"].sum()

    st.metric("Total Net Balance", f"Rs.{total_balance:,.0f}")