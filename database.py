import os
from decimal import Decimal
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import date as date_type
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def init_db():
    pass  # Supabase table already created via SQL editor

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
        result = supabase.table("expenses").insert({
            "client_id": client_id,
            "session_id": session_id,
            "amount_paise": amount_paise,
            "category": category.strip(),
            "description": description.strip(),
            "date": date,
        }).execute()
        print(result)
    except Exception as e:
        print("Error",e)# duplicate client_id — idempotent, safe to ignore
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
