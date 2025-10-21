# 🛍️ Streamlit E-Commerce Store (Supabase + Python)

A modern e-commerce concept web app built with **Streamlit**, **Supabase**, and **Python** — featuring authentication, product browsing, checkout simulation, and analytics.  
This project demonstrates how to connect Streamlit with a cloud database (Supabase) and manage user accounts, orders, and analytics in real time.

---

## 🚀 Features

- 🔐 **User Authentication** (Signup, Login, Logout) with Supabase Auth  
- 🛒 **Product Catalog** — Filter and search across categories  
- 💳 **Checkout Flow** — Simulated purchase & order tracking  
- 📊 **Analytics Dashboard** — Sales overview and user stats  
- 🎨 **Custom Styling** — Background images, dark sidebar, and transparent headers  
- 📧 **Email Verification** — Works with Supabase email confirmations  
- ⚙️ **RLS-Ready** — Configurable row-level security policies for user data safety  

---

## 🧱 Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend | [Streamlit](https://streamlit.io) |
| Backend | [Supabase](https://supabase.com) |
| Database | PostgreSQL (managed by Supabase) |
| Authentication | Supabase Auth |
| Language | Python 3.10+ |

---

## 🧩 Folder Structure

```
ecommerce/
│
├── main.py                # App entry point
├── about.py               # About page
├── checkout.py            # Checkout page and logic
├── analytics.py           # Analytics dashboard
├── auth_helpers.py        # Auth helpers (login/signup/logout)
├── supabase_config.py     # Supabase initialization
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not committed)
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Pathogenic-cmd/my-online-store.git
cd streamlit-ecommerce
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure environment variables

Create a `.env` file in the root directory with:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key   # optional, for backend logs
RESEND_API_KEY=your-resend-key          # optional, for emails
```

> ⚠️ Never commit `.env` to GitHub. Streamlit Cloud supports environment secrets directly in the dashboard.

### 4️⃣ Enable Supabase Email Auth

In your Supabase dashboard:
- Go to **Authentication → Providers → Email**
- Enable **Email signups** and **Confirm email** (recommended)
- Optionally configure your SMTP provider (Resend, SendGrid, etc.)

### 5️⃣ Configure Row-Level Security (optional but recommended)

Enable **RLS** on user-related tables and add these basic policies:

```sql
-- Users can view/update only their own profile
create policy "Users can view their own profile"
on users for select using (auth.uid() = id);
create policy "Users can update their own profile"
on users for update using (auth.uid() = id);
```

### 6️⃣ Run the app

```bash
streamlit run main.py
```

Then visit:
👉 http://localhost:8501

---

## 🌄 Customization

You can easily change:
- **Background image** — in `main.py`:
  ```python
  background_image = "https://your-bucket-url/background.jpg"
  ```
- **Theme colors** — Streamlit supports [theming via config](https://docs.streamlit.io/library/advanced-features/theming).
- **Email templates** — customize in Supabase under *Auth → Templates*.

---

## 🧠 Future Improvements

- Stripe or Paystack integration for real payments  
- Inventory management dashboard  
- Real-time chat or customer support  
- Product reviews and ratings  
- Admin panel for managing products and orders  

---

## 🧑‍💻 Author

**Daniel Kofi Debrah Awuma**  
Passionate Python developer building modern cloud-connected apps.

---

## 🪪 License

MIT License — free to use, modify, and distribute.

---

## ⭐ Acknowledgments

- [Streamlit](https://streamlit.io) for the fantastic open-source framework  
- [Supabase](https://supabase.com) for the full-stack backend tools  
