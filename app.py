# app.py
import streamlit as st
import os
from typing import List

# ----------------------
# 🔧 CONFIGURATION
# ----------------------
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# ----------------------
# 🎨 PAGE SETUP
# ----------------------
st.set_page_config(page_title="CAPNOW - Loan Detection Tool", layout="wide")
st.title("📄 CAPNOW Loan Detection Tool")
st.markdown("""
Upload one or more **PDF bank statements** to detect:
- 💸 **Large deposits** that may represent previous funding
- 🔁 **Repeated daily/weekly withdrawals** that may indicate outstanding loans

*This tool helps identify possible loan activity based on transaction patterns.*
""")

# ----------------------
# 📤 FILE UPLOAD
# ----------------------
uploaded_files = st.file_uploader(
    "Upload PDF Statements",
    type=["pdf"],
    accept_multiple_files=True,
    help=f"You can upload multiple statements (Max per file: {MAX_FILE_SIZE_MB}MB)"
)

# ----------------------
# 📋 FILE VALIDATION + STATUS
# ----------------------
def validate_file(file) -> List[str]:
    errors = []
    if file.size > MAX_FILE_SIZE_BYTES:
        errors.append("File too large")
    if not file.name.lower().endswith(".pdf"):
        errors.append("Unsupported format")
    return errors

if uploaded_files:
    st.subheader("📂 Uploaded Files")
    for file in uploaded_files:
        errors = validate_file(file)
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{file.name}** ({round(file.size / 1024, 1)} KB)")
        with col2:
            if errors:
                st.error(" ❌ ".join(errors))
            else:
                st.success("✅ Ready")

    st.info("Analysis and results will appear here in the next step.")

# ----------------------
# 📌 FOOTER
# ----------------------
st.markdown("""
---
Built by **Capnow** | Empowering smarter funding decisions
""")
