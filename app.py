import streamlit as st

# Configure page settings - MUST be the first Streamlit command executed
st.set_page_config(
    page_title="SmartCampusAI Workspace",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

from components.sidebar import render_sidebar

def main() -> None:
    """
    Main application router and session controller.
    Validates credentials, manages page states, and guards authenticated resources.
    """
    # 1. Initialize global session states
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        
    if "user" not in st.session_state:
        st.session_state.user = None
        
    if "page" not in st.session_state:
        # Default starting page based on auth state
        st.session_state.page = "Login"

    # 2. Render sidebar and retrieve user's selection
    selected_page = render_sidebar()

    # 3. Security guards & programmatic navigation checks
    is_authenticated = st.session_state.logged_in
    
    if not is_authenticated:
        # Unauthenticated Security Guard: force redirect to Login/Register
        if selected_page not in ["Login", "Register"]:
            st.session_state.page = "Login"
            st.rerun()
            
        if selected_page == "Register":
            from pages.register import show_register
            show_register()
        else:
            from pages.login import show_login
            show_login()
            
    else:
        # Authenticated Security Guard: prevent returning to Login/Register
        if selected_page in ["Login", "Register"]:
            st.session_state.page = "Dashboard"
            st.rerun()
            
        # Route to the appropriate workspace page
        if selected_page == "Dashboard":
            from pages.dashboard import show_dashboard
            show_dashboard()
            
        elif selected_page == "AI Assistant":
            from pages.ai_assistant import show_ai_assistant
            show_ai_assistant()
            
        elif selected_page == "History":
            from pages.history import show_history
            show_history()
            
        elif selected_page == "Profile":
            from pages.profile import show_profile
            show_profile()
            
        elif selected_page == "Settings":
            from pages.settings import show_settings
            show_settings()
            
        elif selected_page == "Logout":
            # Clear active chatbot caching
            st.session_state.pop("chat_messages", None)
            st.session_state.pop("openai_api_key", None)
            st.session_state.pop("api_key_valid", None)
            
            # Reset authentication parameters
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.page = "Login"
            
            st.success("Successfully logged out. Redirecting...")
            import time
            time.sleep(0.6)
            st.rerun()

if __name__ == "__main__":
    main()
