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

    st.subheader("📊 Financial Overview")

    if len(df) == 0:
        st.info("No transactions found.")
        return

    # =========================
    # BASIC CALCULATIONS
    # =========================

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()

    if income <= 0:
        st.warning("Add income to calculate insights.")
        return

    savings_rate = max(0, ((income - expense) / income) * 100)

    # Budget + Debt (safe defaults)
    budget = st.session_state.get("monthly_budget", 20000)
    debt = st.session_state.get("total_debt", 0)

    expense_ratio = (expense / income) * 100
    debt_ratio = (debt / income) * 100

    # =========================
    # SCORES
    # =========================

    savings_score = min(savings_rate, 100)
    spending_score = max(0, 100 - expense_ratio)

    budget_usage = (expense / budget) * 100 if budget > 0 else 0
    budget_score = max(0, 100 - abs(100 - budget_usage)) if budget > 0 else 70

    debt_score = max(0, 100 - debt_ratio) if income > 0 else 100

    financial_health = round(
        savings_score * 0.35 +
        spending_score * 0.25 +
        budget_score * 0.25 +
        debt_score * 0.15
    )

    # =========================
    # UI: 50 / 50 LAYOUT
    # =========================

    col1, col2 = st.columns(2)

    # -------------------------
    # LEFT: SAVINGS RATE
    # -------------------------
    with col1:

        st.subheader("💰 Savings Rate")

        st.metric(
            "Rate",
            f"{savings_rate:.1f}%"
        )

        st.progress(min(savings_rate / 100, 1.0))

        st.caption(f"Income: Rs.{income:,.0f} | Expense: Rs.{expense:,.0f}")

    # -------------------------
    # RIGHT: FINANCIAL HEALTH
    # -------------------------
    with col2:

        st.subheader("🏥 Financial Health")

        st.metric(
            "Score",
            f"{financial_health}/100"
        )

        st.progress(financial_health / 100)

        # =========================
        # COLOR BADGES
        # =========================

        if financial_health >= 80:
            st.success("🟢 Excellent Financial Health")

        elif financial_health >= 60:
            st.info("🔵 Good Financial Health")

        elif financial_health >= 40:
            st.warning("🟠 Fair Financial Health")

        else:
            st.error("🔴 Poor Financial Health")

        # extra insight
        st.caption(
            f"Savings:{savings_score:.0f} | Spending:{spending_score:.0f} | Budget:{budget_score:.0f} | Debt:{debt_score:.0f}"
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