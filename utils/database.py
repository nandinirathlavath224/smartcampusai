import os
import json
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base directory setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
USERS_FILE = os.path.join(DATABASE_DIR, "users.json")
HISTORY_FILE = os.path.join(DATABASE_DIR, "history.json")

def ensure_db_exists() -> None:
    """Ensures database directory and files exist."""
    os.makedirs(DATABASE_DIR, exist_ok=True)
    for file_path in [USERS_FILE, HISTORY_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
            logger.info(f"Created missing database file: {file_path}")

def load_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Loads data from a JSON file.
    Handles missing or corrupted JSON files gracefully.
    """
    ensure_db_exists()
    
    if not os.path.exists(file_path):
        return []
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Corrupted JSON file {file_path}: {str(e)}. Backing up and resetting.")
        
        # Backup corrupted file
        backup_path = f"{file_path}.corrupted_{int(os.path.getmtime(file_path))}"
        try:
            os.rename(file_path, backup_path)
            logger.info(f"Backed up corrupted database to: {backup_path}")
        except Exception as rename_err:
            logger.error(f"Failed to backup corrupted file: {str(rename_err)}")
            
        # Reset file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        return []
    except Exception as e:
        logger.error(f"Unexpected error loading JSON file {file_path}: {str(e)}")
        return []

def save_data(file_path: str, data: List[Dict[str, Any]]) -> bool:
    """
    Saves a Python list/dict structure to a JSON file.
    Returns True if successful, False otherwise.
    """
    ensure_db_exists()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving to JSON file {file_path}: {str(e)}")
        return False

def get_users() -> List[Dict[str, Any]]:
    """Helper to load user database."""
    return load_data(USERS_FILE)

def save_users(users: List[Dict[str, Any]]) -> bool:
    """Helper to save user database."""
    return save_data(USERS_FILE, users)

def get_history() -> List[Dict[str, Any]]:
    """Helper to load chat history database."""
    return load_data(HISTORY_FILE)

def save_history(history: List[Dict[str, Any]]) -> bool:
    """Helper to save chat history database."""
    return save_data(HISTORY_FILE, history)
