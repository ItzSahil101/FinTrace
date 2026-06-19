import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF

# =========================
# 🎯 FINANCIAL GOALS
# =========================
def financial_goals(df):

    st.subheader("🎯 Financial Goals")

    # FIX: correct session_state key
    if "goal" not in st.session_state:
        st.session_state.goal = 50000

    goal = st.number_input(
        "Set Monthly Savings Goal",
        min_value=1000,
        value=st.session_state.goal,
        key="goal_input"   # FIX: prevent duplicate widget error
    )

    st.session_state.goal = goal

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    savings = income - expense

    progress = min(savings / goal, 1.0)

    st.progress(progress)

    st.write(f"Saved: Rs.{savings:,.0f} / Rs.{goal:,.0f}")

    if savings >= goal:
        st.success("🎉 Goal Achieved!")
    else:
        st.info("Keep going 💪")


# =========================
# 🚨 EMERGENCY FUND TRACKER
# =========================
def emergency_fund(df):

    st.subheader("🚨 Emergency Fund Tracker")

    if len(df) == 0:
        st.info("No data available")
        return

    monthly_expense = df[df["Type"] == "Expense"]["Amount"].sum()

    recommended = monthly_expense * 3  # 3 months rule

    income = df[df["Type"] == "Income"]["Amount"].sum()
    current_savings = income - monthly_expense

    progress = min(current_savings / recommended, 1.0) if recommended > 0 else 0

    st.progress(progress)

    st.write(f"Recommended: Rs.{recommended:,.0f}")
    st.write(f"Current: Rs.{current_savings:,.0f}")

    if current_savings < recommended:
        st.warning("Emergency fund is not enough ⚠️")
    else:
        st.success("Emergency fund is healthy ✅")


# =========================
# 🔁 RECURRING TRANSACTIONS
# =========================
def recurring_transactions(df):

    st.subheader("🔁 Recurring Transactions Tracker")

    if len(df) == 0:
        st.info("No data available")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    recurring = df.groupby(["Category", "Amount"]).size().reset_index(name="Count")

    recurring = recurring[recurring["Count"] > 1]

    if len(recurring) == 0:
        st.info("No recurring transactions found")
        return

    st.dataframe(recurring, use_container_width=True)


# =========================
# 📄 PDF REPORT EXPORT
# =========================
def export_pdf(df):

    st.subheader("📄 Export Monthly Report (PDF)")

    if st.button("Generate PDF", key="pdf_btn"):

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        income = df[df["Type"] == "Income"]["Amount"].sum()
        expense = df[df["Type"] == "Expense"]["Amount"].sum()
        balance = income - expense

        pdf.cell(200, 10, txt="FinTrace Pro Monthly Report", ln=True)
        pdf.cell(200, 10, txt=f"Income: {income}", ln=True)
        pdf.cell(200, 10, txt=f"Expense: {expense}", ln=True)
        pdf.cell(200, 10, txt=f"Balance: {balance}", ln=True)

        file_path = "report.pdf"
        pdf.output(file_path)

        with open(file_path, "rb") as f:
            st.download_button(
                "⬇ Download PDF",
                f,
                file_name="report.pdf",
                key="pdf_download"
            )


# =========================
# 📊 MONTHLY REPORTS
# =========================
def monthly_reports(df):

    st.subheader("📊 Monthly Reports")

    if len(df) == 0:
        st.info("No data")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    current_month = datetime.now().month

    month_df = df[df["Date"].dt.month == current_month]

    income = month_df[month_df["Type"] == "Income"]["Amount"].sum()
    expense = month_df[month_df["Type"] == "Expense"]["Amount"].sum()

    st.metric("Monthly Income", f"Rs.{income:,.0f}")
    st.metric("Monthly Expense", f"Rs.{expense:,.0f}")
    st.metric("Monthly Savings", f"Rs.{income - expense:,.0f}")


# =========================
# 🚀 MAIN RUNNER
# =========================
def run_phase2(df):

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Goals",
        "🚨 Emergency Fund",
        "🔁 Recurring",
        "📄 PDF Export",
        "📊 Monthly Reports"
    ])

    with tab1:
        financial_goals(df)

    with tab2:
        emergency_fund(df)

    with tab3:
        recurring_transactions(df)

    with tab4:
        export_pdf(df)

    with tab5:
        monthly_reports(df)