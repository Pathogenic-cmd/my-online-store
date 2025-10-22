import streamlit as st
from supabase_config import init_supabase
from supabase_auth.errors import AuthApiError


supabase = init_supabase()

def signup(email: str, password: str, full_name: str = None):
    """Sign up a user — profile is created automatically via Supabase trigger."""
    try:
        # Attempt to create the auth user
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"full_name": full_name or "New User"}  # passed into user_metadata
            }
        })
    except Exception as e:
        return {"error": f"Signup request failed: {e}"}

    # Handle Supabase error response
    if hasattr(res, "error") and res.error:
        return {"error": res.error.message}

    user = getattr(res, "user", None)
    if not user:
        return {"error": "User creation failed. Check email confirmation or RLS policies."}

    # ✅ The trigger now creates the `users` row in the database automatically.
    # We no longer call upsert() here.

    # Optional: log event or display message
    import streamlit as st
    st.success("🎉 Account created! Please verify your email before logging in.")
    st.balloons()

    return {"user": user}



def login(email: str, password: str):
    """Sign in using password (returns session / user)."""
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = getattr(res, "user", None)
        session = getattr(res, "session", None)
        if not user:
            return {"error": "Login failed. Please try again."}

        # ✅ ensure user profile exists
        supabase.table("users").upsert({
            "id": user.id,
            "email": user.email,
            "full_name": user.user_metadata.get("full_name", "User")
        }).execute()

        return {"session": session, "user": user}

    except AuthApiError as e:
        # Handle invalid login credentials
        if "Invalid login credentials" in str(e):
            return {"error": "Incorrect email or password. Please try again."}
        else:
            return {"error": "Unable to log in. Please check your connection or try again later."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}



def logout():
    """Sign out the current user."""
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state.pop("user", None)


def get_current_user():
    """Return the current user from Streamlit session_state or Supabase."""
    if "user" in st.session_state:
        return st.session_state["user"]

    try:
        res = supabase.auth.get_user()
        user = getattr(res, "user", None)
        if user:
            st.session_state["user"] = user
            return user
    except Exception:
        pass
    return None
