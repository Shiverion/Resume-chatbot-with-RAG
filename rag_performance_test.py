#!/usr/bin/env python3
"""
RAG Performance Test - Measures response times for RAG-enabled queries
"""

import time
from app import Me

def test_rag_performance():
    """Test RAG-specific response times"""
    print("Initializing chatbot with RAG...")
    me = Me()
    
    # Test queries that should trigger RAG
    rag_test_messages = [
        "What's your experience with Python programming?",
        "Tell me about your machine learning projects",
        "What skills do you have in data science?",
        "Can you describe your background in AI?",
        "What projects have you worked on?",
        "Tell me about your career experience",
        "What are your technical skills?",
        "Do you have experience with analytics?"
    ]
    
    # Test queries that should NOT trigger RAG (for comparison)
    non_rag_test_messages = [
        "Hello, how are you?",
        "Nice to meet you",
        "What's your name?",
        "How's the weather?",
        "Thanks for the information"
    ]
    
    print("\n=== Testing RAG-enabled queries ===")
    rag_times = []
    for i, message in enumerate(rag_test_messages, 1):
        print(f"\nRAG Test {i}: {message}")
        start_time = time.time()
        
        try:
            response = me.chat(message, [])
            end_time = time.time()
            response_time = end_time - start_time
            rag_times.append(response_time)
            
            print(f"Response time: {response_time:.2f} seconds")
            print(f"Response length: {len(response)} characters")
            
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n=== Testing non-RAG queries ===")
    non_rag_times = []
    for i, message in enumerate(non_rag_test_messages, 1):
        print(f"\nNon-RAG Test {i}: {message}")
        start_time = time.time()
        
        try:
            response = me.chat(message, [])
            end_time = time.time()
            response_time = end_time - start_time
            non_rag_times.append(response_time)
            
            print(f"Response time: {response_time:.2f} seconds")
            print(f"Response length: {len(response)} characters")
            
        except Exception as e:
            print(f"Error: {e}")
    
    # Calculate averages
    if rag_times:
        avg_rag_time = sum(rag_times) / len(rag_times)
        print(f"\n=== RESULTS ===")
        print(f"Average RAG response time: {avg_rag_time:.2f} seconds")
        print(f"Fastest RAG response: {min(rag_times):.2f} seconds")
        print(f"Slowest RAG response: {max(rag_times):.2f} seconds")
    
    if non_rag_times:
        avg_non_rag_time = sum(non_rag_times) / len(non_rag_times)
        print(f"Average non-RAG response time: {avg_non_rag_time:.2f} seconds")
        print(f"Fastest non-RAG response: {min(non_rag_times):.2f} seconds")
        print(f"Slowest non-RAG response: {max(non_rag_times):.2f} seconds")
    
    if rag_times and non_rag_times:
        speedup = avg_rag_time / avg_non_rag_time if avg_non_rag_time > 0 else 0
        print(f"RAG queries are {speedup:.1f}x slower than non-RAG queries")
    
    print("\nPerformance test completed!")

if __name__ == "__main__":
    test_rag_performance() 