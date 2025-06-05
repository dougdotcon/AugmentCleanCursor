"""
Command-line interface for Augment VIP
"""

import os
import sys
import click
from pathlib import Path

from . import __version__
from .utils import info, success, error, warning
from .db_cleaner import clean_cursor_db, clean_cursor_extensions
from .id_modifier import modify_telemetry_ids

@click.group()
@click.version_option(version=__version__)
def cli():
    """Augment VIP - Tools for managing Cursor settings"""
    pass

@cli.command()
def clean():
    """Clean Cursor databases by removing Augment-related entries"""
    if clean_cursor_db():
        success("Database cleaning completed successfully")
    else:
        error("Database cleaning failed")
        sys.exit(1)

@cli.command()
def clean_extensions():
    """Clean Cursor extensions directory by removing all extensions"""
    if clean_cursor_extensions():
        success("Extensions cleaning completed successfully")
    else:
        error("Extensions cleaning failed")
        sys.exit(1)

@cli.command()
def modify_ids():
    """Modify Cursor telemetry IDs"""
    if modify_telemetry_ids():
        success("Telemetry ID modification completed successfully")
    else:
        error("Telemetry ID modification failed")
        sys.exit(1)

@cli.command()
def all():
    """Run all tools (clean database, clean extensions, and modify IDs)"""
    info("Running all tools...")

    clean_db_result = clean_cursor_db()
    clean_ext_result = clean_cursor_extensions()
    modify_result = modify_telemetry_ids()

    if clean_db_result and clean_ext_result and modify_result:
        success("All operations completed successfully")
    else:
        error("Some operations failed")
        sys.exit(1)

@cli.command()
def install():
    """Install Augment VIP"""
    info("Installing Augment VIP...")

    # This is a placeholder for any installation steps
    # In Python, most of the installation is handled by pip/setup.py

    success("Augment VIP installed successfully")
    info("You can now use the following commands:")
    info("  - augment-vip clean: Clean Cursor databases")
    info("  - augment-vip clean-extensions: Clean Cursor extensions")
    info("  - augment-vip modify-ids: Modify telemetry IDs")
    info("  - augment-vip all: Run all tools")

def main():
    """Main entry point for the CLI"""
    try:
        cli()
    except Exception as e:
        error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
