#!/usr/bin/env python3
"""
Force reset RAG system - handles Windows file locking issues
"""

import shutil
import os
import time
from pathlib import Path

def force_reset_rag():
    """Force reset the RAG system, handling file locks"""
    print("=== FORCE RESETTING RAG SYSTEM ===")
    
    # Remove existing vector database with retry logic
    vector_db_path = "./vector_db"
    if os.path.exists(vector_db_path):
        print(f"Attempting to remove vector database: {vector_db_path}")
        
        # Try multiple times with delays
        for attempt in range(5):
            try:
                shutil.rmtree(vector_db_path)
                print("✅ Vector database removed successfully")
                break
            except PermissionError as e:
                print(f"⚠️  Attempt {attempt + 1}: File is locked, waiting...")
                if attempt < 4:
                    time.sleep(2)  # Wait 2 seconds before retry
                else:
                    print("❌ Could not remove vector database - it's locked by another process")
                    print("Please:")
                    print("1. Close any running chatbot instances")
                    print("2. Close any Python processes")
                    print("3. Try again")
                    return False
            except Exception as e:
                print(f"❌ Error removing vector database: {e}")
                return False
    else:
        print("No existing vector database found")
    
    # Also remove any ChromaDB lock files
    lock_files = [
        "./vector_db/chroma.sqlite3",
        "./vector_db/chroma.sqlite3-shm",
        "./vector_db/chroma.sqlite3-wal"
    ]
    
    for lock_file in lock_files:
        if os.path.exists(lock_file):
            try:
                os.remove(lock_file)
                print(f"✅ Removed lock file: {lock_file}")
            except Exception as e:
                print(f"⚠️  Could not remove {lock_file}: {e}")
    
    print("\n=== RAG SYSTEM RESET COMPLETE ===")
    print("Now you can rebuild the RAG system:")
    print("python app.py")
    return True

if __name__ == "__main__":
    force_reset_rag() 