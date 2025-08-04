# app.py

import streamlit as st
import pandas as pd
from utils import parser

st.set_page_config(page_title="CapNow Loan Detector", layout="wide")
st.title("💰 CapNow Loan Detector App")
st.markdown("""
Upload multiple bank statement PDFs. The system will:
- ✅ Detect **large deposits** (potential funding)
- ✅ Detect **repeated withdrawals** (potential loans out)
""")

uploaded_files = st.file_uploader("Upload PDF Statements", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    all_transactions = []
    large_deposits = []
    repeated_withdrawals = []

    for file in uploaded_files:
        with st.spinner(f"Processing {file.name}..."):
            text = parser.extract_text_from_pdf(file)
            transactions = parser.extract_transactions(text)
            deposits = parser.detect_large_deposits(transactions)
            withdrawals = parser.detect_repeated_withdrawals(transactions)

            all_transactions.extend(transactions)
            large_deposits.extend(deposits)
            repeated_withdrawals.extend(withdrawals)

    st.subheader("📄 All Parsed Transactions")
    st.dataframe(pd.DataFrame(all_transactions))

    st.subheader("💸 Large Deposits Detected")
    if large_deposits:
        st.success(f"{len(large_deposits)} potential fundings found.")
        st.dataframe(pd.DataFrame(large_deposits))
    else:
        st.info("No large deposits detected above threshold.")

    st.subheader("📉 Repeated Withdrawals Detected")
    if repeated_withdrawals:
        st.warning(f"{len(repeated_withdrawals)} possible loans out detected.")
        st.dataframe(pd.DataFrame(repeated_withdrawals))
    else:
        st.info("No repeated withdrawals detected.")
