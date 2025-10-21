# checkout.py
import streamlit as st
from supabase_config import init_supabase
from auth_helpers import get_current_user

supabase = init_supabase()

def show_checkout(cart, products_all):
    """Handles checkout, authentication, order creation, and payment."""
    st.sidebar.divider()
    st.sidebar.subheader("💳 Checkout")

    user = get_current_user()

    # 🛒 Empty cart
    if not cart:
        st.sidebar.info("Your cart is empty. Add some items to continue.")
        return

    # 🚫 Require login before payment
    if not user:
        st.sidebar.warning("Please **log in or create an account** from the sidebar before making a payment.")
        return

    # 🧮 Compute total
    total_price = 0
    for pid, qty in cart.items():
        product = next(
            (p for p in products_all if str(p["id"]) == pid),
            None
        )
        if product:
            total_price += (product["price"] or 0) * qty

    st.sidebar.write(f"**🧾 Total Amount:** ₵ {total_price:,.2f}")

    # 💰 Payment method selection
    payment_method = st.sidebar.selectbox("Select Payment Method", ["Card", "Cash", "Mobile Money"])
    confirm_payment = st.sidebar.button("✅ Confirm & Pay")

    if confirm_payment:
        try:
            # 1️⃣ Create an order
            order_response = supabase.table("orders").insert({
                "user_id": user.id,
                "total": total_price,
                "status": "completed",
                "payment_status": "paid"
            }).execute()
            order_id = order_response.data[0]["id"]

            # 2️⃣ Add items to order
            for pid, qty in cart.items():
                product = next(
                    (p for p in products_all if str(p["id"]) == pid),
                    None
                )
                if product:
                    price = product["price"] or 0
                    subtotal = price * qty
                    supabase.table("order_items").insert({
                        "order_id": order_id,
                        "product_id": product["id"],
                        "quantity": qty,
                        "price": price,
                        "subtotal": subtotal
                    }).execute()

            # 3️⃣ Record payment
            supabase.table("payment").insert({
                "order_id": order_id,
                "amount": total_price,
                "method": payment_method,
                "status": "paid",
                "transaction_ref": f"TX-{order_id}-{user.id[:6]}"
            }).execute()

            # 4️⃣ Clear cart
            cart.clear()
            st.sidebar.success("🎉 Payment successful! Your order has been placed.")
            st.rerun()

        except Exception as e:
            st.sidebar.error(f"❌ Error processing payment: {e}")
