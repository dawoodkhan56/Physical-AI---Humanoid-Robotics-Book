"""
Integration verification script for the RAG chatbot system.
This script verifies that all necessary files exist and are properly structured.
"""
import sys
import os
from pathlib import Path
import json

def check_backend_files():
    """Check if all necessary backend files exist"""
    print("Checking backend files...")
    backend_dir = Path("backend")

    required_files = [
        "main.py",
        "requirements.txt",
        "ingest_pipeline.py",
        "advanced_endpoints.py",
        ".env"
    ]

    all_found = True
    for file in required_files:
        file_path = backend_dir / file
        if file_path.exists():
            print(f"  [OK] {file}")
        else:
            print(f"  [MISSING] {file}")
            all_found = False

    return all_found

def check_frontend_files():
    """Check if all necessary frontend files exist"""
    print("\nChecking frontend files...")
    frontend_checks = [
        Path("website/src/components/BookChatbot.jsx"),
        Path("website/src/css/chatbot.css"),
        Path("website/src/theme/Layout/index.js"),
    ]

    all_found = True
    for file_path in frontend_checks:
        if file_path.exists():
            print(f"  [OK] {file_path}")
        else:
            print(f"  [MISSING] {file_path}")
            all_found = False

    # Check package.json for necessary dependencies
    package_json_path = Path("website/package.json")
    if package_json_path.exists():
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            dependencies = package_data.get('dependencies', {})
            dev_dependencies = package_data.get('devDependencies', {})

            # Check for react dependency (needed for our component)
            has_react = 'react' in dependencies or 'react' in dev_dependencies
            if has_react:
                print("  [OK] React dependency found")
            else:
                print("  [WARNING] React dependency not found (might cause issues)")

        except Exception as e:
            print(f"  [WARNING] Could not check dependencies: {e}")
    else:
        print("  [WARNING] package.json not found")

    return all_found

def check_content_ingested():
    """Check if content has been ingested (by checking if collection likely exists)"""
    print("\nChecking content ingestion...")

    # Check if the ingestion script exists
    ingest_script = Path("backend/ingest_pipeline.py")
    if ingest_script.exists():
        print("  [OK] Ingestion script found")
    else:
        print("  [MISSING] Ingestion script not found")
        return False

    # In a real scenario, we would connect to Qdrant to check if content exists
    # For now, we'll assume if the script exists, content can be ingested
    print("  [INFO] Content ingestion can be performed using the ingestion script")
    return True

def main():
    print("Verifying RAG Chatbot Integration")
    print("="*60)

    backend_ok = check_backend_files()
    frontend_ok = check_frontend_files()
    ingestion_ok = check_content_ingested()

    print("\n" + "="*60)
    print("INTEGRATION VERIFICATION RESULTS")
    print("="*60)
    print(f"Backend files: {'OK' if backend_ok else 'MISSING FILES'}")
    print(f"Frontend files: {'OK' if frontend_ok else 'MISSING FILES'}")
    print(f"Ingestion capability: {'OK' if ingestion_ok else 'ISSUE'}")

    all_ok = backend_ok and frontend_ok and ingestion_ok

    if all_ok:
        print(f"\nAll files are in place for the RAG chatbot system!")
        print("\nTo run the full system:")
        print("1. Set up your environment variables in backend/.env")
        print("2. Run the ingestion to populate your vector database:")
        print("   cd backend")
        print("   python ingest_pipeline.py")
        print("3. Start the backend server:")
        print("   cd backend")
        print("   python -m uvicorn main:app --reload")
        print("4. In another terminal, start the frontend:")
        print("   cd website")
        print("   npm run start")
        print("5. Visit http://localhost:3000 and use the chatbot!")
    else:
        print(f"\nSome components are missing. Please check the above errors.")

    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)