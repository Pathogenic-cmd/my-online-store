import streamlit as st
import pandas as pd
from datetime import datetime
from supabase_config import init_supabase

supabase = init_supabase()

def load_data():
    orders = supabase.table("orders").select("*").execute().data
    payments = supabase.table("payment").select("*").execute().data
    order_items = supabase.table("order_items").select("*").execute().data
    products = supabase.table("products").select("*").execute().data
    categories = supabase.table("categories").select("*").execute().data

    return (
        pd.DataFrame(orders),
        pd.DataFrame(payments),
        pd.DataFrame(order_items),
        pd.DataFrame(products),
        pd.DataFrame(categories),
    )


def show_analytics():
    st.markdown(
        """
        <style>
        /* --- Analytics Dashboard Styling --- */
        .metric-card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 1.2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            text-align: center;
            transition: transform 0.2s ease;
        }
        .metric-card:hover {
            transform: scale(1.02);
        }
        .metric-title {
            font-size: 0.9rem;
            color: #6b7280;
            margin-bottom: 0.2rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        .metric-value {
            font-size: 1.6rem;
            font-weight: 700;
            color: #2563eb;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Analytics Dashboard")
    st.caption("Gain insights into store performance and sales trends.")

    orders_df, payments_df, items_df, products_df, categories_df = load_data()

    if orders_df.empty:
        st.warning("No data available yet. Add some orders first!")
        return

    # === METRICS ===
    total_revenue = payments_df["amount"].sum() if not payments_df.empty else 0
    total_orders = len(orders_df)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    # Card-like metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Revenue</div>
                <div class="metric-value">₵{total_revenue:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Orders</div>
                <div class="metric-value">{total_orders}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Avg Order Value</div>
                <div class="metric-value">₵{avg_order_value:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # === SALES BY STATUS ===
    st.subheader("🧾 Orders by Status")
    if "status" in orders_df.columns:
        status_counts = orders_df["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        st.bar_chart(status_counts.set_index("Status")["Count"])
    else:
        st.info("No order status data found.")

    # === TOP SELLING PRODUCTS ===
    if not items_df.empty and not products_df.empty:
        merged = items_df.merge(products_df, left_on="product_id", right_on="id", how="left")
        top_products = merged.groupby("name")["quantity"].sum().sort_values(ascending=False).head(5)
        st.markdown("### 🏆 Top Selling Products")
        st.bar_chart(top_products)
    else:
        st.info("No sales data available yet for top products.")

    # === MONTHLY SALES TREND ===
    if "created_at" in orders_df.columns:
        orders_df["created_at"] = pd.to_datetime(orders_df["created_at"], errors="coerce")
        monthly_sales = (
            orders_df.groupby(orders_df["created_at"].dt.to_period("M"))["total"]
            .sum()
            .rename_axis("Month")
            .reset_index()
        )
        monthly_sales["Month"] = monthly_sales["Month"].astype(str)
        st.markdown("### 📅 Monthly Sales Trend")
        st.line_chart(monthly_sales.set_index("Month")["total"])

    st.markdown("---")
    st.caption(f"🕒 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
