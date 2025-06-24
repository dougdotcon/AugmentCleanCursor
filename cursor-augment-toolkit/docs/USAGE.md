# 📖 Detailed Usage Guide

## 🎯 Command Reference

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `clean` | Clean Cursor databases | `augment-vip clean` |
| `clean-extensions` | Remove all extensions | `augment-vip clean-extensions` |
| `modify-ids` | Change telemetry IDs | `augment-vip modify-ids` |
| `all` | Run all tools | `augment-vip all` |
| `--help` | Show help | `augment-vip --help` |
| `--version` | Show version | `augment-vip --version` |

## 🔧 Advanced Usage

### Environment Variables

You can customize the behavior using environment variables:

```bash
# Custom Cursor path (if non-standard installation)
export CURSOR_USER_DIR="/custom/path/to/cursor"

# Disable backups (not recommended)
export AUGMENT_VIP_NO_BACKUP=1

# Verbose output
export AUGMENT_VIP_VERBOSE=1
```

### Batch Operations

```bash
# Run multiple commands in sequence
augment-vip clean && augment-vip clean-extensions && augment-vip modify-ids

# Or use the all command
augment-vip all
```

### Automation Scripts

#### Windows PowerShell
```powershell
# automated-cleanup.ps1
Write-Host "Starting Augment VIP cleanup..."
& .venv\Scripts\augment-vip.exe all
if ($LASTEXITCODE -eq 0) {
    Write-Host "Cleanup completed successfully!" -ForegroundColor Green
} else {
    Write-Host "Cleanup failed!" -ForegroundColor Red
}
```

#### Unix/Linux Bash
```bash
#!/bin/bash
# automated-cleanup.sh
echo "Starting Augment VIP cleanup..."
.venv/bin/augment-vip all
if [ $? -eq 0 ]; then
    echo "✅ Cleanup completed successfully!"
else
    echo "❌ Cleanup failed!"
    exit 1
fi
```

## 🛡️ Safety Features

### Backup System

All database operations create automatic backups:

```
Original: state.vscdb
Backup:   state.vscdb.backup
```

### Rollback Procedure

If something goes wrong, you can manually restore:

```bash
# Navigate to Cursor user directory
cd "%APPDATA%\Cursor\User\globalStorage"  # Windows
cd "~/Library/Application Support/Cursor/User/globalStorage"  # macOS
cd "~/.config/Cursor/User/globalStorage"  # Linux

# Restore from backup
copy state.vscdb.backup state.vscdb  # Windows
cp state.vscdb.backup state.vscdb    # Unix/Linux
```

## 🔍 Debugging

### Verbose Mode

Enable detailed logging:

```bash
# Set environment variable
export AUGMENT_VIP_VERBOSE=1
augment-vip clean

# Or use Python directly
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
augment-vip clean
```

### Log Files

Check log files for detailed information:

- Windows: `%TEMP%\augment-vip.log`
- macOS/Linux: `/tmp/augment-vip.log`

### Common Debug Commands

```bash
# Check Cursor installation
augment-vip --version

# Test database connection
python -c "
import sqlite3
from pathlib import Path
import os
db_path = Path(os.environ['APPDATA']) / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'
print(f'Database exists: {db_path.exists()}')
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM ItemTable')
    print(f'Total entries: {cursor.fetchone()[0]}')
    conn.close()
"
```

## 🎨 Customization

### Custom Scripts

You can create custom scripts that use Augment VIP:

```python
#!/usr/bin/env python3
# custom_cleanup.py

import subprocess
import sys
from pathlib import Path

def run_augment_vip(command):
    """Run augment-vip command and return success status"""
    try:
        result = subprocess.run([
            str(Path('.venv/Scripts/augment-vip.exe')),  # Windows
            command
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {command} completed successfully")
            return True
        else:
            print(f"❌ {command} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running {command}: {e}")
        return False

def main():
    """Custom cleanup routine"""
    print("🚀 Starting custom Augment VIP cleanup...")
    
    # Run commands in specific order
    commands = ['clean', 'clean-extensions', 'modify-ids']
    
    for cmd in commands:
        if not run_augment_vip(cmd):
            print(f"❌ Stopping due to failure in {cmd}")
            sys.exit(1)
    
    print("🎉 All operations completed successfully!")

if __name__ == "__main__":
    main()
```

## 📊 Performance Tips

### Faster Operations

1. **Close Cursor** before running commands
2. **Use SSD** for better I/O performance
3. **Run as administrator** to avoid permission issues
4. **Disable antivirus** temporarily for faster file operations

### Bulk Operations

For multiple Cursor installations:

```bash
# Script to clean multiple Cursor profiles
for profile in Profile1 Profile2 Profile3; do
    export CURSOR_PROFILE=$profile
    augment-vip all
done
```

## 🔗 Integration

### CI/CD Integration

#### GitHub Actions
```yaml
name: Cursor Cleanup
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2 AM

jobs:
  cleanup:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install Augment VIP
        run: |
          python scripts/install.py
      - name: Run Cleanup
        run: |
          .venv\Scripts\augment-vip.exe all
```

### Docker Integration

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN python scripts/install.py
CMD [".venv/bin/augment-vip", "all"]
```

## 🆘 Support

If you need help:

1. 📖 Check this documentation
2. 🐛 Search existing [issues](https://github.com/azrilaiman2003/augment-vip/issues)
3. 💬 Create a new issue with:
   - Operating system
   - Python version
   - Error messages
   - Steps to reproduce

## 📈 Monitoring

### Health Checks

Create a health check script:

```bash
#!/bin/bash
# health-check.sh

echo "🔍 Augment VIP Health Check"
echo "=========================="

# Check Python
python --version || echo "❌ Python not found"

# Check Augment VIP installation
.venv/bin/augment-vip --version || echo "❌ Augment VIP not installed"

# Check Cursor installation
if [ -d "$HOME/.config/Cursor" ] || [ -d "$HOME/Library/Application Support/Cursor" ] || [ -d "$APPDATA/Cursor" ]; then
    echo "✅ Cursor installation found"
else
    echo "❌ Cursor installation not found"
fi

echo "=========================="
echo "✅ Health check completed"
```
