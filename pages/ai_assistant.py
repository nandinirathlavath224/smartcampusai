import streamlit as st
from datetime import datetime
import time
from components.navbar import render_navbar
from utils.ai import generate_ai_response
from utils.database import get_history, save_history
from utils.helpers import load_css

def add_chat_to_db(email: str, question: str, answer: str) -> None:
    """Logs the Q&A transaction to history.json."""
    history = get_history()
    new_chat = {
        "email": email,
        "question": question,
        "answer": answer,
        "time": datetime.now().isoformat()
    }
    history.append(new_chat)
    save_history(history)

def show_ai_assistant() -> None:
    """
    Renders the AI Assistant page.
    Includes chatbot messages, suggested prompts, and database logging.
    """
    load_css()
    
    # Render top navbar
    render_navbar()
    
    current_user = st.session_state.get("user", {})
    email = current_user.get("email", "")
    
    st.markdown("<h2 class='main-title'>AI Assistant Chatbot</h2>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Ask campus, programming, or career guidance questions.</p>", unsafe_allow_html=True)
    
    # Categories of support with prompt examples
    suggested_prompts = {
        "Programming": "Explain how list comprehensions work in Python with examples.",
        "Assignments": "Help me outline an essay about the impact of cloud computing on business infrastructure.",
        "Exam Preparation": "Generate 3 practice questions for a database systems exam covering Normalization.",
        "Career Guidance": "What skills are most critical to list on a resume for a junior software engineer internship?",
        "Campus FAQs": "How can I organize my schedule to balance 18 credits with part-time work?",
        "Project Ideas": "Suggest a web development capstone project idea for an IT major using JSON files.",
        "Interview Questions": "Explain the difference between SQL and NoSQL databases for a systems interview.",
        "Resume Help": "Help me write a strong resume bullet point using the X-Y-Z formula for a web app project."
    }
    
    # Layout for categories
    st.markdown("<h4 style='font-weight: 600; color: #f8fafc; margin-bottom: 5px;'>1. Choose a Topic Category</h4>", unsafe_allow_html=True)
    category = st.selectbox(
        "Selecting a category automatically tailors the AI's persona and logic:",
        ["General Advice"] + list(suggested_prompts.keys())
    )
    
    # Suggested prompt suggestion helper box
    suggestion_query = None
    if category in suggested_prompts:
        suggestion_text = suggested_prompts[category]
        st.markdown(f"""
        <div style='background: rgba(99, 102, 241, 0.1); border-left: 4px solid #6366f1; padding: 12px; border-radius: 4px 10px 10px 4px; margin-bottom: 15px;'>
            <div style='font-weight: 600; color: #818cf8; font-size: 0.85rem;'>💡 SUGGESTED QUESTION:</div>
            <div style='font-style: italic; color: #cbd5e1; font-size: 0.9rem;'>"{suggestion_text}"</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ask this suggestion 🚀", key="ask_suggested_btn"):
            suggestion_query = suggestion_text
            
    st.markdown("<hr style='margin: 15px 0; border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-weight: 600; color: #f8fafc;'>2. Chat Conversation</h4>", unsafe_allow_html=True)
    
    # Initialize session state chat history for display
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
        
    # Render existing conversation messages
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Process inputs: either typing in input or clicking suggestion button
    user_query = st.chat_input("Type your question here...")
    
    # Overwrite if suggestion button was clicked
    if suggestion_query:
        user_query = suggestion_query
        
    if user_query:
        # Display user query
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        
        # Call AI with spinner
        with st.chat_message("assistant"):
            with st.spinner("Generating academic insights..."):
                response = generate_ai_response(user_query, category)
                st.markdown(response)
                
        # Append assistant response to display state
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        # Save to database
        add_chat_to_db(email, user_query, response)
        
        # Quick sleep and rerun to sync
        time.sleep(0.1)
        st.rerun()

if __name__ == "__main__":
    show_ai_assistant()
