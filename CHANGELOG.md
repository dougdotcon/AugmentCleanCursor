# 📋 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-12-06

### 🚀 Major Changes
- **BREAKING**: Migrated from VSCode to Cursor support
- **NEW**: Added extension cleaning functionality
- **IMPROVED**: Complete visual overhaul of README.md
- **ORGANIZED**: Restructured repository with proper folder organization

### ✨ Added
- 🧩 **Extension Management**: New `clean-extensions` command to remove all Cursor extensions
- 📁 **Better Organization**: Moved scripts to `scripts/` folder and documentation to `docs/`
- 📖 **Enhanced Documentation**: 
  - Completely redesigned README.md with modern visual elements
  - Added detailed USAGE.md guide
  - Created comprehensive troubleshooting section
- 🔧 **Modern Configuration**: Added `pyproject.toml` for modern Python packaging
- 📜 **License**: Added MIT License file
- 🎯 **Better CLI**: Improved command descriptions and help text

### 🔄 Changed
- **Cursor Support**: All paths and operations now target Cursor instead of VSCode
  - Windows: `%USERPROFILE%\.cursor\extensions` for extensions
  - Windows: `%APPDATA%\Cursor\User` for user data
  - macOS: `~/Library/Application Support/Cursor/User`
  - Linux: `~/.config/Cursor/User`
- **Function Names**: 
  - `get_vscode_paths()` → `get_cursor_paths()`
  - `clean_vscode_db()` → `clean_cursor_db()`
- **All Messages**: Updated to reference Cursor instead of VSCode
- **Documentation**: Complete rewrite with modern formatting and better organization

### 🛠️ Technical Improvements
- 📦 **Repository Structure**:
  ```
  📦 augment-vip/
  ├── 📂 augment_vip/          # Main Python package
  ├── 📂 scripts/              # Installation scripts
  ├── 📂 docs/                 # Documentation
  ├── 📄 README.md             # Main documentation
  ├── 📄 LICENSE               # MIT License
  ├── 📄 pyproject.toml        # Modern Python config
  └── 📄 CHANGELOG.md          # This file
  ```
- 🔒 **Enhanced Safety**: Better error handling for extension removal
- 🎨 **Visual Improvements**: Modern badges, tables, and formatting in documentation
- 📊 **Better Feedback**: More detailed progress reporting during operations

### 🐛 Fixed
- Permission handling when Cursor is running
- Better error messages for missing directories
- Improved backup file handling

### 📚 Documentation
- 🎨 **Visual Overhaul**: Complete redesign of README.md with:
  - Modern badges and shields
  - Organized feature tables
  - Collapsible sections
  - Better code examples
  - Visual hierarchy with emojis and formatting
- 📖 **New Guides**: Added comprehensive USAGE.md with advanced examples
- 🔧 **Better Installation**: Improved installation instructions with multiple options
- 🛠️ **Troubleshooting**: Expanded troubleshooting section with common issues

---

## [1.0.0] - 2024-06-04

### ✨ Initial Release
- 🧹 **Database Cleaning**: Remove Augment-related entries from VSCode databases
- 🔐 **Telemetry Modification**: Generate new random telemetry IDs
- 🌍 **Cross-Platform**: Support for Windows, macOS, and Linux
- 💾 **Backup System**: Automatic backup creation before modifications
- 🐍 **Python-Based**: Modern Python implementation with virtual environment support
- 🎮 **CLI Interface**: Easy-to-use command-line interface
- 📦 **Easy Installation**: One-line installation scripts

### 🎯 Features
- Automatic OS detection
- SQLite database operations
- Safe backup and restore
- Color-coded output
- Error handling and rollback

---

## 📋 Legend

- 🚀 **Major Changes**: Breaking changes or significant new features
- ✨ **Added**: New features
- 🔄 **Changed**: Changes in existing functionality
- 🐛 **Fixed**: Bug fixes
- 🛠️ **Technical**: Internal improvements
- 📚 **Documentation**: Documentation changes
- 🔒 **Security**: Security improvements
- ⚡ **Performance**: Performance improvements
- 🎨 **Style**: Code style changes

---

## 🔗 Links

- [Repository](https://github.com/azrilaiman2003/augment-vip)
- [Issues](https://github.com/azrilaiman2003/augment-vip/issues)
- [Releases](https://github.com/azrilaiman2003/augment-vip/releases)
- [Documentation](docs/USAGE.md)
