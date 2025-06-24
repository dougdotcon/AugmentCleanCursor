"""
JetBrains IDE handlers for Free AugmentCode.

This module provides functions to handle JetBrains IDE operations,
including modifying PermanentDeviceId and PermanentUserId.
"""

import os
import sys
import stat
import uuid
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


def backup_file(file_path: Path) -> str:
    """
    Create a backup of the file.
    
    Args:
        file_path (Path): Path to the file to backup
        
    Returns:
        str: Path to the backup file
    """
    if not file_path.exists():
        return ""
    
    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
    shutil.copy2(file_path, backup_path)
    return str(backup_path)


def lock_file(file_path: Path) -> bool:
    """
    Lock a file to prevent modification.
    
    Args:
        file_path (Path): Path to the file to lock
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not file_path.exists():
            return False
        
        # Set file as read-only using Python API
        current_permissions = file_path.stat().st_mode
        file_path.chmod(stat.S_IREAD)
        
        # Use platform-specific commands for additional protection
        if sys.platform == "win32":
            # Windows: Use attrib command
            try:
                subprocess.run(
                    ["attrib", "+R", str(file_path)], 
                    check=False, 
                    capture_output=True
                )
            except Exception:
                pass
        else:
            # Unix-like systems: Use chmod
            try:
                subprocess.run(
                    ["chmod", "444", str(file_path)], 
                    check=False, 
                    capture_output=True
                )
            except Exception:
                pass
            
            # macOS: Use chflags for additional protection
            if sys.platform == "darwin":
                try:
                    subprocess.run(
                        ["chflags", "uchg", str(file_path)], 
                        check=False, 
                        capture_output=True
                    )
                except Exception:
                    pass
        
        return True
    except Exception:
        return False


def update_jetbrains_id_file(file_path: Path) -> Dict[str, Any]:
    """
    Update a JetBrains ID file with a new UUID.
    
    Args:
        file_path (Path): Path to the ID file
        
    Returns:
        dict: Operation result with old and new UUIDs
    """
    try:
        # Read old UUID if file exists
        old_uuid = ""
        if file_path.exists():
            try:
                old_uuid = file_path.read_text(encoding='utf-8').strip()
            except Exception:
                old_uuid = "Não foi possível ler"
        
        # Generate new UUID
        new_uuid = generate_uuid()
        
        # Create backup
        backup_path = backup_file(file_path)
        
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write new UUID
        file_path.write_text(new_uuid, encoding='utf-8')
        
        # Lock the file
        lock_success = lock_file(file_path)
        
        return {
            "success": True,
            "old_uuid": old_uuid,
            "new_uuid": new_uuid,
            "backup_path": backup_path,
            "locked": lock_success,
            "file_path": str(file_path)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file_path": str(file_path)
        }


def get_jetbrains_config_dir() -> Optional[str]:
    """
    Get JetBrains configuration directory path.

    Returns:
        str: Path to JetBrains configuration directory, or None if not found
    """
    home_dir = Path.home()

    # Common JetBrains config paths
    possible_paths = [
        # Windows
        home_dir / "AppData" / "Roaming" / "JetBrains",
        # macOS
        home_dir / "Library" / "Application Support" / "JetBrains",
        # Linux
        home_dir / ".config" / "JetBrains",
        # Alternative Linux path
        home_dir / ".JetBrains",
    ]

    for path in possible_paths:
        if path.exists() and path.is_dir():
            return str(path)

    return None


def get_jetbrains_info(config_dir: str) -> Dict[str, Any]:
    """
    Get information about installed JetBrains IDEs.

    Args:
        config_dir (str): JetBrains configuration directory path

    Returns:
        dict: Information about installed JetBrains IDEs
    """
    config_path = Path(config_dir)
    ides = []

    if not config_path.exists():
        return {"ides": ides, "count": 0}

    # Look for IDE directories
    for item in config_path.iterdir():
        if item.is_dir():
            # Check if it looks like an IDE directory (contains config files)
            config_file = item / "options" / "other.xml"
            if config_file.exists():
                ide_name = item.name
                ides.append({
                    "name": ide_name,
                    "path": str(item),
                    "config_file": str(config_file)
                })

    return {
        "ides": ides,
        "count": len(ides)
    }


def modify_jetbrains_ids(jetbrains_config_path: str) -> Dict[str, Any]:
    """
    Modify JetBrains PermanentDeviceId and PermanentUserId.

    Args:
        jetbrains_config_path (str): Path to JetBrains configuration directory

    Returns:
        dict: Operation result with backup information and new IDs
    """
    try:
        config_path = Path(jetbrains_config_path)
        
        if not config_path.exists():
            return {
                "success": False,
                "error": f"Diretório de configuração do JetBrains não existe: {jetbrains_config_path}",
                "message": "Diretório de configuração não encontrado"
            }

        # Generate new UUIDs
        new_device_id = str(uuid.uuid4())
        new_user_id = str(uuid.uuid4())

        # File paths
        device_id_file = config_path / "PermanentDeviceId"
        user_id_file = config_path / "PermanentUserId"

        # Backup and modify files
        results = {
            "device_id": {"success": False, "old_value": None, "new_value": new_device_id},
            "user_id": {"success": False, "old_value": None, "new_value": new_user_id},
            "backup_path": None
        }

        # Create backup directory
        backup_dir = config_path / "backup_augment_free"
        backup_dir.mkdir(exist_ok=True)

        overall_success = True

        # Handle Device ID
        if device_id_file.exists():
            try:
                # Read old value
                with open(device_id_file, 'r', encoding='utf-8') as f:
                    old_device_id = f.read().strip()
                    results["device_id"]["old_value"] = old_device_id
            except Exception:
                old_device_id = "Não foi possível ler"

            # Backup original file
            backup_device_file = backup_dir / "PermanentDeviceId.backup"
            shutil.copy2(device_id_file, backup_device_file)

            # Write new value
            try:
                with open(device_id_file, 'w', encoding='utf-8') as f:
                    f.write(new_device_id)
                results["device_id"]["success"] = True
            except Exception as e:
                overall_success = False
                results["device_id"]["error"] = str(e)
        else:
            # Create new file
            try:
                with open(device_id_file, 'w', encoding='utf-8') as f:
                    f.write(new_device_id)
                results["device_id"]["success"] = True
            except Exception as e:
                overall_success = False
                results["device_id"]["error"] = str(e)

        # Handle User ID
        if user_id_file.exists():
            try:
                # Read old value
                with open(user_id_file, 'r', encoding='utf-8') as f:
                    old_user_id = f.read().strip()
                    results["user_id"]["old_value"] = old_user_id
            except Exception:
                old_user_id = "Não foi possível ler"

            # Backup original file
            backup_user_file = backup_dir / "PermanentUserId.backup"
            shutil.copy2(user_id_file, backup_user_file)

            # Write new value
            try:
                with open(user_id_file, 'w', encoding='utf-8') as f:
                    f.write(new_user_id)
                results["user_id"]["success"] = True
            except Exception as e:
                overall_success = False
                results["user_id"]["error"] = str(e)
        else:
            # Create new file
            try:
                with open(user_id_file, 'w', encoding='utf-8') as f:
                    f.write(new_user_id)
                results["user_id"]["success"] = True
            except Exception as e:
                overall_success = False
                results["user_id"]["error"] = str(e)

        # Set file permissions to prevent regeneration (Unix-like systems)
        if os.name != 'nt':  # Not Windows
            try:
                if device_id_file.exists():
                    os.chmod(device_id_file, 0o444)  # Read-only
                if user_id_file.exists():
                    os.chmod(user_id_file, 0o444)  # Read-only
            except Exception:
                pass  # Ignore permission errors

        return {
            "success": overall_success,
            "data": {
                "new_device_id": new_device_id,
                "new_user_id": new_user_id,
                "backup_path": str(backup_dir),
                "results": results
            },
            "message": "Processamento de arquivos de ID do JetBrains concluído" if overall_success else "Falha no processamento de alguns arquivos"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Falha no processamento de IDs do JetBrains: {str(e)}"
        }


def read_jetbrains_file_content(file_path: str) -> str:
    """
    Read content from a JetBrains file safely.

    Args:
        file_path (str): Path to the file to read

    Returns:
        str: File content or error message
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return "Não foi possível ler"
