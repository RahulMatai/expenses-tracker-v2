import uuid #genrates Client ID
from decimal import Decimal
from datetime import date
import streamlit as st
import database as db
import pandas as pd

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="₹",
    layout="wide",
)


db.init_db()

# Session management — each browser tab gets unique session
# Persist session_id in URL so refresh doesn't lose data
if "session_id" not in st.query_params:
    new_id = str(uuid.uuid4())
    st.query_params["session_id"] = new_id

session_id = st.query_params["session_id"]
st.session_state.session_id = session_id

session_id = st.session_state.session_id

st.title("₹ Expense Tracker")
st.caption("Your personal expense tracker — data is private to your session.")

# Metrics
all_expenses = db.get_expenses(session_id=session_id)
total_all = sum(e["amount_rupees"] for e in all_expenses)
avg_all = total_all / len(all_expenses) if all_expenses else Decimal("0")

m1, m2, m3 = st.columns(3)
m1.metric("Total Spent", f"₹{total_all:,.2f}")
m2.metric("No. of Expenses", len(all_expenses))
m3.metric("Average Expense", f"₹{avg_all:,.2f}")

st.divider()

# Form
st.subheader("Add New Expense")

with st.form("add_expense_form", clear_on_submit=True):
    amount = st.text_input("Amount (₹)", placeholder="e.g. 250.00")
    category = st.selectbox("Category", [
        "Food & Dining", "Transport", "Shopping",
        "Entertainment", "Health & Medical",
        "Utilities & Bills", "Rent", "Education", "Other"
    ])
    description = st.text_input("Description", placeholder="e.g. Lunch at canteen")
    expense_date = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Add Expense")

if submitted:
    try:
        if not amount.strip():
            st.error("Please enter an amount.")
            st.stop()
        amount_decimal = Decimal(amount.strip().replace(",", ""))
    except Exception:
        st.error("Please enter a valid amount e.g. 250 or 49.99")
        st.stop()
    try:
        db.create_expense(
            client_id=str(uuid.uuid4()),
            amount=amount_decimal,
            category=category,
            description=description,
            date=expense_date.isoformat(),
            session_id=session_id,
        )
        st.success("Expense added successfully!")
        st.rerun()
    except ValueError as e:
        st.error(str(e))
        
st.divider()
st.subheader("Your Expenses")

col1, col2 = st.columns(2)

with col1:
    selected_category = st.selectbox("Filter by Category", 
        ["All", "Food & Dining", "Transport", "Shopping",
        "Entertainment", "Health & Medical",
        "Utilities & Bills", "Rent", "Education", "Other"])

with col2:
    sort_order = st.selectbox("Sort by Date", 
        ["Newest First", "Oldest First"])

expenses = db.get_expenses(
    session_id=session_id,
    category=selected_category,
    sort_by_date_desc=(sort_order == "Newest First")
)

if not expenses:
    st.info("No expenses yet. Add your first expense above!")
else:
    table_data = [{
        "Date": e["date"],
        "Category": e["category"],
        "Description": e["description"],
        "Amount (₹)": f"₹{e['amount_rupees']:,.2f}"
    } for e in expenses]

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)

    total = sum(e["amount_rupees"] for e in expenses)
    st.markdown(f"### Total: ₹{total:,.2f}")

    # Category summary
    st.subheader("Summary by Category")
    from collections import defaultdict
    cat_totals = defaultdict(Decimal)
    for e in expenses:
        cat_totals[e["category"]] += e["amount_rupees"]

    cat_df = pd.DataFrame([
        {"Category": cat, "Total (₹)": f"₹{amt:,.2f}"}
        for cat, amt in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
    ])
    st.dataframe(cat_df, use_container_width=True)