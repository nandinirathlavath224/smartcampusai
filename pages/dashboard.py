import streamlit as st
from datetime import datetime
from components.navbar import render_navbar
from components.cards import render_stat_cards, render_quick_actions
from utils.database import get_users, get_history
from utils.helpers import load_css, format_timestamp, get_department_icon

def show_dashboard() -> None:
    """
    Renders the modern Dashboard page.
    Displays analytics cards, quick actions, and recent activity logs.
    """
    load_css()
    
    # Render premium top navigation
    render_navbar()
    
    # Retrieve data metrics
    users = get_users()
    history = get_history()
    
    current_user = st.session_state.get("user", {})
    user_email = current_user.get("email", "")
    
    # Filter stats
    total_users_count = len(users)
    user_chats = [chat for chat in history if chat.get("email") == user_email]
    user_requests_count = len(user_chats)
    user_history_count = len(user_chats)
    
    # Calculate session status or last activity time
    if user_chats:
        # Sort by iso timestamp to get last action
        sorted_chats = sorted(user_chats, key=lambda x: x.get("time", ""), reverse=True)
        last_action_time = sorted_chats[0].get("time", "")
        last_active = format_timestamp(last_action_time)
    else:
        last_active = "No activity recorded"
        
    # Render dashboard metrics
    st.markdown("<h2 class='main-title'>Dashboard Workspace</h2>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Overview of system metrics and academic assistant stats.</p>", unsafe_allow_html=True)
    
    render_stat_cards(
        total_users=total_users_count,
        user_requests=user_requests_count,
        history_count=user_history_count,
        last_active=last_active
    )
    
    # Render quick action panel
    render_quick_actions()
    
    # Render Recent Activity section
    st.markdown("<h3 style='margin-top: 30px; font-weight: 700; color: #e2e8f0;'>⏳ Recent Activity Feed</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: #94a3b8; margin-top: -10px; margin-bottom: 20px;'>Your last three interactions with the SmartCampusAI Assistant.</p>", unsafe_allow_html=True)
    
    if user_chats:
        # Get last 3 chats
        recent_chats = sorted(user_chats, key=lambda x: x.get("time", ""), reverse=True)[:3]
        
        for idx, chat in enumerate(recent_chats):
            q_preview = chat.get("question", "")
            a_preview = chat.get("answer", "")
            time_formatted = format_timestamp(chat.get("time", ""))
            
            # Truncate previews
            if len(q_preview) > 90:
                q_preview = q_preview[:90] + "..."
            if len(a_preview) > 160:
                a_preview = a_preview[:160] + "..."
                
            st.markdown(f"""
            <div class="history-item" style="animation: fadeInUp {0.6 + idx*0.2}s ease-out;">
                <div class="history-meta">
                    <span>💬 Interaction #{user_requests_count - idx}</span>
                    <span>🕒 {time_formatted}</span>
                </div>
                <div class="history-q">Q: {q_preview}</div>
                <div class="history-a">A: {a_preview}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 **No Activity Found**: You haven't asked any questions yet. Head over to the **AI Assistant** using the sidebar or Quick Actions to get started!")

if __name__ == "__main__":
    show_dashboard()
