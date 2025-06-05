"""
Utility functions for the Augment VIP project
"""

import os
import sys
import platform
import json
import sqlite3
import uuid
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Console colors
try:
    from colorama import init, Fore, Style
    init()  # Initialize colorama for Windows support
    
    def info(msg: str) -> None:
        """Print an info message in blue"""
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} {msg}")
    
    def success(msg: str) -> None:
        """Print a success message in green"""
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {msg}")
    
    def warning(msg: str) -> None:
        """Print a warning message in yellow"""
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {msg}")
    
    def error(msg: str) -> None:
        """Print an error message in red"""
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}")
        
except ImportError:
    # Fallback if colorama is not installed
    def info(msg: str) -> None:
        print(f"[INFO] {msg}")
    
    def success(msg: str) -> None:
        print(f"[SUCCESS] {msg}")
    
    def warning(msg: str) -> None:
        print(f"[WARNING] {msg}")
    
    def error(msg: str) -> None:
        print(f"[ERROR] {msg}")

def get_cursor_paths() -> Dict[str, Path]:
    """
    Get Cursor paths based on the operating system

    Returns:
        Dict with paths to Cursor directories and files
    """
    system = platform.system()
    paths = {}

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        userprofile = os.environ.get("USERPROFILE")
        if not appdata or not userprofile:
            error("APPDATA or USERPROFILE environment variable not found")
            sys.exit(1)

        base_dir = Path(appdata) / "Cursor" / "User"
        extensions_dir = Path(userprofile) / ".cursor" / "extensions"

    elif system == "Darwin":  # macOS
        base_dir = Path.home() / "Library" / "Application Support" / "Cursor" / "User"
        extensions_dir = Path.home() / ".cursor" / "extensions"

    elif system == "Linux":
        base_dir = Path.home() / ".config" / "Cursor" / "User"
        extensions_dir = Path.home() / ".cursor" / "extensions"

    else:
        error(f"Unsupported operating system: {system}")
        sys.exit(1)

    # Common paths
    paths["base_dir"] = base_dir
    paths["storage_json"] = base_dir / "globalStorage" / "storage.json"
    paths["state_db"] = base_dir / "globalStorage" / "state.vscdb"
    paths["extensions_dir"] = extensions_dir

    return paths

def backup_file(file_path: Path) -> Path:
    """
    Create a backup of a file
    
    Args:
        file_path: Path to the file to backup
        
    Returns:
        Path to the backup file
    """
    if not file_path.exists():
        error(f"File not found: {file_path}")
        sys.exit(1)
        
    backup_path = Path(f"{file_path}.backup")
    shutil.copy2(file_path, backup_path)
    success(f"Created backup at: {backup_path}")
    
    return backup_path

def generate_machine_id() -> str:
    """Generate a random 64-character hex string for machineId"""
    return uuid.uuid4().hex + uuid.uuid4().hex

def generate_device_id() -> str:
    """Generate a random UUID v4 for devDeviceId"""
    return str(uuid.uuid4())

def clean_extensions_directory(extensions_dir: Path) -> bool:
    """
    Clean Cursor extensions directory by removing all extensions

    Args:
        extensions_dir: Path to the extensions directory

    Returns:
        True if successful, False otherwise
    """
    if not extensions_dir.exists():
        warning(f"Extensions directory not found at: {extensions_dir}")
        return False

    info(f"Found extensions directory at: {extensions_dir}")

    try:
        # Count extensions before deletion
        extensions_before = list(extensions_dir.iterdir())
        count_before = len(extensions_before)

        if count_before == 0:
            info("No extensions found in the directory")
            return True

        info(f"Found {count_before} extensions to remove")

        # Remove all extensions
        for extension_path in extensions_before:
            if extension_path.is_dir():
                shutil.rmtree(extension_path)
                info(f"Removed extension directory: {extension_path.name}")
            elif extension_path.is_file():
                extension_path.unlink()
                info(f"Removed extension file: {extension_path.name}")

        # Count extensions after deletion
        extensions_after = list(extensions_dir.iterdir())
        count_after = len(extensions_after)

        success(f"Successfully removed {count_before - count_after} extensions")
        return True

    except PermissionError:
        error("Permission denied. Please close Cursor and try again.")
        return False
    except Exception as e:
        error(f"Unexpected error while cleaning extensions: {e}")
        return False
