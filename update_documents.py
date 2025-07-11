#!/usr/bin/env python3
"""
Update documents in RAG system without full reset
"""

from app import Me
import os
from pathlib import Path

def update_documents():
    """Update documents in the RAG system"""
    print("=== UPDATING RAG DOCUMENTS ===")
    
    # Initialize the chatbot
    me = Me()
    
    # Load documents again
    documents = {}
    
    # Load ALL PDF and text files from me/ folder
    me_folder = "me"
    if os.path.exists(me_folder):
        for file_path in Path(me_folder).glob("*"):
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() == '.pdf':
                        print(f"Loading PDF: {file_path.name}")
                        from pypdf import PdfReader
                        reader = PdfReader(str(file_path))
                        content = ""
                        for page in reader.pages:
                            text = page.extract_text()
                            if text:
                                content += text + "\n"
                        documents[file_path.stem] = content
                    elif file_path.suffix.lower() in ['.txt', '.md']:
                        print(f"Loading text file: {file_path.name}")
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        documents[file_path.stem] = content
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
    
    # Force reprocess documents
    if documents:
        print(f"Found {len(documents)} documents to update:")
        for doc_name in documents.keys():
            print(f"  - {doc_name}")
        
        print("\nForce reprocessing documents...")
        me.rag_processor.process_documents(documents, force_reprocess=True)
        print("✅ Documents updated successfully!")
    else:
        print("No documents found to update")

if __name__ == "__main__":
    update_documents() 