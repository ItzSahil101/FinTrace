import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import re

# ==============================
# 🧠 AI INSIGHTS ENGINE (BASIC)
# ==============================
def show_ai_insights(df):

    st.subheader("🧠 AI Financial Insights")

    if len(df) == 0:
        st.info("No data available for AI analysis")
        return

    expense_df = df[df["Type"] == "Expense"]

    if len(expense_df) == 0:
        st.info("No expense data")
        return

    # ---------------- TOP SPENDING CATEGORY ----------------
    top_category = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(1)

    st.success(f"📊 Highest spending category: {top_category.index[0]} (Rs.{top_category.values[0]:,.0f})")

    # ---------------- SPENDING PATTERN ----------------
    avg_spend = expense_df["Amount"].mean()

    if avg_spend > 1000:
        st.warning("⚠️ Your average spending per transaction is high.")
    else:
        st.success("✅ Your spending per transaction is under control.")

    # ---------------- INCOME VS EXPENSE HEALTH ----------------
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()

    ratio = expense / income if income > 0 else 0

    if ratio > 0.8:
        st.error("🚨 You are spending more than 80% of your income!")
    elif ratio > 0.5:
        st.warning("⚠️ Moderate spending detected.")
    else:
        st.success("💰 Healthy financial balance.")


# ==============================
# 🔮 SPENDING PREDICTION (SIMPLE ML-LIKE TREND)
# ==============================
def show_spending_prediction(df):

    st.subheader("🔮 Spending Prediction")

    if len(df) < 5:
        st.info("Need more data for prediction (min 5 transactions)")
        return

    df_exp = df[df["Type"] == "Expense"].copy()

    if len(df_exp) == 0:
        st.info("No expense data")
        return

    # Convert date
    df_exp["Date"] = pd.to_datetime(df_exp["Date"])
    df_exp = df_exp.sort_values("Date")

    # daily grouping
    daily = df_exp.groupby("Date")["Amount"].sum().reset_index()

    if len(daily) < 3:
        st.info("Not enough daily data")
        return

    # Simple moving average prediction
    daily["MA3"] = daily["Amount"].rolling(3).mean()

    predicted = daily["MA3"].iloc[-1]

    if np.isnan(predicted):
        predicted = daily["Amount"].mean()

    st.metric("Predicted Next Expense", f"Rs.{predicted:,.0f}")

    st.info("📌 Based on your last spending trend (simple ML model)")


# ==============================
# 🏷 AUTO CATEGORY DETECTION
# ==============================
def show_auto_category_detection(df):

    st.subheader("🏷 Auto Category Detection")

    if len(df) == 0:
        st.info("No data")
        return

    if "Description" not in df.columns:
        st.warning("Description column missing")
        return

    text_data = df["Description"].dropna().astype(str)

    words = []

    for desc in text_data:
        cleaned = re.sub(r"[^a-zA-Z ]", "", desc.lower())
        words.extend(cleaned.split())

    common_words = Counter(words).most_common(10)

    st.write("📊 Frequent keywords in your spending:")

    for word, count in common_words:
        st.write(f"• {word} → {count} times")


# ==============================
# 💡 SMART RECOMMENDATIONS ENGINE
# ==============================
def show_smart_recommendations(df):

    st.subheader("💡 Smart Recommendations")

    if len(df) == 0:
        st.info("No data available")
        return

    expense_df = df[df["Type"] == "Expense"]

    if len(expense_df) == 0:
        return

    # category analysis
    cat_sum = expense_df.groupby("Category")["Amount"].sum()

    highest = cat_sum.idxmax()
    lowest = cat_sum.idxmin()

    st.info(f"💸 You are spending most on: {highest}")

    st.success(f"📉 Try reducing spending on: {highest}")

    # wallet analysis if exists
    if "Wallet" in df.columns:

        wallet_sum = expense_df.groupby("Wallet")["Amount"].sum()

        worst_wallet = wallet_sum.idxmax()

        st.warning(f"⚠️ Highest spending wallet: {worst_wallet}")

    # saving suggestion
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()

    if income > 0:
        save_rate = ((income - expense) / income) * 100

        if save_rate < 20:
            st.error("🚨 Low savings rate — try reducing expenses!")
        elif save_rate < 40:
            st.warning("⚠️ Moderate savings — can improve")
        else:
            st.success("💰 Great savings behavior!")


# ==============================
# 🚀 MASTER FUNCTION (USE THIS IN APP)
# ==============================
def run_phase3(df):

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🧠 AI Insights", "🔮 Prediction", "🏷 Auto Category", "💡 Recommendations"]
    )

    with tab1:
        show_ai_insights(df)

    with tab2:
        show_spending_prediction(df)

    with tab3:
        show_auto_category_detection(df)

    with tab4:
        show_smart_recommendations(df)