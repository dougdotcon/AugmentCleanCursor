# Augment VIP (Python Version)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

A utility toolkit for Augment VIP users, providing tools to manage and clean VS Code databases. This is the Python version, which offers better cross-platform compatibility and eliminates the need for external dependencies.

## 🚀 Features

- **Database Cleaning**: Remove Augment-related entries from VS Code databases
- **Telemetry ID Modification**: Generate random telemetry IDs for VS Code to enhance privacy
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Python-Based**: Uses Python for better cross-platform compatibility
- **Virtual Environment**: Isolates dependencies to avoid conflicts
- **Safe Operations**: Creates backups before making any changes
- **User-Friendly**: Clear, color-coded output and detailed status messages

## 📋 Requirements

- Python 3.6 or higher
- No external system dependencies required (all managed through Python)

## 💻 Installation

### Quick Install

Run the installer script:

```bash
# On macOS/Linux
python3 install.py

# On Windows
python install.py
```

### Installation Options

```bash
# Install and run database cleaning
python install.py --clean

# Install and modify telemetry IDs
python install.py --modify-ids

# Install and run all tools
python install.py --all
```

### Manual Installation

If you prefer to set up manually:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# Install the package
pip install -e .
```

## 🔧 Usage

### Clean VS Code Databases

To remove Augment-related entries from VS Code databases:

```bash
# If using the virtual environment
.venv/bin/augment-vip clean  # macOS/Linux
.venv\Scripts\augment-vip clean  # Windows

# If installed globally
augment-vip clean
```

This will:
- Detect your operating system
- Find VS Code database files
- Create backups of each database
- Remove entries containing "augment" from the databases
- Report the results

### Modify VS Code Telemetry IDs

To change the telemetry IDs in VS Code's storage.json file:

```bash
# If using the virtual environment
.venv/bin/augment-vip modify-ids  # macOS/Linux
.venv\Scripts\augment-vip modify-ids  # Windows

# If installed globally
augment-vip modify-ids
```

This will:
- Locate the VS Code storage.json file
- Generate a random 64-character hex string for machineId
- Generate a random UUID v4 for devDeviceId
- Create a backup of the original file
- Update the file with the new random values

### Run All Tools

To run both tools at once:

```bash
# If using the virtual environment
.venv/bin/augment-vip all  # macOS/Linux
.venv\Scripts\augment-vip all  # Windows

# If installed globally
augment-vip all
```

## 📁 Project Structure

```
augment-vip/
├── .venv/                  # Virtual environment (created during installation)
├── augment_vip/            # Main package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface
│   ├── db_cleaner.py       # Database cleaning functionality
│   ├── id_modifier.py      # Telemetry ID modification functionality
│   └── utils.py            # Utility functions
├── install.py              # Installation script
├── README.md               # This file
├── requirements.txt        # Package dependencies
└── setup.py                # Package setup script
```

## 🔍 How It Works

The database cleaning tool works by:

1. **Finding Database Locations**: Automatically detects the correct paths for VS Code databases based on your operating system.

2. **Creating Backups**: Before making any changes, the tool creates a backup of each database file.

3. **Cleaning Databases**: Uses SQLite commands to remove entries containing "augment" from the databases.

4. **Reporting Results**: Provides detailed feedback about the operations performed.

## 🛠️ Troubleshooting

### Common Issues

**Python Not Found**
```
'python' is not recognized as an internal or external command
```
Make sure Python is installed and added to your PATH.

**Permission Denied**
```
Permission denied
```
On macOS/Linux, you may need to make the scripts executable:
```bash
chmod +x install.py
```

**Virtual Environment Creation Failed**
```
Error: Command '['/path/to/.venv/bin/python', '-m', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1
```
Try installing the venv module:
```bash
# On Ubuntu/Debian
sudo apt install python3-venv

# On Fedora/RHEL
sudo dnf install python3-venv
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

Azril Aiman - me@azrilaiman.my

Project Link: [https://github.com/azrilaiman2003/augment-vip](https://github.com/azrilaiman2003/augment-vip)

---

Made with ❤️ by [Azril Aiman](https://github.com/azrilaiman2003)
