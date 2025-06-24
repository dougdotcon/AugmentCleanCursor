# AugmentCode Free

[中文](README.md) | **English**

AugmentCode Free is a simple GUI tool for cleaning AugmentCode-related data, helping you avoid account bans and enjoy free AugmentCode effortlessly.

- **Auto Scan** - One-click detection of all supported IDEs installed on the system
- **Cross-Platform Support** - Compatible with Windows, macOS, Linux
- **Dynamic Adaptation** - Automatically adjusts available operations based on selected IDE type


## Interface Preview

<div align="center">

### Main Interface
![Main Interface](docs/ui2.png)

### Operation Interface
![Operation Interface](docs/ui.png)

</div>

## Features

- 🖥️ **Modern GUI Interface**
  - Cross-platform desktop application based on webview
  - Intuitive interface design
  - Real-time operation feedback

- 🔍 **Smart IDE Detection**
  - Automatically scan installed IDEs on the system
  - Support for VSCode series and JetBrains series
  - Cross-platform compatibility (Windows, macOS, Linux)
  - Dynamic operation interface adaptation

- 💙 **VSCode Series Support (VSCode, VSCodium, Cursor, etc.)**
  - Reset device ID and machine ID (Telemetry)
  - Clean specific records in SQLite database
  - Clean workspace storage files
  - Automatic backup of original data

- 🧠 **JetBrains Series Support (IDEA, PyCharm, GoLand, etc.)**
  - Reset PermanentDeviceId and PermanentUserId
  - Automatic file locking to prevent regeneration
  - Cross-platform file permission management
  - Support for all mainstream JetBrains IDEs

- 🛡️ **Security Features**
  - Automatic backup of important files before operations
  - File locking mechanism to prevent accidental modifications
  - Detailed operation logs and result feedback

## Installation

### Method 1: Download Executable ( Windows Recommended)

1. Download the latest version from [Releases](https://github.com/vagmr/Augment-free/releases) page
2. Extract and run `AugmentFree_latest.exe`

### Method 2: Run from Source

1. Ensure you have a suitable Python version installed
2. Clone this repository locally:
   ```bash
   git clone https://github.com/vagmr/Augment-free.git
   cd Augment-free
   ```
3. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -e .
   ```

## Usage

### Using Executable

1. **Log out from AugmentCode plugin**
2. **Completely exit the selected editor**
3. **Run the application**:
   - Double-click `AugmentFree_latest.exe`
   - Or run in command line: `./AugmentFree_latest.exe`
4. **Select desired operations in the GUI interface**
5. **Restart the selected editor**
6. **Log in with a new email in AugmentCode plugin**

### Running from Source

1. **Log out from AugmentCode plugin**
2. **Completely exit the selected editor**
3. **Run the application**:
   ```bash
   # Using run.py script (recommended)
   python run.py

   # Or run module directly
   python -m augment_free.main
   ```
4. **Select desired operations in the GUI interface**
5. **Restart the selected editor**
6. **Log in with a new email in AugmentCode plugin**


### Development Environment Setup

1. Fork this repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-github-username/Augment-free.git
   ```
3. Install development dependencies:
   ```bash
   uv sync --dev
   ```
4. Make your changes

## ⚠️ Disclaimer

**Use at Your Own Risk:** This tool is for educational and research purposes only. Users assume all risks associated with its use.

**Data Safety:** Please ensure important data is backed up before use. The author is not responsible for any data loss.

**Compliance:** Please comply with relevant software terms of use and local laws and regulations.

**No Warranty:** This software is provided "as is" without any express or implied warranties.

**Commercial Use:** All commercial sales are unrelated to the author. Please obtain from official channels.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.
