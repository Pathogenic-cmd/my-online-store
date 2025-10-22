import streamlit as st
from supabase_config import init_supabase
from auth_helpers import signup, login, logout, get_current_user
from checkout import show_checkout
from pathlib import Path



# Connect to Supabase
supabase = init_supabase()

st.set_page_config(page_title="My E-Commerce Concept")


# --- Custom Background ---
background_image = "https://rflyaqswtuuoukmvfhfc.supabase.co/storage/v1/object/public/product-mages/cyber-monday-shopping-sales.jpg"

page_bg = f"""
<style>
/* Full-page background image */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
    background: url("{background_image}") no-repeat center center fixed;
    background-size: cover;
    position: relative;
}}

/* Dark translucent overlay behind all content */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5); /* darkness level */
    z-index: 0;
}}

/* Ensure all main content sits above the overlay */
[data-testid="stAppViewContainer"] > div {{
    position: relative;
    z-index: 1;
}}

/* Transparent header */
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

/* DARK SIDEBAR */
[data-testid="stSidebar"] > div:first-child {{
    background-color: rgba(20, 20, 20, 0.85); /* dark translucent background */
    color: white !important;
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    padding-top: 1rem; /* small top spacing */
}}

/* Sidebar text color */
[data-testid="stSidebar"] * {{
    color: #f0f0f0 !important;
}}

/* Sidebar headings (e.g., 'Account', 'Filter') */
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {{
    color: #ffffff !important;
}}

/* 🧭 Fix sidebar collapse/expand arrow position */
[data-testid="stSidebarCollapseButton"] {{
    margin-top: 0 !important;
    top: 8px !important; /* adjust 5–15px if needed */
    position: relative !important;
    z-index: 2;
}}

/* ✨ Optional: smooth sidebar open/close animation */
[data-testid="stSidebar"] {{
    transition: all 0.3s ease-in-out;
}}


</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)




st.title("E-Commerce Store Concept")




st.markdown('<a name="top"></a>', unsafe_allow_html=True)

user = get_current_user()

# 🧱 SIDEBAR AUTH SECTION
with st.sidebar:
    st.markdown("## 🔐 Account")

    if not user:
        with st.expander("Login", expanded=False):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pw")
            if st.button("Login"):
                res = login(email, password)
                if res.get("error"):
                    st.error(res["error"])
                else:
                    st.success("✅ Logged in successfully!")
                    st.rerun()

        with st.expander("Create Account"):
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_pw")
            full_name = st.text_input("Full Name")
            if st.button("Sign Up"):
                res = signup(new_email, new_password, full_name)
                if res.get("error"):
                    st.error(res["error"])
                else:
                    st.success("🎉 Account created! Please check your email to verify.")

    else:
        from datetime import datetime, timezone

        try:
            # ✅ Always fetch the freshest profile data
            profile_res = supabase.table("users").select("*").eq("id", user.id).execute()
            profile = profile_res.data[0] if profile_res.data else None

            if not profile:
                # Fallback if user table entry is missing
                st.warning("Profile not found. Creating a new one.")
                supabase.table("users").insert({
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.user_metadata.get("full_name", user.email.split("@")[0]),
                    "last_login": datetime.now(timezone.utc).isoformat()
                }).execute()
                profile = {"full_name": user.email.split("@")[0], "last_login": None}

            full_name = profile.get("full_name") or user.email.split("@")[0]
            last_login = profile.get("last_login")

            # ✅ Check for first login
            if not last_login:
                st.success(f"🎉 Welcome, {full_name}! Glad to have you here for the first time.")
            else:
                st.success(f"👋 Welcome back, {full_name}!")

            # ✅ Update last_login *after* greeting, every time
            now = datetime.now(timezone.utc).isoformat()
            update_res = supabase.table("users").update({"last_login": now}).eq("id", user.id).execute()

            if update_res.data:
                updated_time = update_res.data[0].get("last_login")
                if updated_time:
                    st.caption(f"🕒 Last login updated to: {updated_time[:19].replace('T', ' ')} UTC")

        except Exception as e:
            st.error(f"⚠️ Error fetching or updating profile: {e}")
            st.success(f"Welcome back, {user.email} 👋")

        if st.button("Logout"):
            logout()
            st.rerun()



page = st.sidebar.selectbox("Navigate", ["Shop", "Analytics","About"])

if page == "Analytics":
    from analytics import show_analytics
    show_analytics()
    st.stop()

if page == "About":
    from about import show_about
    show_about()
    st.stop()





# Fetch categories
categories_response = supabase.table("categories").select("*").execute()
categories = categories_response.data

# Fetch products
products_response = supabase.table("products").select("*").execute()
products = products_response.data


# Sidebar filter
category_names = ["All"] + [c["name"] for c in categories]
selected_category = st.sidebar.selectbox("🗂️ Filter by Category", category_names)

query = st.sidebar.text_input("🔍 Search products")



# -----------------------------------------
# 🛒 PRODUCT FILTERING + CART + SIDEBAR VIEW
# -----------------------------------------

# Keep a master copy of all products before filtering
if "products_all" not in st.session_state:
    st.session_state.products_all = products.copy()

# --- Filter Products Based on Category ---
if selected_category != "All":
    selected_cat = next((c for c in categories if c["name"] == selected_category), None)
    if selected_cat:
        products = [p for p in products if p.get("category_id") == selected_cat["id"]]

# --- Filter by search query ---
if query:
    q = query.lower()
    products = [
        p for p in products
        if q in (p.get("name", "").lower() + p.get("description", "").lower())
    ]

# --- Initialize cart in session_state ---
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {product_id: quantity}

# --- SIDEBAR CART HEADER ---
total_quantity = sum(st.session_state.cart.values())
st.sidebar.markdown(f"### 🛒 Cart: {total_quantity} item(s)")

# --- DISPLAY PRODUCTS ---
num_products = len(products)
st.markdown(f"### {selected_category} ({num_products} Found)")

if not products:
    st.warning("No products found.")
else:
    cols = st.columns(3)
    fallback_img = "https://via.placeholder.com/300x200.png?text=Image+Unavailable"

    for i, product in enumerate(products):
        with cols[i % 3]:
            img_url = product.get("image_url", "")
            try:
                st.image(img_url or fallback_img, use_container_width=True)
            except Exception:
                st.image(fallback_img, use_container_width=True)

            st.subheader(product.get("name", "Unnamed"))
            description = product.get("description", "").strip()
            if description:
                st.write(description)

            price = product.get("price") or 0
            st.write(f"**₵ {price:,.2f}**")

            if product.get("attribution"):
                st.caption(product["attribution"], unsafe_allow_html=True)


            # --- ADD TO CART BUTTON ---
            pid = str(product["id"])
            if st.button(f"Add to Cart 🛒", key=f"add-{pid}-{i}"):
                st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
                st.rerun()  # 🔁 rerun to immediately refresh sidebar count

# --- SIDEBAR CART VIEW ---
with st.sidebar.expander("🛍️ View Cart", expanded=False):
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        st.markdown("#### 🧾 Cart Summary")

        for pid, qty in st.session_state.cart.items():
            # ✅ Lookup product in the master list (not filtered list)
            product = next(
                (p for p in st.session_state.products_all if str(p.get("id")) == pid),
                None
            )

            if product:
                name = product.get("name", "Unnamed")
                price = product.get("price", 0)
                img_url = product.get("image_url", "https://via.placeholder.com/80x80.png?text=No+Image")

                cols = st.columns([1, 2])
                with cols[0]:
                    st.image(img_url, use_container_width=True)
                with cols[1]:
                    st.markdown(f"**{name}**")
                    st.write(f"Qty: {qty}")
                    st.write(f"₵ {price:,.2f}")
            else:
                st.write(f"Product ID: {pid} — Quantity: {qty}")

        st.divider()
        st.markdown(f"**🧮 Total Items:** {total_quantity}")

        if st.button("🗑️ Clear Cart"):
            st.session_state.cart.clear()
            st.rerun()


        show_checkout(st.session_state.cart, st.session_state.products_all)




#Banner


# ---- BANNER (at bottom) ----
st.markdown("""
    <style>
        /* Smooth scrolling */
        html {
            scroll-behavior: smooth;
        }

        /* Banner container */
        .banner {
            position: relative;
            text-align: center;
            overflow: hidden;
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.25);
            margin-top: 4rem;
        }

        /* Image styling + slow zoom animation */
        .banner img {
            width: 100%;
            height: auto;
            border-radius: 16px;
            animation: zoom 10s ease-in-out infinite alternate;
        }

        /* Overlay text container */
        .banner-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            text-shadow: 0 2px 8px rgba(0,0,0,0.7);
            background: rgba(0,0,0,0.45);
            padding: 1rem 2.5rem;
            border-radius: 12px;
            animation: fadeInUp 2s ease-in-out;
        }

        /* Animations */
        @keyframes fadeInUp {
            from {opacity: 0; transform: translate(-50%, -40%);}
            to {opacity: 1; transform: translate(-50%, -50%);}
        }

        @keyframes zoom {
            from {transform: scale(1);}
            to {transform: scale(1.05);}
        }

        /* Typography */
        .banner-text h1 {
            font-size: clamp(1.5rem, 4vw, 3rem);
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .banner-text p {
            font-size: clamp(1rem, 2vw, 1.25rem);
            margin: 0;
        }

        .shop-btn {
            display: inline-block;
            margin-top: 1rem;
            padding: 0.6rem 1.5rem;
            background: #ff4b4b;
            color: white;
            border-radius: 8px;
            font-weight: 600;
            text-decoration: none;
            transition: background 0.3s ease;
        }

        .shop-btn:hover {
            background: #ff2e2e;
        }
    </style>

    <div class="banner">
        <img src="https://rflyaqswtuuoukmvfhfc.supabase.co/storage/v1/object/public/product-mages/client-shopping-fashionable-clothes.jpg" alt="banner">
        <div class="banner-text">
            <h1>Discover Your Style</h1>
            <p>Trendy collections tailored just for you</p>
            <a href="#top" class="shop-btn">Start Shopping</a>
        </div>
    </div>
""", unsafe_allow_html=True)




