import streamlit as st
from datetime import datetime
from components.navbar import render_navbar
from utils.auth import update_user_profile
from utils.helpers import load_css, format_timestamp, get_department_icon

def show_profile() -> None:
    """
    Renders the Profile page.
    Allows students to review registration details and update profile parameters.
    """
    load_css()
    
    # Render top navbar
    render_navbar()
    
    current_user = st.session_state.get("user", {})
    email = current_user.get("email", "")
    name = current_user.get("name", "Student")
    dept = current_user.get("department", "Other")
    student_id = current_user.get("student_id", "")
    year = current_user.get("year", "1st")
    created_at = current_user.get("created_at", "")
    
    st.markdown("<h2 class='main-title'>Student Profile</h2>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Manage and update your campus credentials.</p>", unsafe_allow_html=True)
    
    # Initialize edit mode in session state
    if "editing_profile" not in st.session_state:
        st.session_state.editing_profile = False
        
    # Visual Avatar Header
    dept_icon = get_department_icon(dept)
    initials = "".join([part[0] for part in name.split() if part])[:2].upper()
    
    st.markdown(f"""
    <div class="profile-header-container">
        <div class="profile-avatar-large">
            {initials if initials else "🎓"}
        </div>
        <div class="profile-header-text">
            <div class="profile-name">{name}</div>
            <div class="profile-role">{dept_icon} {dept} Student</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 5px;">Member since: {format_timestamp(created_at)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.editing_profile:
        # Read-only View Mode
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.4); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 1rem;">
                <span style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">Official Full Name</span>
                <div style="font-size: 1.1rem; font-weight: 600; color: #f8fafc; margin-top: 4px;">{name}</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.4); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 1rem;">
                <span style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">University Department</span>
                <div style="font-size: 1.1rem; font-weight: 600; color: #f8fafc; margin-top: 4px;">{dept_icon} {dept}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.4); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 1rem;">
                <span style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">Student ID Number</span>
                <div style="font-size: 1.1rem; font-weight: 600; color: #f8fafc; margin-top: 4px;">{student_id}</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.4); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 1rem;">
                <span style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">Current Academic Year</span>
                <div style="font-size: 1.1rem; font-weight: 600; color: #f8fafc; margin-top: 4px;">{year} Year</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.4); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 1.5rem; width: 100%;">
            <span style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">Login Email Address (Non-editable)</span>
            <div style="font-size: 1.1rem; font-weight: 600; color: #f8fafc; margin-top: 4px;">📧 {email}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Edit Profile Credentials 🛠️", key="edit_profile_btn"):
            st.session_state.editing_profile = True
            st.rerun()
            
    else:
        # Edit Form Mode
        with st.form("edit_profile_form"):
            st.markdown("<h4 style='color: #f8fafc; margin-bottom: 10px;'>Update Credentials</h4>", unsafe_allow_html=True)
            
            new_name = st.text_input("Full Name", value=name)
            
            col1, col2 = st.columns(2)
            with col1:
                new_dept = st.selectbox(
                    "Department",
                    ["Computer Science", "Information Technology", "Electrical Engineering", 
                     "Mechanical Engineering", "Civil Engineering", "Business Administration", "Other"],
                    index=["Computer Science", "Information Technology", "Electrical Engineering", 
                           "Mechanical Engineering", "Civil Engineering", "Business Administration", "Other"].index(dept) 
                           if dept in ["Computer Science", "Information Technology", "Electrical Engineering", 
                                       "Mechanical Engineering", "Civil Engineering", "Business Administration", "Other"] 
                           else 6
                )
            with col2:
                new_year = st.selectbox(
                    "Academic Year",
                    ["1st", "2nd", "3rd", "4th", "Postgraduate"],
                    index=["1st", "2nd", "3rd", "4th", "Postgraduate"].index(year) if year in ["1st", "2nd", "3rd", "4th", "Postgraduate"] else 0
                )
                
            new_student_id = st.text_input("Student ID Number", value=student_id)
            
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            col_save, col_cancel = st.columns(2)
            
            with col_save:
                save_btn = st.form_submit_button("Save Changes")
            with col_cancel:
                cancel_btn = st.form_submit_button("Cancel")
                
        if save_btn:
            # Perform profile updates
            success, msg, updated_user = update_user_profile(
                email=email,
                name=new_name,
                department=new_dept,
                student_id=new_student_id,
                year=new_year
            )
            
            if success:
                st.session_state.user = updated_user
                st.session_state.editing_profile = False
                st.success(msg)
                import time
                time.sleep(0.8)
                st.rerun()
            else:
                st.error(msg)
                
        if cancel_btn:
            st.session_state.editing_profile = False
            st.rerun()

if __name__ == "__main__":
    show_profile()
