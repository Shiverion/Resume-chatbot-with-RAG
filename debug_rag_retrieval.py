#!/usr/bin/env python3
"""
Debug RAG retrieval to see what content is being found and what's missing
"""

from app import Me

def debug_rag_retrieval():
    """Debug what content is being retrieved from RAG"""
    print("=== RAG RETRIEVAL DEBUG ===")
    
    # Initialize the chatbot
    me = Me()
    
    # Test queries that should find different types of information
    test_queries = [
        "What is your GPA?",
        "What is your thesis topic?",
        "Tell me about your thesis",
        "What research did you do?",
        "What is your thesis about?",
        "What was your thesis topic?",
        "Tell me about your academic research",
        "What did you study for your thesis?",
        "What is your thesis description?"
    ]
    
    print("\n=== Testing RAG Retrieval ===")
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Query {i}: {query} ---")
        
        try:
            # Get RAG context with different top_k values
            context_3 = me.rag_processor.retrieve_relevant_context(query, top_k=3)
            context_5 = me.rag_processor.retrieve_relevant_context(query, top_k=5)
            context_10 = me.rag_processor.retrieve_relevant_context(query, top_k=10)
            
            print(f"Context with top_k=3: {'Found' if context_3 else 'Not found'}")
            print(f"Context with top_k=5: {'Found' if context_5 else 'Not found'}")
            print(f"Context with top_k=10: {'Found' if context_10 else 'Not found'}")
            
            if context_3:
                print(f"Context length (top_k=3): {len(context_3)} characters")
                print("Context preview:")
                print(context_3[:300] + "..." if len(context_3) > 300 else context_3)
            
            # Check if thesis-related keywords are in the context
            thesis_keywords = ['thesis', 'research', 'study', 'investigation', 'dissertation']
            found_keywords = []
            if context_3:
                for keyword in thesis_keywords:
                    if keyword.lower() in context_3.lower():
                        found_keywords.append(keyword)
            
            if found_keywords:
                print(f"✅ Found thesis keywords: {found_keywords}")
            else:
                print("❌ No thesis keywords found in retrieved context")
            
        except Exception as e:
            print(f"Error: {e}")
    
    # Let's also check what documents are in the vector database
    print("\n=== CHECKING VECTOR DATABASE ===")
    try:
        count = me.rag_processor.collection.count()
        print(f"Total documents in vector database: {count}")
        
        # Get a sample of all documents
        results = me.rag_processor.collection.get()
        if results and results.get('documents'):
            print(f"Sample documents in database:")
            for i, doc in enumerate(results['documents'][:5]):  # Show first 5
                source = results['metadatas'][i]['source'] if results.get('metadatas') else 'Unknown'
                print(f"  {i+1}. Source: {source}")
                print(f"     Content: {doc[:100]}...")
                
                # Check for thesis keywords
                thesis_keywords = ['thesis', 'research', 'study', 'investigation']
                found = [kw for kw in thesis_keywords if kw.lower() in doc.lower()]
                if found:
                    print(f"     ✅ Contains: {found}")
                else:
                    print(f"     ❌ No thesis keywords")
                print()
    except Exception as e:
        print(f"Error checking vector database: {e}")

if __name__ == "__main__":
    debug_rag_retrieval() 