# coding: utf-8
"""
Build script for Free AugmentCode.
Creates a standalone executable using PyInstaller.
"""

import sys
import shutil
import platform
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

try:
    import PyInstaller.__main__
except ImportError:
    print("[ERROR] PyInstaller not found. Installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    import PyInstaller.__main__


def move_to_release(exe_path):
    """Move the built executable to the release folder with timestamp."""
    print("[INFO] Moving executable to release folder...")

    # Create release folder if it doesn't exist
    release_dir = project_root / "release"
    release_dir.mkdir(exist_ok=True)

    # Generate filename with timestamp and platform info
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_info = get_version_info()
    current_platform = platform.system().lower()

    print(f"[DEBUG] Version info: {version_info}")
    print(f"[DEBUG] Current platform: {current_platform}")

    # Determine file extension based on platform
    if current_platform == "windows":
        ext = ".exe"
        platform_suffix = "windows"
    elif current_platform == "darwin":
        ext = ""
        platform_suffix = "macos"
    else:
        ext = ""
        platform_suffix = "linux"

    if version_info:
        release_filename = f"AugmentFree_v{version_info}_{platform_suffix}_{timestamp}{ext}"
    else:
        release_filename = f"AugmentFree_{platform_suffix}_{timestamp}{ext}"

    release_path = release_dir / release_filename

    try:
        # Copy the file to release folder
        shutil.copy2(exe_path, release_path)
        print(f"[SUCCESS] Executable moved to: {release_path}")

        # Also create a "latest" copy for convenience
        latest_filename = f"AugmentFree_latest_{platform_suffix}{ext}"
        latest_path = release_dir / latest_filename
        shutil.copy2(exe_path, latest_path)
        print(f"[INFO] Latest copy created: {latest_path}")

        # Show release folder contents
        print("\n[INFO] Release folder contents:")
        # Look for both .exe files (Windows) and files without extension (macOS/Linux)
        patterns = ["*.exe", "AugmentFree_*"] if current_platform == "windows" else ["AugmentFree_*"]
        all_files = []
        for pattern in patterns:
            all_files.extend(release_dir.glob(pattern))

        for file in sorted(set(all_files)):
            if file.is_file():
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"   {file.name} ({size_mb:.1f} MB)")

    except Exception as e:
        print(f"[ERROR] Failed to move executable: {e}")


def get_version_info():
    """Get version information from pyproject.toml."""
    try:
        pyproject_file = project_root / "pyproject.toml"
        if pyproject_file.exists():
            with open(pyproject_file, "r", encoding="utf-8") as f:
                content = f.read()
                # Use regex to extract version more reliably
                import re
                match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)
    except Exception as e:
        print(f"[WARNING] Failed to parse version: {e}")
    return None


def main():
    """Build the application."""
    print("[INFO] Building Free AugmentCode...")

    # Paths
    main_script = project_root / "src" / "augment_free" / "main.py"
    web_dir = project_root / "src" / "augment_free" / "web"
    requirements_file = project_root / "requirements.txt"

    # Get current platform
    current_platform = platform.system().lower()

    # Choose icon file based on platform
    if current_platform == "windows":
        icon_file = project_root / "app.ico"
    elif current_platform == "darwin":
        icon_file = project_root / "app.icns"
    else:
        icon_file = project_root / "app.ico"  # Default to .ico for Linux

    # PyInstaller command
    cmd = [
        str(main_script),
        "--name=AugmentFree",
        "--clean",  # Clean PyInstaller cache
        "--onefile",  # Create single executable
        "--noconfirm",  # Replace output without asking
        "--distpath=./dist",  # Output directory
    ]

    # Platform-specific data inclusion
    if current_platform == "windows":
        cmd.extend([
            f"--add-data={web_dir};web",  # Include web files (Windows)
            "--noconsole",  # Hide console window (Windows)
        ])
    else:
        cmd.extend([
            f"--add-data={web_dir}:web",  # Include web files (macOS/Linux)
            "--windowed",  # Hide console window (macOS/Linux)
        ])

    # Add icon if it exists
    if icon_file.exists():
        cmd.append(f"--icon={icon_file}")  # Set application icon

        # Platform-specific icon data inclusion
        if current_platform == "windows":
            cmd.append(f"--add-data={icon_file};.")  # Include icon file in bundle (Windows)
        else:
            cmd.append(f"--add-data={icon_file}:.")  # Include icon file in bundle (macOS/Linux)

        print(f"[INFO] Adding icon: {icon_file}")
    else:
        print("[WARNING] Icon file not found, building without icon")

    # Add hidden imports from requirements.txt
    if requirements_file.exists():
        print("[INFO] Adding dependencies from requirements.txt...")
        with open(requirements_file, "r", encoding="utf-8") as reader:
            for line in reader:
                line = line.strip()
                if line and not line.startswith("#") and "==" in line:
                    package = line.split("==")[0].strip()
                    cmd.append(f"--hidden-import={package}")
                    print(f"   Added: {package}")

    # Additional hidden imports for pywebview and our modules
    additional_imports = [
        "webview",
        "webview.platforms.winforms",
        "webview.platforms.cef",
        "webview.platforms.edgechromium",
        "bottle",
        "jinja2",
        # Our project modules
        "augment_free",
        "augment_free.api",
        "augment_free.api.core",
        "augment_free.api.handlers",
        "augment_free.api.handlers.database",
        "augment_free.api.handlers.telemetry",
        "augment_free.api.handlers.workspace",
        "augment_free.utils",
        "augment_free.utils.device_codes",
        "augment_free.utils.paths",
    ]

    for imp in additional_imports:
        cmd.append(f"--hidden-import={imp}")

    print("[INFO] Running PyInstaller...")
    print(f"Command: {' '.join(cmd)}")

    try:
        PyInstaller.__main__.run(cmd)
        print("[SUCCESS] Build completed successfully!")

        # Move to release folder
        if current_platform == "windows":
            dist_exe = project_root / "dist" / "AugmentFree.exe"
        else:
            dist_exe = project_root / "dist" / "AugmentFree"

        if dist_exe.exists():
            move_to_release(dist_exe)
        else:
            print(f"[WARNING] Executable not found in dist folder: {dist_exe}")

    except Exception as e:
        print(f"[ERROR] Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()