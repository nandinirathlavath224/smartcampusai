import uuid
import hashlib
from datetime import datetime
import re
from typing import Dict, Any, Optional, Tuple
from utils.database import get_users, save_users

# Static salt for simple security enhancement
PASSWORD_SALT = "SmartCampusAI_Secure_Salt_2026"

def hash_password(password: str) -> str:
    """Hashes the user password using SHA-256 with a static salt."""
    salted_pwd = password + PASSWORD_SALT
    return hashlib.sha256(salted_pwd.encode("utf-8")).hexdigest()

def is_valid_email(email: str) -> bool:
    """Validates email format using regex."""
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(email_regex, email))

def is_strong_password(password: str) -> Tuple[bool, str]:
    """
    Checks if a password meets the strength requirements:
    - At least 6 characters long
    - Contains at least one uppercase or lowercase letter
    - Contains at least one digit
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not any(c.isalpha() for c in password):
        return False, "Password must contain at least one letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    return True, "Password is strong."

def register_user(
    name: str, 
    email: str, 
    password: str, 
    department: str, 
    student_id: str, 
    year: str
) -> Tuple[bool, str]:
    """
    Registers a new student.
    Performs field validations and stores the record in users.json.
    """
    # Clean inputs
    name = name.strip()
    email = email.strip().lower()
    department = department.strip()
    student_id = student_id.strip()
    year = year.strip()
    
    # Empty field validation
    if not all([name, email, password, department, student_id, year]):
        return False, "All fields are required."
        
    # Email structure check
    if not is_valid_email(email):
        return False, "Please enter a valid email address."
        
    # Password strength check
    is_strong, pwd_err = is_strong_password(password)
    if not is_strong:
        return False, pwd_err
        
    # Check if email already exists
    users = get_users()
    for u in users:
        if u["email"] == email:
            return False, "An account with this email already exists."
            
    # Check if Student ID already exists
    for u in users:
        if u["student_id"] == student_id:
            return False, "This Student ID is already registered."
            
    # Hash password and create record
    hashed_pwd = hash_password(password)
    new_user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password": hashed_pwd,
        "department": department,
        "student_id": student_id,
        "year": year,
        "created_at": datetime.now().isoformat()
    }
    
    users.append(new_user)
    if save_users(users):
        return True, "Registration successful!"
    return False, "Database error: Could not complete registration."

def authenticate_user(email: str, password: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Authenticates a user.
    Returns the user data (excluding password) if successful, along with status message.
    """
    email = email.strip().lower()
    
    if not email or not password:
        return None, "Email and password are required."
        
    users = get_users()
    hashed_pwd = hash_password(password)
    
    for u in users:
        if u["email"] == email:
            if u["password"] == hashed_pwd:
                # Return a copy of user info without the password hash
                user_copy = u.copy()
                user_copy.pop("password", None)
                return user_copy, "Login successful."
            else:
                return None, "Invalid email or password."
                
    return None, "Invalid email or password."

def update_user_profile(
    email: str, 
    name: str, 
    department: str, 
    student_id: str, 
    year: str
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Updates the profile info of an existing user.
    """
    name = name.strip()
    department = department.strip()
    student_id = student_id.strip()
    year = year.strip()
    
    if not all([name, department, student_id, year]):
        return False, "All fields are required.", None
        
    users = get_users()
    updated_user = None
    
    # Check if updated student ID conflicts with another user
    for u in users:
        if u["email"] != email and u["student_id"] == student_id:
            return False, "This Student ID is already registered by another student.", None
            
    # Update values
    for u in users:
        if u["email"] == email:
            u["name"] = name
            u["department"] = department
            u["student_id"] = student_id
            u["year"] = year
            updated_user = u.copy()
            updated_user.pop("password", None)
            break
            
    if updated_user and save_users(users):
        return True, "Profile updated successfully!", updated_user
        
    return False, "User not found or database write failed.", None
