import streamlit as st

def render_stat_cards(total_users: int, user_requests: int, history_count: int, last_active: str) -> None:
    """
    Renders the metric stat cards on the dashboard using a flex/grid custom CSS layout.
    """
    st.markdown(f"""
    <div class="dashboard-grid">
        <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-title">Total Students</div>
            <div class="stat-value">{total_users}</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🤖</div>
            <div class="stat-title">My AI Requests</div>
            <div class="stat-value">{user_requests}</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📜</div>
            <div class="stat-title">Chat Records</div>
            <div class="stat-value">{history_count}</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">⚡</div>
            <div class="stat-title">Session Activity</div>
            <div class="stat-value" style="font-size: 1.15rem; margin-top: 8px; color: #10b981; font-weight:600;">{last_active}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_quick_actions() -> None:
    """
    Renders interactive card widgets representing rapid triggers/shortcuts
    to key panels (Chatbot, Profile editing, and Settings/theme overrides).
    """
    st.markdown("<h3 style='margin-top: 25px; font-weight: 700; color: #e2e8f0;'>⚡ Quick Actions</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: #94a3b8; margin-top: -10px; margin-bottom: 20px;'>Quickly launch tasks or update configurations.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-icon">💬</div>
            <div class="action-card-text">
                <div class="action-card-title">Campus Chatbot</div>
                <div class="action-card-desc">Get assignment structure, debugging help, or career answers.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Small margin spacing, followed by the redirect button styled via CSS
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button("Launch AI Assistant 🤖", key="qa_btn_chat"):
            st.session_state.page = "AI Assistant"
            st.rerun()
            
    with col2:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-icon">👤</div>
            <div class="action-card-text">
                <div class="action-card-title">Student Profile</div>
                <div class="action-card-desc">Edit your official department information or registration ID.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button("Edit Profile Details 👤", key="qa_btn_profile"):
            st.session_state.page = "Profile"
            st.rerun()
            
    with col3:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-icon">⚙️</div>
            <div class="action-card-text">
                <div class="action-card-title">Preferences & API</div>
                <div class="action-card-desc">Change interface dark themes or validation of your API key.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button("Manage Settings ⚙️", key="qa_btn_settings"):
            st.session_state.page = "Settings"
            st.rerun()
