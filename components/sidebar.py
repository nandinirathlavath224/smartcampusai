import streamlit as st
from streamlit_option_menu import option_menu
import os

def render_sidebar() -> str:
    """
    Renders a unified custom sidebar.
    Shows the logo, user status dashboard details, and option-menu navigation.
    Returns the selected page label.
    """
    with st.sidebar:
        # Render Logo
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.markdown(
                "<h2 style='text-align: center; color: #818cf8; margin-top: 10px;'>🎓 SmartCampusAI</h2>", 
                unsafe_allow_html=True
            )
            
        st.markdown("<hr style='margin: 12px 0; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
        
        # User details card
        is_logged_in = st.session_state.get("logged_in", False)
        if is_logged_in:
            user = st.session_state.get("user", {})
            st.markdown(f"""
            <div style='text-align: center; padding: 12px; background: rgba(99, 102, 241, 0.1); border-radius: 14px; margin-bottom: 18px; border: 1px solid rgba(99, 102, 241, 0.2);'>
                <div style='font-size: 1rem; font-weight: 700; color: #f8fafc;'>{user.get('name', 'Student')}</div>
                <div style='font-size: 0.8rem; color: #818cf8; font-weight: 500;'>ID: {user.get('student_id', '')}</div>
                <div style='font-size: 0.75rem; color: #94a3b8; margin-top: 2px;'>{user.get('department', '')} • {user.get('year', '')} Yr</div>
            </div>
            """, unsafe_allow_html=True)
            
            options = ["Dashboard", "AI Assistant", "History", "Profile", "Settings", "Logout"]
            icons = ["grid-fill", "chat-square-dots-fill", "clock-history", "person-badge-fill", "gear-fill", "box-arrow-right"]
            menu_title = "Navigation"
        else:
            options = ["Login", "Register"]
            icons = ["box-arrow-in-right", "person-plus-fill"]
            menu_title = "Welcome"
            
        # Determine dynamic default index based on session state page
        current_page = st.session_state.get("page", "Dashboard" if is_logged_in else "Login")
        if current_page in options:
            default_idx = options.index(current_page)
        else:
            default_idx = 0
            
        # Customize style dictionary for the option menu
        selected = option_menu(
            menu_title=menu_title,
            options=options,
            icons=icons,
            menu_icon="cast",
            default_index=default_idx,
            styles={
                "container": {
                    "padding": "2px !important", 
                    "background-color": "transparent"
                },
                "icon": {
                    "color": "#818cf8", 
                    "font-size": "15px"
                }, 
                "nav-link": {
                    "font-size": "14px", 
                    "text-align": "left", 
                    "margin": "4px 0px", 
                    "border-radius": "8px",
                    "color": "#94a3b8",
                    "--hover-color": "rgba(99, 102, 241, 0.08)"
                },
                "nav-link-selected": {
                    "background-color": "#4f46e5", 
                    "color": "#ffffff",
                    "font-weight": "500"
                },
                "menu-title": {
                    "color": "#64748b",
                    "font-size": "12px",
                    "text-transform": "uppercase",
                    "letter-spacing": "0.08em",
                    "font-weight": "600"
                }
            }
        )
        
        # Save selection back to session state to maintain synchronization
        st.session_state.page = selected
        
        # Sidebar Footer
        st.markdown(
            "<div style='margin-top: 40px; text-align: center; font-size: 0.7rem; color: #475569;'>"
            "SmartCampusAI v1.0.0<br>© 2026 DeepMind Pair Project"
            "</div>", 
            unsafe_allow_html=True
        )
        
    return selected
