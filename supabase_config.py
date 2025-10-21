import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Missing SUPABASE_URL or SUPABASE_ANON_KEY in Streamlit Secrets.")

def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)
