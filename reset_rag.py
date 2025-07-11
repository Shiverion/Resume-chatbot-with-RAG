#!/usr/bin/env python3
"""
Reset and rebuild RAG system from scratch
"""

import shutil
import os
from pathlib import Path

def reset_rag_system():
    """Reset the RAG system and rebuild it"""
    print("=== RESETTING RAG SYSTEM ===")
    
    # Remove existing vector database
    vector_db_path = "./vector_db"
    if os.path.exists(vector_db_path):
        print(f"Removing existing vector database: {vector_db_path}")
        shutil.rmtree(vector_db_path)
        print("✅ Vector database removed")
    else:
        print("No existing vector database found")
    
    # Check what documents are available
    me_folder = "me"
    if os.path.exists(me_folder):
        print(f"\n=== DOCUMENTS IN {me_folder} ===")
        for file_path in Path(me_folder).glob("*"):
            if file_path.is_file():
                print(f"📄 {file_path.name}")
                if file_path.suffix.lower() == '.pdf':
                    try:
                        from pypdf import PdfReader
                        reader = PdfReader(str(file_path))
                        total_pages = len(reader.pages)
                        print(f"   Pages: {total_pages}")
                        
                        # Show first page content
                        first_page = reader.pages[0].extract_text()
                        print(f"   First page preview: {first_page[:100]}...")
                        
                        # Check for thesis-related content
                        if 'thesis' in first_page.lower():
                            print("   ✅ Contains 'thesis' keyword")
                        if 'research' in first_page.lower():
                            print("   ✅ Contains 'research' keyword")
                            
                    except Exception as e:
                        print(f"   ❌ Error reading {file_path.name}: {e}")
    
    print("\n=== REBUILDING RAG SYSTEM ===")
    print("Now run the chatbot to rebuild the RAG system:")
    print("python app.py")
    print("\nAfter rebuilding, test with:")
    print("python debug_rag.py")

if __name__ == "__main__":
    reset_rag_system() 