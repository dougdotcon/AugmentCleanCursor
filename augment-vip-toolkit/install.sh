#!/usr/bin/env bash
#
# install.sh
#
# Description: Installation script for the Augment VIP project (Python version)
# This script downloads and runs the Python-based installer
#
# Usage: ./install.sh [options]
#   Options:
#     --help          Show this help message
#     --clean         Run database cleaning script after installation
#     --modify-ids    Run telemetry ID modification script after installation
#     --all           Run all scripts (clean and modify IDs)

set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error

# Text formatting
BOLD="\033[1m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
RESET="\033[0m"

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${RESET} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${RESET} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${RESET} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${RESET} $1"
}

# Repository information
REPO_URL="https://raw.githubusercontent.com/azrilaiman2003/augment-vip/main"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check for Python
check_python() {
    log_info "Checking for Python..."

    # Try python3 first, then python as fallback
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        log_success "Found Python 3: $(python3 --version)"
    elif command -v python &> /dev/null; then
        # Check if python is Python 3
        PYTHON_VERSION=$(python --version 2>&1)
        if [[ $PYTHON_VERSION == *"Python 3"* ]]; then
            PYTHON_CMD="python"
            log_success "Found Python 3: $PYTHON_VERSION"
        else
            log_error "Python 3 is required but found: $PYTHON_VERSION"
            log_info "Please install Python 3.6 or higher from https://www.python.org/downloads/"
            exit 1
        fi
    else
        log_error "Python 3 is not installed or not in PATH"
        log_info "Please install Python 3.6 or higher from https://www.python.org/downloads/"
        exit 1
    fi
}

# Download Python installer
download_python_installer() {
    log_info "Downloading Python installer..."

    # Create a project directory for standalone installation
    PROJECT_ROOT="$SCRIPT_DIR/augment-vip"
    log_info "Creating project directory at: $PROJECT_ROOT"
    mkdir -p "$PROJECT_ROOT"

    # Download the Python installer
    INSTALLER_URL="$REPO_URL/install.py"
    INSTALLER_PATH="$PROJECT_ROOT/install.py"

    log_info "Downloading from: $INSTALLER_URL"
    log_info "Saving to: $INSTALLER_PATH"

    # Use -L to follow redirects
    if curl -L "$INSTALLER_URL" -o "$INSTALLER_PATH"; then
        log_success "Downloaded Python installer"
    else
        log_error "Failed to download Python installer"
        exit 1
    fi

    # Make it executable
    chmod +x "$INSTALLER_PATH"

    # Download the Python package files
    log_info "Downloading Python package files..."

    # Create package directories
    mkdir -p "$PROJECT_ROOT/augment_vip"

    # List of Python files to download
    PYTHON_FILES=(
        "augment_vip/__init__.py"
        "augment_vip/utils.py"
        "augment_vip/db_cleaner.py"
        "augment_vip/id_modifier.py"
        "augment_vip/cli.py"
        "setup.py"
        "requirements.txt"
    )

    # Download each file
    for file in "${PYTHON_FILES[@]}"; do
        file_url="$REPO_URL/$file"
        file_path="$PROJECT_ROOT/$file"

        # Create directory if needed
        mkdir -p "$(dirname "$file_path")"

        log_info "Downloading $file..."

        # Use -L to follow redirects
        if curl -L "$file_url" -o "$file_path"; then
            log_success "Downloaded $file"
        else
            log_warning "Failed to download $file, will try to continue anyway"
        fi
    done

    log_success "All Python files downloaded"
    return 0
}

# Run Python installer
run_python_installer() {
    log_info "Running Python installer..."

    # Change to the project directory
    cd "$PROJECT_ROOT"

    # Run the Python installer with the provided arguments
    if "$PYTHON_CMD" install.py "$@"; then
        log_success "Python installation completed successfully"
    else
        log_error "Python installation failed"
        exit 1
    fi

    # Return to the original directory
    cd - > /dev/null
}

# Display help message
show_help() {
    echo "Augment VIP Installation Script (Python Version)"
    echo
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  --help          Show this help message"
    echo "  --clean         Run database cleaning script after installation"
    echo "  --modify-ids    Run telemetry ID modification script after installation"
    echo "  --all           Run all scripts (clean and modify IDs)"
    echo
    echo "Example: $0 --all"
}

# Main installation function
main() {
    # Parse command line arguments for help
    for arg in "$@"; do
        if [[ "$arg" == "--help" ]]; then
            show_help
            exit 0
        fi
    done

    log_info "Starting installation process for Augment VIP (Python Version)"

    # Check for Python
    check_python

    # Download Python installer
    download_python_installer

    # Run Python installer with all arguments passed to this script plus --no-prompt
    run_python_installer "$@" --no-prompt

    # Get the path to the augment-vip command
    if [ "$PYTHON_CMD" = "python3" ]; then
        AUGMENT_CMD="$PROJECT_ROOT/.venv/bin/augment-vip"
    else
        if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
            AUGMENT_CMD="$PROJECT_ROOT/.venv/Scripts/augment-vip.exe"
        else
            AUGMENT_CMD="$PROJECT_ROOT/.venv/bin/augment-vip"
        fi
    fi

    # Prompt user to clean database
    echo
    read -p "Would you like to clean VS Code databases now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Running database cleaning..."
        "$AUGMENT_CMD" clean
    fi

    # Prompt user to modify telemetry IDs
    echo
    read -p "Would you like to modify VS Code telemetry IDs now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Running telemetry ID modification..."
        "$AUGMENT_CMD" modify-ids
    fi

    log_info "You can now use Augment VIP with the following commands:"
    log_info "  $AUGMENT_CMD clean       - Clean VS Code databases"
    log_info "  $AUGMENT_CMD modify-ids  - Modify telemetry IDs"
    log_info "  $AUGMENT_CMD all         - Run all tools"
}

# Execute main function
main "$@"
