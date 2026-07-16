import os
import streamlit as st
from datetime import datetime

def load_css() -> None:
    """Loads and injects the global stylesheet into the current Streamlit app page."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    css_path = os.path.join(base_dir, "assets", "style.css")
    
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading stylesheet: {str(e)}")
    else:
        st.warning("Stylesheet file not found. Styles will fallback to defaults.")
        
    # Inject light theme override block if the session is toggled to light theme
    if st.session_state.get("theme", "dark") == "light":
        st.markdown("""
        <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
            --card-gradient: linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%) !important;
            --card-bg-dark: #ffffff !important;
            --border-dark: #cbd5e1 !important;
            --text-dark: #0f172a !important;
            --text-muted-dark: #475569 !important;
        }
        .stApp {
            background-color: #f8fafc !important;
            color: #0f172a !important;
        }
        .stat-card {
            background: linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%) !important;
            border-color: #cbd5e1 !important;
        }
        .stat-card:hover {
            box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.1) !important;
        }
        .stat-value {
            color: #0f172a !important;
        }
        .stat-title {
            color: #475569 !important;
        }
        .action-card {
            background: linear-gradient(135deg, rgba(241, 245, 249, 0.7) 0%, rgba(226, 232, 240, 0.7) 100%) !important;
            border-color: #cbd5e1 !important;
        }
        .action-card:hover {
            background: rgba(226, 232, 240, 0.9) !important;
        }
        .action-card-title {
            color: #0f172a !important;
        }
        .action-card-desc {
            color: #475569 !important;
        }
        .history-item {
            background: rgba(241, 245, 249, 0.5) !important;
            border-color: #cbd5e1 !important;
        }
        .history-item:hover {
            border-color: #4f46e5 !important;
        }
        .history-meta {
            color: #64748b !important;
            border-bottom-color: rgba(0, 0, 0, 0.05) !important;
        }
        .history-q {
            color: #1e293b !important;
        }
        .history-a {
            color: #334155 !important;
        }
        .profile-name {
            color: #0f172a !important;
        }
        .profile-header-container {
            background: linear-gradient(135deg, rgba(241, 245, 249, 0.6) 0%, rgba(226, 232, 240, 0.6) 100%) !important;
            border-color: #cbd5e1 !important;
        }
        h2, h3, h4, .main-title {
            color: #0f172a !important;
        }
        .subtitle {
            color: #475569 !important;
        }
        .secondary-btn button {
            color: #0f172a !important;
            border-color: #cbd5e1 !important;
        }
        .secondary-btn button:hover {
            background: rgba(0, 0, 0, 0.05) !important;
            color: #4f46e5 !important;
        }
        </style>
        """, unsafe_allow_html=True)

def get_time_based_greeting() -> str:
    """Returns a personalized greeting depending on the current time of day."""
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

def format_timestamp(iso_string: str) -> str:
    """Formats an ISO-formatted timestamp into a clean, human-readable date/time string."""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%b %d, %Y - %I:%M %p")
    except Exception:
        return iso_string

def get_department_icon(dept: str) -> str:
    """Maps departments to nice emojis for visual design."""
    dept_lower = dept.lower()
    if "computer" in dept_lower or "software" in dept_lower or "it" in dept_lower or "cs" in dept_lower:
        return "💻"
    elif "mechanic" in dept_lower or "mech" in dept_lower:
        return "⚙️"
    elif "electric" in dept_lower or "ee" in dept_lower or "ece" in dept_lower:
        return "⚡"
    elif "civil" in dept_lower:
        return "🏗️"
    elif "bio" in dept_lower or "chem" in dept_lower:
        return "🧪"
    elif "business" in dept_lower or "mba" in dept_lower or "finance" in dept_lower:
        return "💼"
    else:
        return "🎓"
