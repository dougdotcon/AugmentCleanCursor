"""
Cursor database cleaner module
"""

import os
import sys
import sqlite3
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional

from .utils import info, success, error, warning, get_cursor_paths, backup_file, clean_extensions_directory

def clean_cursor_db() -> bool:
    """
    Clean Cursor databases by removing entries containing "augment"

    Returns:
        True if successful, False otherwise
    """
    info("Starting database cleanup process")

    # Get Cursor paths
    paths = get_cursor_paths()
    state_db = paths["state_db"]

    if not state_db.exists():
        warning(f"Cursor database not found at: {state_db}")
        return False

    info(f"Found Cursor database at: {state_db}")
    
    # Create backup
    backup_path = backup_file(state_db)
    
    # Connect to the database
    try:
        # Connect to the original database
        conn = sqlite3.connect(str(state_db))
        cursor = conn.cursor()
        
        # Get the count of records before deletion
        cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%augment%'")
        count_before = cursor.fetchone()[0]
        
        if count_before == 0:
            info("No Augment-related entries found in the database")
            conn.close()
            return True
        
        # Delete records containing "augment"
        cursor.execute("DELETE FROM ItemTable WHERE key LIKE '%augment%'")
        conn.commit()
        
        # Get the count of records after deletion
        cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%augment%'")
        count_after = cursor.fetchone()[0]
        
        conn.close()
        
        success(f"Removed {count_before - count_after} Augment-related entries from the database")
        return True
        
    except sqlite3.Error as e:
        error(f"SQLite error: {e}")
        
        # Restore from backup if there was an error
        if backup_path.exists():
            info("Restoring from backup...")
            try:
                shutil.copy2(backup_path, state_db)
                success("Restored from backup")
            except Exception as restore_error:
                error(f"Failed to restore from backup: {restore_error}")
        
        return False
    except Exception as e:
        error(f"Unexpected error: {e}")
        return False

def clean_cursor_extensions() -> bool:
    """
    Clean Cursor extensions directory by removing all extensions

    Returns:
        True if successful, False otherwise
    """
    info("Starting extensions cleanup process")

    # Get Cursor paths
    paths = get_cursor_paths()
    extensions_dir = paths["extensions_dir"]

    return clean_extensions_directory(extensions_dir)
