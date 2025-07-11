#!/usr/bin/env python3
"""
Debug script to see what content is being retrieved from RAG documents
"""

from app import Me
import os

def debug_rag_content():
    """Debug what content is being loaded and retrieved"""
    print("=== RAG DEBUG SESSION ===")
    
    # Initialize the chatbot
    me = Me()
    
    # Test specific thesis-related queries
    thesis_queries = [
        "What is your thesis topic?",
        "Tell me about your thesis",
        "What did you research for your thesis?",
        "What was your thesis about?",
        "What is your thesis description?",
        "What research did you do for your thesis?"
    ]
    
    print("\n=== Testing Thesis Queries ===")
    for i, query in enumerate(thesis_queries, 1):
        print(f"\n--- Query {i}: {query} ---")
        
        try:
            # Get RAG context directly
            context = me.rag_processor.retrieve_relevant_context(query, top_k=5)
            print(f"RAG Context Found: {'Yes' if context else 'No'}")
            
            if context:
                print(f"Context Length: {len(context)} characters")
                print("=== RAG CONTEXT ===")
                print(context)
                print("=== END RAG CONTEXT ===")
            else:
                print("❌ NO RAG CONTEXT FOUND")
            
            # Get full response
            response = me.chat(query, [])
            print(f"\n=== FULL RESPONSE ===")
            print(response)
            print("=== END RESPONSE ===")
            
        except Exception as e:
            print(f"Error: {e}")
    
    # Let's also check what documents were loaded
    print("\n=== CHECKING LOADED DOCUMENTS ===")
    me_folder = "me"
    if os.path.exists(me_folder):
        for file_path in os.listdir(me_folder):
            if file_path.endswith('.pdf'):
                print(f"PDF found: {file_path}")
                # Try to read a sample
                try:
                    from pypdf import PdfReader
                    reader = PdfReader(f"me/{file_path}")
                    first_page = reader.pages[0].extract_text()
                    print(f"  First page preview: {first_page[:200]}...")
                except Exception as e:
                    print(f"  Error reading {file_path}: {e}")

if __name__ == "__main__":
    debug_rag_content() 