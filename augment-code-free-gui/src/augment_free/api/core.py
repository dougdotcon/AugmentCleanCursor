"""
Core API class for Free AugmentCode pywebview application.

This module provides the main API interface between the frontend and backend.
"""

import json
import os
import traceback
import webbrowser
from pathlib import Path
from typing import Dict, Any, Optional

from .handlers import (
    modify_telemetry_ids,
    clean_augment_data,
    clean_workspace_storage,
    modify_jetbrains_ids,
    get_jetbrains_config_dir,
    get_jetbrains_info
)
from ..utils.paths import (
    get_home_dir,
    get_app_data_dir,
    get_storage_path,
    get_db_path,
    get_machine_id_path,
    get_workspace_storage_path,
)
from ..utils.ide_detector import detect_ides, IDEDetector


class AugmentFreeAPI:
    """
    Main API class for the Free AugmentCode application.

    This class provides methods that can be called from the frontend
    to perform various operations on AugmentCode data.
    """

    def __init__(self):
        """Initialize the API."""
        self.status = "ready"
        self.editor_type = "VSCodium"  # Default editor type
        self.current_ide_info = None  # Store current IDE information
        self._config_dir = self._get_config_dir()
        self._first_run_file = self._config_dir / ".augment_free_first_run"

    def set_editor_type(self, editor_name: str, ide_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Set the editor type for operations.

        Args:
            editor_name (str): Editor name (e.g., "VSCodium", "Code", "IntelliJ IDEA")
            ide_info (dict): Optional IDE information from detection

        Returns:
            dict: Operation result
        """
        self.editor_type = editor_name
        self.current_ide_info = ide_info

        return {
            "success": True,
            "data": {
                "editor_type": self.editor_type,
                "ide_info": self.current_ide_info
            },
            "message": f"Editor type set to {editor_name}"
        }

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information and paths.

        Returns:
            dict: System information including all relevant paths
        """
        try:
            # Determine IDE type
            ide_type = "vscode"  # Default
            if self.current_ide_info:
                ide_type = self.current_ide_info.get("ide_type", "vscode")

            data = {
                "home_dir": get_home_dir(),
                "app_data_dir": get_app_data_dir(),
                "editor_type": self.editor_type,
                "ide_type": ide_type,
            }

            if ide_type == "jetbrains":
                # JetBrains IDE paths
                jetbrains_config = get_jetbrains_config_dir()
                if jetbrains_config:
                    jetbrains_info = get_jetbrains_info(jetbrains_config)
                    data.update({
                        "jetbrains_config_path": jetbrains_config,
                        "jetbrains_info": jetbrains_info,
                        "permanent_device_id_path": os.path.join(jetbrains_config, "PermanentDeviceId"),
                        "permanent_user_id_path": os.path.join(jetbrains_config, "PermanentUserId"),
                    })
                else:
                    data.update({
                        "jetbrains_config_path": "Não encontrado",
                        "permanent_device_id_path": "Não encontrado",
                        "permanent_user_id_path": "Não encontrado",
                    })
            else:
                # VSCode series paths
                data.update({
                    "storage_path": get_storage_path(self.editor_type),
                    "db_path": get_db_path(self.editor_type),
                    "machine_id_path": get_machine_id_path(self.editor_type),
                    "workspace_storage_path": get_workspace_storage_path(self.editor_type),
                })

            return {
                "success": True,
                "data": data,
                "message": "System information retrieved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve system information"
            }

    def modify_telemetry(self) -> Dict[str, Any]:
        """
        Modify telemetry IDs based on IDE type.

        Returns:
            dict: Operation result with backup information and new IDs
        """
        try:
            # Determine IDE type
            ide_type = "vscode"  # Default
            if self.current_ide_info:
                ide_type = self.current_ide_info.get("ide_type", "vscode")

            if ide_type == "jetbrains":
                # Handle JetBrains IDE
                jetbrains_config = get_jetbrains_config_dir()
                if not jetbrains_config:
                    return {
                        "success": False,
                        "error": "Diretório de configuração do JetBrains não encontrado",
                        "message": "Não foi possível encontrar o diretório de configuração do JetBrains"
                    }

                result = modify_jetbrains_ids(jetbrains_config)
                return {
                    "success": result["success"],
                    "data": result.get("data", {}),
                    "message": result.get("message", "Processamento de ID do JetBrains concluído")
                }
            else:
                # Handle VSCode series
                result = modify_telemetry_ids(self.editor_type)
                return {
                    "success": True,
                    "data": result,
                    "message": "Telemetry IDs modified successfully"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "message": "Failed to modify telemetry IDs"
            }

    def clean_database(self) -> Dict[str, Any]:
        """
        Clean augment data from SQLite database.

        Returns:
            dict: Operation result with backup information and deletion count
        """
        try:
            result = clean_augment_data(self.editor_type)
            return {
                "success": True,
                "data": result,
                "message": f"Database cleaned successfully. Deleted {result['deleted_rows']} rows."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "message": "Failed to clean database"
            }

    def clean_workspace(self) -> Dict[str, Any]:
        """
        Clean workspace storage.

        Returns:
            dict: Operation result with backup information and deletion count
        """
        try:
            result = clean_workspace_storage(self.editor_type)
            return {
                "success": True,
                "data": result,
                "message": f"Workspace cleaned successfully. Deleted {result['deleted_files_count']} files."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "message": "Failed to clean workspace"
            }

    def run_all_operations(self) -> Dict[str, Any]:
        """
        Run all cleaning operations.

        Returns:
            dict: Combined results from all operations
        """
        try:
            results = {}

            # Determine IDE type
            ide_type = "vscode"  # Default
            if self.current_ide_info:
                ide_type = self.current_ide_info.get("ide_type", "vscode")

            # Run telemetry modification
            telemetry_result = self.modify_telemetry()
            results["telemetry"] = telemetry_result

            # Run database cleaning (only for VSCode series)
            if ide_type == "vscode":
                database_result = self.clean_database()
                results["database"] = database_result
            else:
                results["database"] = {"success": True, "message": "Não aplicável para IDE JetBrains"}

            # Run workspace cleaning (only for VSCode series)
            if ide_type == "vscode":
                workspace_result = self.clean_workspace()
                results["workspace"] = workspace_result
            else:
                results["workspace"] = {"success": True, "message": "Não aplicável para IDE JetBrains"}

            # Determine overall success
            overall_success = all(
                result.get("success", False) for result in results.values()
            )

            return {
                "success": overall_success,
                "data": results,
                "message": "All operations completed"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "message": "Failed to run all operations"
            }

    def get_status(self) -> Dict[str, Any]:
        """
        Get API status.

        Returns:
            dict: Status information
        """
        return {
            "success": True,
            "data": {
                "status": self.status,
                "editor_type": self.editor_type
            },
            "message": "API is ready"
        }

    def get_version_info(self) -> Dict[str, Any]:
        """
        Get version information.

        Returns:
            dict: Version information
        """
        try:
            # Try to get version from pyproject.toml
            project_root = Path(__file__).parent.parent.parent
            pyproject_path = project_root / "pyproject.toml"

            version = "0.1.0"  # Default version

            if pyproject_path.exists():
                try:
                    import tomllib
                    with open(pyproject_path, "rb") as f:
                        data = tomllib.load(f)
                        version = data.get("project", {}).get("version", version)
                except ImportError:
                    # Fallback for Python < 3.11
                    try:
                        import tomli
                        with open(pyproject_path, "rb") as f:
                            data = tomli.load(f)
                            version = data.get("project", {}).get("version", version)
                    except ImportError:
                        pass

            return {
                "success": True,
                "data": {
                    "version": version,
                    "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
                },
                "message": "Version information retrieved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve version information"
            }

    def open_external_link(self, url: str) -> Dict[str, Any]:
        """
        Open external link in default browser.

        Args:
            url (str): URL to open

        Returns:
            dict: Operation result
        """
        try:
            webbrowser.open(url)
            return {
                "success": True,
                "message": f"Opened {url} in browser"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to open {url}"
            }

    def _get_config_dir(self) -> Path:
        """
        Get configuration directory.

        Returns:
            Path: Configuration directory path
        """
        if sys.platform == "win32":
            config_dir = Path.home() / "AppData" / "Local" / "AugmentFree"
        elif sys.platform == "darwin":
            config_dir = Path.home() / "Library" / "Application Support" / "AugmentFree"
        else:
            config_dir = Path.home() / ".config" / "AugmentFree"

        # Create directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def is_first_run(self) -> Dict[str, Any]:
        """
        Check if this is the first time running the application.

        Returns:
            dict: First run status
        """
        try:
            is_first = not self._first_run_file.exists()
            return {
                "success": True,
                "data": {
                    "is_first_run": is_first
                },
                "message": "First run status checked successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to check first run status"
            }

    def mark_first_run_complete(self) -> Dict[str, Any]:
        """
        Mark that the user has completed the first run.

        Returns:
            dict: Operation result
        """
        try:
            # Create the file to mark first run as complete
            self._first_run_file.touch()
            return {
                "success": True,
                "message": "First run marked as complete"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to mark first run as complete"
            }

    def detect_ides(self) -> Dict[str, Any]:
        """
        Detect installed IDEs.

        Returns:
            dict: Detection results
        """
        try:
            detector = IDEDetector()
            detected_ides = detector.detect_all_ides()

            return {
                "success": True,
                "data": {
                    "ides": detected_ides,
                    "count": len(detected_ides)
                },
                "message": f"Detectados {len(detected_ides)} IDEs"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Falha na detecção de IDEs: {str(e)}"
            }

    def get_default_ides(self) -> Dict[str, Any]:
        """
        Get default IDE list.

        Returns:
            dict: Default IDE list
        """
        try:
            default_ides = [
                {
                    "name": "VSCodium",
                    "display_name": "VSCodium",
                    "icon": "🔷",
                    "ide_type": "vscode"
                },
                {
                    "name": "Code",
                    "display_name": "VS Code",
                    "icon": "💙",
                    "ide_type": "vscode"
                }
            ]

            return {
                "success": True,
                "data": {
                    "ides": default_ides
                },
                "message": "Default IDEs retrieved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve default IDEs"
            }

    def get_supported_operations(self) -> Dict[str, Any]:
        """
        Get supported operations for current IDE type.

        Returns:
            dict: Supported operations
        """
        try:
            # Determine IDE type
            ide_type = "vscode"  # Default
            if self.current_ide_info:
                ide_type = self.current_ide_info.get("ide_type", "vscode")

            if ide_type == "jetbrains":
                # JetBrains operations
                operations = [
                    {
                        "id": "telemetry",
                        "name": "Redefinir Código da Máquina",
                        "description": "Redefine PermanentDeviceId e PermanentUserId",
                        "icon": "🔑",
                        "supported": True
                    },
                    {
                        "id": "database",
                        "name": "Limpar Banco de Dados",
                        "description": "Não aplicável para IDEs JetBrains",
                        "icon": "🗃️",
                        "supported": False
                    },
                    {
                        "id": "workspace",
                        "name": "Limpar Workspace",
                        "description": "Não aplicável para IDEs JetBrains",
                        "icon": "💾",
                        "supported": False
                    }
                ]
            else:
                # VSCode operations
                operations = [
                    {
                        "id": "telemetry",
                        "name": "Redefinir Código da Máquina",
                        "description": "Redefine Device ID e Machine ID",
                        "icon": "🔑",
                        "supported": True
                    },
                    {
                        "id": "database",
                        "name": "Limpar Banco de Dados",
                        "description": "Remove registros do banco SQLite",
                        "icon": "🗃️",
                        "supported": True
                    },
                    {
                        "id": "workspace",
                        "name": "Limpar Workspace",
                        "description": "Remove arquivos de armazenamento do workspace",
                        "icon": "💾",
                        "supported": True
                    }
                ]

            return {
                "success": True,
                "data": {
                    "operations": operations,
                    "ide_type": ide_type
                },
                "message": "Supported operations retrieved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve supported operations"
            }
