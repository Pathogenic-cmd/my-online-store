from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

def init_supabase() -> Client:
    assert SUPABASE_URL and SUPABASE_KEY, "Missing SUPABASE_URL or SUPABASE_KEY"
    return create_client(SUPABASE_URL, SUPABASE_KEY)



supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# Example: update the product with id = 1
product_id = 4  # change this to the actual product id
new_image_url = "https://rflyaqswtuuoukmvfhfc.supabase.co/storage/v1/object/public/product-mages/2150170582.jpg"
response = supabase.table("products").update({
    "image_url": new_image_url
}).eq("id", product_id).execute()

print("✅ Updated:", response)
