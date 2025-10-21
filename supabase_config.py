import os
from supabase import create_client, Client

# No dotenv needed on Streamlit Cloud
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Missing SUPABASE_URL or SUPABASE_ANON_KEY. Did you add them in Streamlit Secrets?")

def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Optional: create a global client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
