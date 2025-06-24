"""
IDE Detection Module for Free AugmentCode.

This module provides intelligent detection of installed IDEs across different platforms.
Supports VSCode variants and JetBrains IDEs.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import json


class IDEInfo:
    """Information about a detected IDE."""

    def __init__(self, name: str, display_name: str, ide_type: str, config_path: str, icon: str = "📝"):
        self.name = name  # Internal name (e.g., "Code", "VSCodium")
        self.display_name = display_name  # Display name (e.g., "VS Code", "VSCodium")
        self.ide_type = ide_type  # "vscode" or "jetbrains"
        self.config_path = config_path  # Configuration directory path
        self.icon = icon  # Emoji icon for display

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "ide_type": self.ide_type,
            "config_path": self.config_path,
            "icon": self.icon
        }


class IDEDetector:
    """Cross-platform IDE detector."""

    def __init__(self):
        self.detected_ides: List[IDEInfo] = []

    def get_standard_directories(self) -> List[Path]:
        """Get standard directories where IDEs might store configuration."""
        dirs = []

        if sys.platform == "win32":
            # Windows
            if appdata := os.getenv("APPDATA"):
                dirs.append(Path(appdata))
            if localappdata := os.getenv("LOCALAPPDATA"):
                dirs.append(Path(localappdata))
        elif sys.platform == "darwin":
            # macOS
            home = Path.home()
            dirs.extend([
                home / "Library" / "Application Support",
                home / "Library" / "Preferences",
                home / ".config"
            ])
        else:
            # Linux and other Unix-like systems
            home = Path.home()
            dirs.extend([
                home / ".config",
                home / ".local" / "share",
                home / ".cache"
            ])

        # Add home directory as fallback
        dirs.append(Path.home())

        return [d for d in dirs if d.exists()]

    def detect_vscode_variants(self) -> List[IDEInfo]:
        """Detect VSCode and its variants."""
        vscode_variants = []

        # Known VSCode variant names and their display info
        known_variants = {
            "Code": {"display": "VS Code", "icon": "💙"},
            "VSCodium": {"display": "VSCodium", "icon": "🔷"},
            "Cursor": {"display": "Cursor", "icon": "🎯"},
            "Code - OSS": {"display": "Code - OSS", "icon": "🔶"},
            "code-oss": {"display": "Code - OSS", "icon": "🔶"},
            "Codium": {"display": "Codium", "icon": "🔷"},
            "code": {"display": "Code", "icon": "💙"},
        }

        base_dirs = self.get_standard_directories()

        for base_dir in base_dirs:
            try:
                # Scan for directories that might be VSCode variants
                for item in base_dir.iterdir():
                    if not item.is_dir():
                        continue

                    item_name = item.name

                    # Check if this looks like a VSCode variant
                    for variant_name, variant_info in known_variants.items():
                        if item_name == variant_name or item_name.lower() == variant_name.lower():
                            # Check if it has the expected VSCode structure
                            user_dir = item / "User"
                            global_storage = user_dir / "globalStorage"

                            if user_dir.exists() and global_storage.exists():
                                vscode_variants.append(IDEInfo(
                                    name=variant_name,
                                    display_name=variant_info["display"],
                                    ide_type="vscode",
                                    config_path=str(item),
                                    icon=variant_info["icon"]
                                ))
                                break
            except (PermissionError, OSError):
                # Skip directories we can't access
                continue

        return vscode_variants

    def detect_jetbrains_ides(self) -> List[IDEInfo]:
        """Detect JetBrains IDEs."""
        jetbrains_ides = []

        # Known JetBrains IDE patterns
        jetbrains_patterns = {
            "IntelliJIdea": {"display": "IntelliJ IDEA", "icon": "🧠"},
            "PyCharm": {"display": "PyCharm", "icon": "🐍"},
            "WebStorm": {"display": "WebStorm", "icon": "🚀"},
            "PhpStorm": {"display": "PhpStorm", "icon": "🐘"},
            "RubyMine": {"display": "RubyMine", "icon": "💎"},
            "CLion": {"display": "CLion", "icon": "⚙️"},
            "DataGrip": {"display": "DataGrip", "icon": "🗄️"},
            "GoLand": {"display": "GoLand", "icon": "🐹"},
            "Rider": {"display": "Rider", "icon": "🏇"},
            "AndroidStudio": {"display": "Android Studio", "icon": "🤖"},
        }

        base_dirs = self.get_standard_directories()

        for base_dir in base_dirs:
            jetbrains_dir = base_dir / "JetBrains"
            if not jetbrains_dir.exists():
                continue

            try:
                for item in jetbrains_dir.iterdir():
                    if not item.is_dir():
                        continue

                    item_name = item.name

                    # Check for JetBrains IDE patterns
                    for pattern, info in jetbrains_patterns.items():
                        if pattern.lower() in item_name.lower():
                            # Verify it's a valid JetBrains IDE directory
                            if self._is_valid_jetbrains_dir(item):
                                jetbrains_ides.append(IDEInfo(
                                    name=item_name,
                                    display_name=info["display"],
                                    ide_type="jetbrains",
                                    config_path=str(item),
                                    icon=info["icon"]
                                ))
                                break
            except (PermissionError, OSError):
                continue

        return jetbrains_ides

    def _is_valid_jetbrains_dir(self, path: Path) -> bool:
        """Check if a directory is a valid JetBrains IDE configuration directory."""
        # Look for common JetBrains configuration files/directories
        indicators = ["options", "config", "system", "plugins"]
        return any((path / indicator).exists() for indicator in indicators)

    def detect_all_ides(self) -> List[IDEInfo]:
        """Detect all supported IDEs."""
        all_ides = []

        # Detect VSCode variants
        all_ides.extend(self.detect_vscode_variants())

        # Detect JetBrains IDEs
        all_ides.extend(self.detect_jetbrains_ides())

        # Remove duplicates based on config path and display name
        seen_items = set()
        unique_ides = []
        for ide in all_ides:
            # Create a unique key combining path and display name
            unique_key = f"{ide.config_path}|{ide.display_name}"
            if unique_key not in seen_items:
                seen_items.add(unique_key)
                unique_ides.append(ide)

        # Mecanismo de desduplicação robusto: filtro final baseado em display_name
        final_unique_ides = []
        seen_display_names = set()
        for ide in unique_ides:
            if ide.display_name not in seen_display_names:
                seen_display_names.add(ide.display_name)
                final_unique_ides.append(ide)

        # Sort by IDE type and name
        final_unique_ides.sort(key=lambda x: (x.ide_type, x.display_name))

        self.detected_ides = final_unique_ides
        return final_unique_ides

    def get_default_ides(self) -> List[IDEInfo]:
        """Get the default IDE list (VSCodium and VS Code)."""
        return [
            IDEInfo("VSCodium", "VSCodium", "vscode", "", "🔷"),
            IDEInfo("Code", "VS Code", "vscode", "", "💙")
        ]


def detect_ides() -> Dict[str, Any]:
    """
    Main function to detect IDEs.

    Returns:
        dict: Detection results with IDE list and summary
    """
    try:
        detector = IDEDetector()
        detected_ides = detector.detect_all_ides()

        return {
            "success": True,
            "ides": [ide.to_dict() for ide in detected_ides],
            "count": len(detected_ides),
            "message": f"Detectados {len(detected_ides)} IDEs"
        }
    except Exception as e:
        return {
            "success": False,
            "ides": [],
            "count": 0,
            "message": f"Falha na detecção: {str(e)}"
        }


if __name__ == "__main__":
    # Test the detector
    result = detect_ides()
    print(json.dumps(result, indent=2, ensure_ascii=False))
