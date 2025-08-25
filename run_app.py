#!/usr/bin/env python3
"""
Startup script for FastAPI User Management System
Run this script to start either the backend or frontend
"""

import subprocess
import sys
import os
import time

def run_backend():
    """Start the FastAPI backend server"""
    print("Starting FastAPI Backend Server...")
    print("Server will be available at: http://localhost:8001")
    print("API Documentation: http://localhost:8001/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the FastAPI server
        subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"])
    except KeyboardInterrupt:
        print("\nBackend server stopped")
    except Exception as e:
        print(f"Error starting backend: {e}")

def run_frontend():
    """Start the Streamlit frontend"""
    print("Starting Streamlit Frontend...")
    print("Frontend will be available at: http://localhost:8502")
    print("Press Ctrl+C to stop the frontend")
    print("-" * 50)
    
    try:
        # Start the Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend.py", "--server.port", "8502"])
    except KeyboardInterrupt:
        print("\nFrontend stopped")
    except Exception as e:
        print(f"Error starting frontend: {e}")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ["fastapi", "uvicorn", "streamlit", "requests", "pandas"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main function"""
    print("FastAPI User Management System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\nChoose an option:")
    print("1. Start Backend (FastAPI)")
    print("2. Start Frontend (Streamlit)")
    print("3. Start Both (Backend + Frontend)")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                run_backend()
                break
            elif choice == "2":
                run_frontend()
                break
            elif choice == "3":
                print("\nStarting both backend and frontend...")
                print("Backend: http://localhost:8001")
                print("Frontend: http://localhost:8502")
                print("API Docs: http://localhost:8001/docs")
                print("\nStarting backend in 3 seconds...")
                time.sleep(3)
                
                # Start backend in background
                backend_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"])
                
                print("Backend started successfully!")
                print("Starting frontend in 3 seconds...")
                time.sleep(3)
                
                # Start frontend
                try:
                    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend.py", "--server.port", "8502"])
                except KeyboardInterrupt:
                    print("\nFrontend stopped")
                finally:
                    print("Stopping backend...")
                    backend_process.terminate()
                    backend_process.wait()
                    print("Backend stopped")
                break
            elif choice == "4":
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
