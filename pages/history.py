import streamlit as st
from components.navbar import render_navbar
from utils.database import get_history, save_history
from utils.helpers import load_css, format_timestamp

def delete_single_chat(email: str, question: str, answer: str, time_stamp: str) -> bool:
    """Deletes a specific chat item matching all credentials from history.json."""
    history = get_history()
    original_len = len(history)
    
    # Filter out the matching item
    updated_history = [
        chat for chat in history
        if not (
            chat.get("email") == email and
            chat.get("question") == question and
            chat.get("answer") == answer and
            chat.get("time") == time_stamp
        )
    ]
    
    # If duplicates exist, this deletes only one by matching length (or all matching copies)
    save_history(updated_history)
    return len(updated_history) < original_len

def clear_user_history(email: str) -> None:
    """Deletes all chat history records for the current user email."""
    history = get_history()
    # Retain other students' history, delete current user's history
    updated_history = [chat for chat in history if chat.get("email") != email]
    save_history(updated_history)

def show_history() -> None:
    """
    Renders the History page.
    Provides keyword filtering, listing of logs, and selective deletion triggers.
    """
    load_css()
    
    # Render top navbar
    render_navbar()
    
    current_user = st.session_state.get("user", {})
    email = current_user.get("email", "")
    
    st.markdown("<h2 class='main-title'>Conversation History</h2>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Review, search, or clear your past AI transactions.</p>", unsafe_allow_html=True)
    
    # Retrieve user specific history
    all_chats = get_history()
    user_chats = [chat for chat in all_chats if chat.get("email") == email]
    
    if not user_chats:
        st.info("💡 **History Empty**: You have not recorded any AI queries yet. Run a chat in the **AI Assistant** page to populate history logs.")
        return
        
    # Actions row: Search & Delete All
    col_search, col_action = st.columns([3, 1])
    
    with col_search:
        search_query = st.text_input("🔍 Search History Logs", placeholder="Type keywords from questions or answers...")
        
    with col_action:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        # Accidental click protection using confirm state or confirmation expander
        with st.popover("🗑️ Clear History"):
            st.warning("Are you sure? This will delete all your conversations forever.")
            confirm_clear = st.button("Yes, Clear All", type="primary", key="clear_all_confirm_btn")
            if confirm_clear:
                clear_user_history(email)
                # Clear active chatbot chat display cache
                if "chat_messages" in st.session_state:
                    st.session_state.chat_messages = []
                st.success("Chat history cleared successfully!")
                import time
                time.sleep(0.8)
                st.rerun()
                
    # Filter chats by search keyword
    filtered_chats = user_chats
    if search_query:
        query_lower = search_query.lower()
        filtered_chats = [
            chat for chat in user_chats
            if query_lower in chat.get("question", "").lower() or query_lower in chat.get("answer", "").lower()
        ]
        
    # Sort history showing newest first
    sorted_chats = sorted(filtered_chats, key=lambda x: x.get("time", ""), reverse=True)
    
    st.markdown(f"<p style='color: #94a3b8; font-size: 0.85rem;'>Showing {len(sorted_chats)} entries</p>", unsafe_allow_html=True)
    
    # Render logs list
    for idx, chat in enumerate(sorted_chats):
        q = chat.get("question", "")
        a = chat.get("answer", "")
        ts = chat.get("time", "")
        time_formatted = format_timestamp(ts)
        
        # Render item content alongside a trash delete button
        col_card, col_delete = st.columns([9, 1])
        
        with col_card:
            st.markdown(f"""
            <div class="history-item">
                <div class="history-meta">
                    <span>🕒 Saved: {time_formatted}</span>
                </div>
                <div class="history-q">Question:</div>
                <p style="color:#f1f5f9; font-size:0.925rem; margin-top:2px;">{q}</p>
                <div class="history-q" style="margin-top:12px;">AI Assistant Response:</div>
                <div class="history-a">{a}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_delete:
            st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
            # Delete button for single chat
            if st.button("🗑️", key=f"del_single_{idx}", help="Delete this interaction"):
                deleted = delete_single_chat(email, q, a, ts)
                if deleted:
                    st.success("Item deleted.")
                    import time
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Error deleting item.")
