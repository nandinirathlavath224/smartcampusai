import streamlit as st
from components.navbar import render_navbar
from utils.ai import get_api_key, test_api_key
from utils.helpers import load_css

def show_settings() -> None:
    """
    Renders the Settings page.
    Handles theme toggles, custom OpenAI API key verification,
    and provides logout capability.
    """
    load_css()
    
    # Render top navbar
    render_navbar()
    
    st.markdown("<h2 class='main-title'>System Settings</h2>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Manage application display preferences and API credentials.</p>", unsafe_allow_html=True)
    
    # Theme Selection
    st.markdown("### 🎨 Interface Customization")
    
    # Initialize theme state if not present
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
        
    theme_choice = st.radio(
        "Choose Theme Mode:",
        ["Dark Mode 🌙", "Light Mode ☀️"],
        index=0 if st.session_state.theme == "dark" else 1,
        help="Switches the interface styling variables."
    )
    
    # Update theme state on change
    new_theme = "dark" if "Dark" in theme_choice else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.success(f"Theme switched to {new_theme.capitalize()} mode!")
        import time
        time.sleep(0.5)
        st.rerun()
        
    st.markdown("<hr style='margin: 20px 0; border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
    
    # API Key Configuration
    st.markdown("### 🔑 API Key Override")
    st.markdown(
        "<p style='font-size: 0.85rem; color: #94a3b8; margin-top: -10px;'>"
        "Provide a personal OpenAI API Key to override the environment variable default config.</p>", 
        unsafe_allow_html=True
    )
    
    # Display current key status
    active_key = get_api_key()
    key_placeholder = "••••••••••••••••••••••••" if active_key else "OpenAI API Key (sk-...)"
    
    input_key = st.text_input(
        "OpenAI API Key Override",
        type="password",
        placeholder=key_placeholder,
        help="Your API Key is kept in temporary memory and never stored in the JSON database."
    )
    
    col_save_key, col_test_key = st.columns(2)
    
    with col_save_key:
        if st.button("Save API Key Override 💾"):
            if input_key:
                st.session_state.openai_api_key = input_key.strip()
                # Clear validation status since the key changed
                st.session_state.api_key_valid = None
                st.success("API Key override saved in active session!")
                import time
                time.sleep(0.6)
                st.rerun()
            else:
                st.warning("Please type a valid API Key to save.")
                
    with col_test_key:
        if st.button("Test Connection Status ⚡"):
            test_key = input_key.strip() if input_key else active_key
            if not test_key:
                st.error("No API key available to test. Please input a key first.")
            else:
                with st.spinner("Testing API authenticity against OpenAI models list..."):
                    is_valid = test_api_key(test_key)
                    if is_valid:
                        st.session_state.api_key_valid = True
                        st.success("✅ **Success**: OpenAI API is active and connected!")
                    else:
                        st.session_state.api_key_valid = False
                        st.error("❌ **Verification Failed**: Invalid OpenAI API Key.")
                    import time
                    time.sleep(1.0)
                    st.rerun()
                    
    # Remove override
    if st.session_state.get("openai_api_key"):
        if st.button("Remove API Key Override 🗑️", type="secondary"):
            st.session_state.pop("openai_api_key", None)
            st.session_state.api_key_valid = None
            st.info("API Key override removed. Restored environment variable defaults.")
            import time
            time.sleep(0.6)
            st.rerun()
            
    st.markdown("<hr style='margin: 20px 0; border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
    
    # Session Management Actions
    st.markdown("### 🚪 Account Session")
    
    if st.button("Logout from SmartCampusAI 📤", type="primary"):
        # Reset session states
        st.session_state.logged_in = False
        st.session_state.user = None
        # Clear chat caches
        st.session_state.pop("chat_messages", None)
        # Redirect
        st.session_state.page = "Login"
        st.success("Logged out successfully. Redirecting...")
        import time
        time.sleep(0.8)
        st.rerun()

if __name__ == "__main__":
    show_settings()
