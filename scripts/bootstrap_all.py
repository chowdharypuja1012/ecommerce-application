#!/usr/bin/env python3
"""
Bootstrap Script for Sweet Sentiments (E-Commerce Platform)
Automates end-to-end setup:
1. Environment validation (Python 3.10+, Node.js/npm)
2. Python dependency installation (requirements.txt)
3. Frontend dependency installation (npm install)
4. Database migrations across all 7 microservices
5. Catalogue data seeding (21 products + 6 categories + image assets)
6. Superuser admin account provisioning (admin / admin123)
"""

import sys
import os
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

SERVICES = [
    "accounts",
    "catalogue",
    "cart",
    "wishlist",
    "orders",
    "payments",
    "reviews",
]

def run_cmd(cmd, cwd=ROOT_DIR, description=""):
    print(f"\n🌸 [{description or 'Running'}] -> {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str))
    if res.returncode != 0:
        print(f"❌ Error while executing: {description}")
        return False
    return True

def main():
    print("=" * 65)
    print("  🌸 SWEET SENTIMENTS — AUTOMATED REPOSITORY BOOTSTRAP 🌸")
    print("=" * 65)

    # 1. Environment Checks
    print("\n🔍 Step 1: Checking environment...")
    py_ver = sys.version_info
    print(f"  • Python Version: {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    if py_ver.major < 3 or (py_ver.major == 3 and py_ver.minor < 10):
        print("  ⚠️ Warning: Python 3.10+ is recommended.")

    # Check npm
    try:
        npm_ver = subprocess.check_output(["npm", "-v"], shell=True).decode().strip()
        print(f"  • Node.js npm Version: {npm_ver}")
    except Exception:
        print("  ⚠️ npm not found in PATH. Make sure Node.js is installed for the frontend.")

    # 2. Install Python Dependencies
    req_file = ROOT_DIR / "requirements.txt"
    if req_file.exists():
        run_cmd([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], description="Installing Python dependencies")

    # 3. Install Frontend Dependencies
    frontend_dir = ROOT_DIR / "frontend"
    if frontend_dir.exists() and (frontend_dir / "package.json").exists():
        run_cmd("npm install", cwd=frontend_dir, description="Installing Frontend dependencies")

    # 4. Run Migrations for all Microservices
    print("\n🗄️ Step 4: Running migrations for all 7 microservices...")
    for s in SERVICES:
        manage_py = ROOT_DIR / "services" / s / "manage.py"
        if manage_py.exists():
            run_cmd([sys.executable, str(manage_py), "migrate"], description=f"Migrating {s} service")

    # 5. Seed Catalogue Data (21 products + 6 categories)
    cat_manage = ROOT_DIR / "services" / "catalogue" / "manage.py"
    if cat_manage.exists():
        run_cmd([sys.executable, str(cat_manage), "seed_data"], description="Seeding Sweet Sentiments product catalogue")

    # 6. Setup Admin Superusers
    admin_setup = ROOT_DIR / "setup_admins.py"
    if admin_setup.exists():
        run_cmd([sys.executable, str(admin_setup)], description="Creating admin superuser accounts")

    print("\n" + "=" * 65)
    print("  ✨ BOOTSTRAP COMPLETE! ✨")
    print("=" * 65)
    print("You can now start the application:")
    print("  • Frontend: cd frontend && npm run dev (http://localhost:5173)")
    print("  • Gateway:  python gateway/manage.py runserver 8000")
    print("  • Services: python services/<service_name>/manage.py runserver 8001-8007")
    print("  • Admin:    admin / admin123 (e.g. http://localhost:8002/admin/)")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
