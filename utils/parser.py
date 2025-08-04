# parser.py

import fitz  # PyMuPDF
import re
from typing import List, Dict

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from PDF using PyMuPDF."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_transactions(text: str) -> List[Dict[str, str]]:
    """Extract basic transactions from text. Placeholder for smarter extraction."""
    # Placeholder logic: You should replace this with actual line-by-line extraction
    lines = text.split('\n')
    transactions = []
    for line in lines:
        if re.search(r'\d{2}/\d{2}/\d{4}', line):  # Looks for date format
            transactions.append({"raw": line})
    return transactions

def detect_large_deposits(transactions: List[Dict[str, str]], threshold: float = 5000.0) -> List[Dict[str, str]]:
    """Identify large deposits."""
    large = []
    for tx in transactions:
        if 'deposit' in tx['raw'].lower():
            match = re.search(r'\$?([\d,]+\.\d{2})', tx['raw'])
            if match:
                amount = float(match.group(1).replace(',', ''))
                if amount >= threshold:
                    tx['amount'] = amount
                    large.append(tx)
    return large

def detect_repeated_withdrawals(transactions: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Detect repeated withdrawals by amount and frequency (daily or weekly)."""
    amount_counts = {}
    for tx in transactions:
        if 'withdrawal' in tx['raw'].lower():
            match = re.search(r'\$?([\d,]+\.\d{2})', tx['raw'])
            if match:
                amount = match.group(1)
                amount_counts[amount] = amount_counts.get(amount, 0) + 1

    repeated = [amount for amount, count in amount_counts.items() if count >= 4]
    flagged = []
    for tx in transactions:
        for amt in repeated:
            if amt in tx['raw']:
                tx['amount'] = amt
                flagged.append(tx)
                break
    return flagged

