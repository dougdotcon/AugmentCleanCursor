"""
VS Code telemetry ID modifier module
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

from .utils import (
    info, success, error, warning, 
    get_vscode_paths, backup_file,
    generate_machine_id, generate_device_id
)

def modify_telemetry_ids() -> bool:
    """
    Modify telemetry IDs in VS Code storage.json file
    
    Returns:
        True if successful, False otherwise
    """
    info("Starting VS Code telemetry ID modification")
    
    # Get VS Code paths
    paths = get_vscode_paths()
    storage_json = paths["storage_json"]
    
    if not storage_json.exists():
        warning(f"VS Code storage.json not found at: {storage_json}")
        return False
    
    info(f"Found storage.json at: {storage_json}")
    
    # Create backup
    backup_path = backup_file(storage_json)
    
    # Generate new IDs
    info("Generating new telemetry IDs...")
    machine_id = generate_machine_id()
    device_id = generate_device_id()
    
    # Read the current file
    try:
        with open(storage_json, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # Update the values
        content["telemetry.machineId"] = machine_id
        content["telemetry.devDeviceId"] = device_id
        
        # Write the updated content back to the file
        with open(storage_json, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)
        
        success("Successfully updated telemetry IDs")
        info(f"New machineId: {machine_id}")
        info(f"New devDeviceId: {device_id}")
        info("You may need to restart VS Code for changes to take effect")
        
        return True
        
    except json.JSONDecodeError:
        error("The storage file is not valid JSON")
        return False
    except Exception as e:
        error(f"Unexpected error: {e}")
        return False
