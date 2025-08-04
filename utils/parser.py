# utils/parser.py

import pdfplumber
import fitz  # PyMuPDF
import re
from datetime import datetime

# 1. Extract text using pdfplumber, fallback to PyMuPDF
def extract_text_from_pdf(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            if text:
                return text
    except Exception:
        pass  # fallback

    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        return text
    except Exception as e:
        return ""

# 2. Extract transactions (assumes a format like: 01/01/2024 - Description - $1,000.00)
def extract_transactions(text):
    lines = text.split("\n")
    pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4}).*?(-?\$?\(?\d{1,3}(,\d{3})*(\.\d{2})?\)?$)")
    
    transactions = []
    for line in lines:
        match = pattern.search(line)
        if match:
            date_str, amount_str = match.group(1), match.group(2)
            try:
                amount = float(re.sub(r"[^\d.-]", "", amount_str))
                date = datetime.strptime(date_str, "%m/%d/%Y")
                transactions.append({"date": date, "amount": amount, "description": line})
            except:
                continue
    return transactions

# 3. Detect large deposits (e.g., $3,000+)
def detect_large_deposits(transactions, threshold=3000):
    return [txn for txn in transactions if txn['amount'] > threshold]

# 4. Detect repeated withdrawals (same amount withdrawn repeatedly)
def detect_repeated_withdrawals(transactions, min_occurrences=3):
    withdrawals = [t for t in transactions if t['amount'] < 0]
    amount_map = {}

    for txn in withdrawals:
        amt = round(abs(txn['amount']), 2)
        if amt not in amount_map:
            amount_map[amt] = []
        amount_map[amt].append(txn)

    result = []
    for amt, txns in amount_map.items():
        if len(txns) >= min_occurrences:
            result.extend(txns)

    return result
