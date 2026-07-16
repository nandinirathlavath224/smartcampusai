import streamlit as st
from utils.helpers import get_time_based_greeting
from utils.ai import get_api_key, test_api_key

def render_navbar() -> None:
    """
    Renders a premium top navigation panel.
    Displays personalized greetings, current date/session status,
    and a badge displaying the OpenAI API connectivity status.
    """
    # Personalize greeting
    if st.session_state.get("logged_in", False):
        user = st.session_state.get("user", {})
        name = user.get("name", "Student")
        subtitle = "Welcome back to your campus assistant hub."
    else:
        name = "Guest"
        subtitle = "Sign in to access your student AI assistant workspace."
        
    greeting = get_time_based_greeting()
    
    # Efficient API status caching in session state
    if "api_status" not in st.session_state:
        st.session_state.api_status = "Checked" # Default marker
        
    api_key = get_api_key()
    if not api_key:
        status_badge = (
            '<span style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); '
            'padding: 5px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">'
            '🔴 API Key Unset</span>'
        )
    else:
        # Check if the connection status has already been verified
        if st.session_state.get("api_key_valid") is True:
            status_badge = (
                '<span style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); '
                'padding: 5px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">'
                '🟢 API Connected</span>'
            )
        elif st.session_state.get("api_key_valid") is False:
            status_badge = (
                '<span style="background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); '
                'padding: 5px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">'
                '❌ API Key Invalid</span>'
            )
        else:
            # We have a key but haven't validated it yet; show configured status
            status_badge = (
                '<span style="background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); '
                'padding: 5px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">'
                '🔵 API Key Loaded</span>'
            )
            
    # Draw navbar container
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 12px; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.06);">
        <div>
            <h4 style="margin: 0; color: #f8fafc; font-weight: 700; font-size: 1.25rem;">{greeting}, {name}! 👋</h4>
            <p style="margin: 3px 0 0 0; font-size: 0.8rem; color: #94a3b8;">{subtitle}</p>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            {status_badge}
        </div>
    </div>
    """, unsafe_allow_html=True)
