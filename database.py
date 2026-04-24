import os
from decimal import Decimal
from supabase import create_client, Client
from datetime import date as date_type

def get_supabase_client():
    try:
        import streamlit as st
        url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    except Exception:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)

supabase: Client = get_supabase_client()

def init_db():
    pass

def create_expense(client_id, amount, category, description, date, session_id):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if not category.strip():
        raise ValueError("Category is required.")
    if not date:
        raise ValueError("Date is required.")
    if date > date_type.today().isoformat():
        raise ValueError("Date cannot be in the future.")

    amount_paise = int(Decimal(str(amount)) * 100)

    try:
        supabase.table("expenses").insert({
            "client_id": client_id,
            "session_id": session_id,
            "amount_paise": amount_paise,
            "category": category.strip(),
            "description": description.strip(),
            "date": date,
        }).execute()
    except Exception as e:
        print("Error", e)

def get_expenses(session_id, category=None, sort_by_date_desc=True):
    query = supabase.table("expenses").select("*").eq("session_id", session_id)

    if category and category != "All":
        query = query.eq("category", category)

    if sort_by_date_desc:
        query = query.order("date", desc=True)
    else:
        query = query.order("date", desc=False)

    response = query.execute()

    result = []
    for row in response.data:
        row["amount_rupees"] = Decimal(row["amount_paise"]) / 100
        result.append(row)

    return result