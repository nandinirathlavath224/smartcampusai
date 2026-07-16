import streamlit as st
import time
from utils.auth import authenticate_user
from utils.helpers import load_css

def show_login() -> None:
    """
    Renders a premium login page.
    Includes input validations, custom CSS styled cards, error feedback,
    and handles authenticated session routing.
    """
    load_css()
    
    # Custom styling overrides to construct the auth card container
    st.markdown("""
    <style>
    [data-testid="stForm"] {
        max-width: 440px;
        margin: 0 auto;
        background: rgba(30, 41, 59, 0.55) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 24px !important;
        padding: 2.25rem !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3) !important;
    }
    /* Style input elements to match premium aesthetic */
    div[data-baseweb="input"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #6366f1 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header Branding
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem; margin-bottom: 1.5rem;">
        <div style="font-size: 2.75rem; margin-bottom: 0.5rem;">🎓</div>
        <h2 style="font-weight: 800; color: #f8fafc; margin: 0; background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">SmartCampusAI</h2>
        <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">Premium College AI Student Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Student Email", placeholder="e.g. student@university.edu")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        remember_me = st.checkbox("Remember Session", value=True)
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("Log In")
        
    # Redirect switcher
    st.markdown("<div style='text-align: center; margin-top: 1.5rem;'>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button("Register an Account 📝", key="switch_to_register"):
            st.session_state.page = "Register"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process login submission
    if submit_btn:
        if not email or not password:
            st.error("⚠️ All fields are required. Please fill in both email and password.")
            return
            
        user, msg = authenticate_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.session_state.remember_me = remember_me
            st.session_state.page = "Dashboard"
            st.success(f"🎉 {msg} Welcome back, {user['name']}!")
            time.sleep(0.8)
            st.rerun()
        else:
            st.error(f"❌ {msg}")

if __name__ == "__main__":
    show_login()
