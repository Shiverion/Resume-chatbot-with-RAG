#!/usr/bin/env python3
"""
Test script to verify RAG is working and accessing knowledge base
"""

from app import Me

def test_rag_access():
    """Test if RAG is properly accessing the knowledge base"""
    print("Initializing chatbot...")
    me = Me()
    
    # Test queries that should trigger RAG
    test_queries = [
        "What's in your full profile?",
        "Tell me about your RAG profile",
        "What specific skills do you have?",
        "What projects have you worked on?",
        "Tell me about your experience",
        "What's your background in data science?",
        "What are your technical skills?",
        "Can you describe your career experience?"
    ]
    
    print("\n=== Testing RAG Access ===")
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i} ---")
        print(f"Query: {query}")
        
        try:
            # Get RAG context directly
            context = me.rag_processor.retrieve_relevant_context(query, top_k=3)
            print(f"RAG Context Found: {'Yes' if context else 'No'}")
            if context:
                print(f"Context Length: {len(context)} characters")
                print(f"Context Preview: {context[:200]}...")
            
            # Get full response
            response = me.chat(query, [])
            print(f"Response Length: {len(response)} characters")
            print(f"Response Preview: {response[:200]}...")
            
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n=== RAG Test Completed ===")

if __name__ == "__main__":
    test_rag_access() 