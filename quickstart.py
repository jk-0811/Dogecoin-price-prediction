#!/usr/bin/env python
"""
Quick Start Script - Dogecoin Price Prediction
Run this to get the project running immediately
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command with error handling"""
    print(f"\n▸ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"  ✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ {description} failed")
        print(f"    Error: {e.stderr}")
        return False

def main():
    """Main setup flow"""
    
    print("""
    ╭─────────────────────────────────────────────────────────╮
    │  🚀 DOGECOIN PRICE PREDICTION - QUICK START             │
    │     Machine Learning Model with Django                  │
    ╰─────────────────────────────────────────────────────────╯
    """)
    
    base_dir = Path(__file__).resolve().parent
    
    # Step 1: Check Python version
    print(f"\n[1/4] Checking Python version...")
    if sys.version_info < (3, 8):
        print(f"  ✗ Python 3.8+ required (you have {sys.version})")
        return False
    print(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Step 2: Create venv
    print(f"\n[2/4] Setting up virtual environment...")
    venv_path = base_dir / ".venv"
    if venv_path.exists():
        print(f"  ⓘ Virtual environment already exists")
    else:
        if not run_command(f"{sys.executable} -m venv .venv", "Creating virtual environment"):
            return False
    
    # Step 3: Install dependencies
    print(f"\n[3/4] Installing dependencies...")
    if sys.platform == "win32":
        activate_cmd = ".venv\\Scripts\\pip"
    else:
        activate_cmd = ".venv/bin/pip"
    
    if not run_command(f"{activate_cmd} install -r requirements.txt", "Installing packages"):
        return False
    
    # Step 4: Train model
    print(f"\n[4/4] Training ML model...")
    if sys.platform == "win32":
        python_cmd = ".venv\\Scripts\\python"
    else:
        python_cmd = ".venv/bin/python"
    
    if not run_command(f"{python_cmd} prediction/ml/train.py", "Training model"):
        print("\n  ⚠️  Model training failed. You can retry with:")
        print(f"     {python_cmd} prediction/ml/train.py")
    
    # Success!
    print(f"""
    
    ╭─────────────────────────────────────────────────────────╮
    │  ✓ SETUP COMPLETE!                                      │
    ╰─────────────────────────────────────────────────────────╯
    
    🚀 To start the server:
    
       Activate venv:
       - Windows: .venv\\Scripts\\activate
       - macOS/Linux: source .venv/bin/activate
       
       Run server:
       python manage.py runserver
       
    🌐 Then open: http://localhost:8000
    
    ℹ️  For API testing:
       python test_api.py
    
    📖 Read README.md for full documentation
    
    """)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
