#!/usr/bin/env python3
"""
Simple performance test for the chatbot
"""

import time
from app import Me

def test_chatbot_performance():
    """Test chatbot response times"""
    print("Initializing chatbot...")
    me = Me()
    
    test_messages = [
        "Hello, how are you?",
        "What's your experience with Python?",
        "Tell me about your background",
        "What skills do you have?",
        "Can you tell me about your projects?"
    ]
    
    print("\nTesting response times...")
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: {message}")
        start_time = time.time()
        
        try:
            response = me.chat(message, [])
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"Response time: {response_time:.2f} seconds")
            print(f"Response length: {len(response)} characters")
            print(f"Response preview: {response[:100]}...")
            
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nPerformance test completed!")

if __name__ == "__main__":
    test_chatbot_performance() 