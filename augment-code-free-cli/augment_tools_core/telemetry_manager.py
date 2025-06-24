import json
from pathlib import Path
import shutil # For potential restore logic

# Assuming common_utils.py is in the same directory (augment_tools_core)
from .common_utils import (
    print_info, 
    print_success, 
    print_error, 
    print_warning, 
    create_backup,
    generate_new_machine_id,
    generate_new_device_id
)

def modify_vscode_telemetry_ids(storage_json_path: Path) -> bool:
    """
    Modifies the VS Code telemetry IDs (machineId and devDeviceId) in storage.json.

    Args:
        storage_json_path: Path to the VS Code storage.json file.

    Returns:
        True if modification was successful, False otherwise.
    """
    print_info(f"Attempting to modify telemetry IDs in: {storage_json_path}")

    if not storage_json_path.exists():
        print_error(f"Storage file not found: {storage_json_path}")
        return False

    backup_path = create_backup(storage_json_path)
    if not backup_path:
        print_error("Failed to create a backup. Aborting telemetry ID modification.")
        return False

    try:
        # Generate new IDs
        new_machine_id = generate_new_machine_id()
        new_device_id = generate_new_device_id()
        
        print_info(f"Generated new machineId: {new_machine_id}")
        print_info(f"Generated new devDeviceId: {new_device_id}")

        # Read the JSON file
        with open(storage_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Modify the IDs
        # The structure of storage.json can vary slightly, but typically:
        # machineId is at the root or under 'telemetry'
        # devDeviceId is often under 'telemetry'
        
        modified = False
        if 'machineId' in data:
            if data['machineId'] != new_machine_id:
                data['machineId'] = new_machine_id
                print_info("Updated root machineId.")
                modified = True
        
        if 'telemetry' in data and isinstance(data['telemetry'], dict):
            if 'machineId' in data['telemetry']:
                 if data['telemetry']['machineId'] != new_machine_id:
                    data['telemetry']['machineId'] = new_machine_id
                    print_info("Updated telemetry.machineId.")
                    modified = True
            # else: # If telemetry.machineId doesn't exist, we could add it, but let's stick to modifying existing ones
            #     data['telemetry']['machineId'] = new_machine_id
            #     print_info("Added telemetry.machineId.")
            #     modified = True


            if 'devDeviceId' in data['telemetry']:
                if data['telemetry']['devDeviceId'] != new_device_id:
                    data['telemetry']['devDeviceId'] = new_device_id
                    print_info("Updated telemetry.devDeviceId.")
                    modified = True
            # else: # If telemetry.devDeviceId doesn't exist, we could add it
            #     data['telemetry']['devDeviceId'] = new_device_id
            #     print_info("Added telemetry.devDeviceId.")
            #     modified = True
        
        # Fallback if 'telemetry' object itself doesn't exist but we want to ensure IDs are set
        # This part is more assertive and might change file structure more than just updating.
        # For now, let's primarily focus on updating existing fields as per augment-vip's likely behavior.
        # If 'telemetry' object itself is missing, creating it and adding IDs might be too intrusive
        # without explicit user consent or more detailed knowledge of VSCode's expectations.
        # The original augment-vip seems to update existing fields.

        if not modified:
            print_info("No relevant telemetry IDs found or IDs already match new ones. No changes made to content.")
            # Even if no content change, we consider the operation "successful" in terms of process.
            # If the goal is to *ensure* IDs are new, this logic might need adjustment.
            # For now, "successful" means the file was processed without error.
            return True

        # Write the modified data back to the file
        with open(storage_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4) # Using indent for readability

        print_success(f"Successfully modified telemetry IDs in {storage_json_path}.")
        return True

    except json.JSONDecodeError as e:
        print_error(f"JSON decode error while processing {storage_json_path}: {e}")
    except IOError as e:
        print_error(f"IO error while processing {storage_json_path}: {e}")
    except Exception as e:
        print_error(f"An unexpected error occurred during telemetry ID modification: {e}")

    # If any error occurred, attempt to restore from backup
    if backup_path and backup_path.exists():
        print_info(f"Attempting to restore storage file from backup: {backup_path}")
        try:
            shutil.copy2(backup_path, storage_json_path)
            print_success("Storage file successfully restored from backup.")
        except Exception as restore_e:
            print_error(f"Failed to restore storage file from backup: {restore_e}")
    return False

if __name__ == '__main__':
    print_info("Testing telemetry_manager.py...")
    dummy_storage_path = Path("test_storage.json").resolve()
    original_content = {
        "machineId": "old_machine_id_root",
        "some_other_key": "value",
        "telemetry": {
            "machineId": "old_machine_id_telemetry",
            "devDeviceId": "old_dev_device_id",
            "another_telemetry_key": "value"
        }
    }

    try:
        # Create dummy storage.json
        with open(dummy_storage_path, 'w', encoding='utf-8') as f:
            json.dump(original_content, f, indent=4)
        print_success(f"Created dummy storage file '{dummy_storage_path}' with test data.")

        # Store original IDs for comparison
        original_machine_id_root = original_content.get("machineId")
        original_machine_id_telemetry = original_content.get("telemetry", {}).get("machineId")
        original_dev_device_id = original_content.get("telemetry", {}).get("devDeviceId")

        # Test modification
        modify_result = modify_vscode_telemetry_ids(dummy_storage_path)

        if modify_result:
            print_success("Telemetry ID modification test completed successfully.")
            # Verify content
            with open(dummy_storage_path, 'r', encoding='utf-8') as f:
                updated_data = json.load(f)
            
            new_machine_id_root = updated_data.get("machineId")
            new_machine_id_telemetry = updated_data.get("telemetry", {}).get("machineId")
            new_dev_device_id = updated_data.get("telemetry", {}).get("devDeviceId")

            error_found = False
            if new_machine_id_root == original_machine_id_root:
                print_error("Verification failed: Root machineId was not updated.")
                error_found = True
            
            if new_machine_id_telemetry == original_machine_id_telemetry:
                print_error("Verification failed: telemetry.machineId was not updated.")
                error_found = True

            if new_dev_device_id == original_dev_device_id:
                print_error("Verification failed: telemetry.devDeviceId was not updated.")
                error_found = True
            
            if not error_found:
                print_success("Verification successful: Telemetry IDs appear to have been updated.")
                print_info(f"  New root machineId: {new_machine_id_root}")
                print_info(f"  New telemetry.machineId: {new_machine_id_telemetry}")
                print_info(f"  New telemetry.devDeviceId: {new_dev_device_id}")

        else:
            print_error("Telemetry ID modification test failed.")
            
    except Exception as e:
        print_error(f"Error during test setup or execution: {e}")
    finally:
        # Clean up dummy db and its backup
        if dummy_storage_path.exists():
            dummy_storage_path.unlink()
        backup_dummy_path = dummy_storage_path.with_suffix(dummy_storage_path.suffix + ".backup")
        if backup_dummy_path.exists():
            backup_dummy_path.unlink()
        print_info("telemetry_manager.py tests complete and cleaned up.")
