import streamlit as st
import time
from utils.auth import register_user
from utils.helpers import load_css

def show_register() -> None:
    """
    Renders the student registration page.
    Implements validation rules, password matching, strength validations,
    and handles redirect prompts back to login.
    """
    load_css()
    
    # Custom form styling matching the dashboard aesthetic
    st.markdown("""
    <style>
    [data-testid="stForm"] {
        max-width: 500px;
        margin: 0 auto;
        background: rgba(30, 41, 59, 0.55) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 24px !important;
        padding: 2.25rem !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3) !important;
    }
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header Branding
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem; margin-bottom: 1.5rem;">
        <div style="font-size: 2.75rem; margin-bottom: 0.5rem;">📝</div>
        <h2 style="font-weight: 800; color: #f8fafc; margin: 0; background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Create Student Account</h2>
        <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">Join the SmartCampusAI platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_form", clear_on_submit=False):
        name = st.text_input("Full Name", placeholder="e.g. John Doe")
        email = st.text_input("Student Email", placeholder="e.g. johndoe@university.edu")
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password", type="password", placeholder="••••••••")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")
            
        col3, col4 = st.columns(2)
        with col3:
            department = st.selectbox(
                "Department",
                ["Computer Science", "Information Technology", "Electrical Engineering", 
                 "Mechanical Engineering", "Civil Engineering", "Business Administration", "Other"]
            )
        with col4:
            year = st.selectbox("Current Year", ["1st", "2nd", "3rd", "4th", "Postgraduate"])
            
        student_id = st.text_input("Student ID Number", placeholder="e.g. STU102938")
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("Register Now")
        
    # Redirect switcher
    st.markdown("<div style='text-align: center; margin-top: 1.5rem;'>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button("Already have an account? Log In Key", key="switch_to_login"):
            st.session_state.page = "Login"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process registration
    if submit_btn:
        if not all([name, email, password, confirm_password, department, student_id, year]):
            st.error("⚠️ All fields are required. Please fill in the registration details.")
            return
            
        if password != confirm_password:
            st.error("❌ Mismatched Passwords: Your password and confirmation password do not match.")
            return
            
        # Register user in database
        success, msg = register_user(
            name=name,
            email=email,
            password=password,
            department=department,
            student_id=student_id,
            year=year
        )
        
        if success:
            st.success(f"🎉 {msg}")
            time.sleep(1.2)
            st.session_state.page = "Login"
            st.rerun()
        else:
            st.error(f"❌ Registration Failed: {msg}")

if __name__ == "__main__":
    show_register()
