#!/usr/bin/env python3
"""
check-deps.py — Detect source file types and install required Python dependencies.
Run this at Phase 0 before any data extraction.

Usage: python3 check-deps.py [directory]
  directory: path to scan for source files (default: current directory)
"""

import sys
import os
import importlib.util
import subprocess
from pathlib import Path

# Map file extensions to required packages
DEPENDENCY_MAP = {
    '.xlsx': ('openpyxl', 'openpyxl'),       # (pip name, import name)
    '.xls': ('openpyxl', 'openpyxl'),
    '.pptx': ('python-pptx', 'pptx'),
    '.ppt': ('python-pptx', 'pptx'),
    '.png': ('Pillow', 'PIL'),
    '.jpg': ('Pillow', 'PIL'),
    '.jpeg': ('Pillow', 'PIL'),
    '.webp': ('Pillow', 'PIL'),
    '.gif': ('Pillow', 'PIL'),
    '.bmp': ('Pillow', 'PIL'),
}

# Always needed for PDF export
PDF_DEPS = [('websocket-client', 'websocket')]

def scan_directory(directory):
    """Scan directory for source files and return detected extensions."""
    extensions = set()
    path = Path(directory)
    for f in path.rglob('*'):
        if f.is_file():
            ext = f.suffix.lower()
            if ext in DEPENDENCY_MAP:
                extensions.add(ext)
    return extensions

def check_installed(import_name):
    """Check if a Python package is importable."""
    return importlib.util.find_spec(import_name) is not None

def install_package(pip_name):
    """Install a package via pip3."""
    print(f'  Installing {pip_name}...')
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', pip_name, '-q'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f'  ERROR: Failed to install {pip_name}')
        print(f'  {result.stderr.strip()}')
        return False
    print(f'  OK: {pip_name} installed')
    return True

def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'

    if not os.path.isdir(directory):
        print(f'Error: {directory} is not a valid directory')
        sys.exit(1)

    print(f'Scanning {os.path.abspath(directory)} for source files...\n')

    extensions = scan_directory(directory)

    if not extensions:
        print('No recognized source files found.')
        print('Supported: .xlsx, .pptx, .csv, .json, .sqlite, .png, .jpg, .webp')
    else:
        print(f'Detected file types: {", ".join(sorted(extensions))}\n')

    # Collect required packages
    needed = {}
    for ext in extensions:
        if ext in DEPENDENCY_MAP:
            pip_name, import_name = DEPENDENCY_MAP[ext]
            needed[pip_name] = import_name

    # Always check PDF export deps
    for pip_name, import_name in PDF_DEPS:
        needed[pip_name] = import_name

    # Check and install
    missing = []
    installed = []

    for pip_name, import_name in needed.items():
        if check_installed(import_name):
            installed.append(pip_name)
        else:
            missing.append((pip_name, import_name))

    if installed:
        print(f'Already installed: {", ".join(installed)}')

    if missing:
        print(f'\nMissing packages: {", ".join(p for p, _ in missing)}')
        print('Installing...\n')

        failed = []
        for pip_name, import_name in missing:
            if not install_package(pip_name):
                failed.append(pip_name)

        if failed:
            print(f'\nFailed to install: {", ".join(failed)}')
            print('Please install manually: pip3 install ' + ' '.join(failed))
            sys.exit(1)
        else:
            print('\nAll dependencies installed successfully.')
    else:
        print('\nAll dependencies are already installed.')

    print('\nReady for data extraction.')

if __name__ == '__main__':
    main()
