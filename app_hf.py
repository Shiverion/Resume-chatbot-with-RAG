#!/usr/bin/env python3
"""
Hugging Face deployment version of the chatbot
"""

import gradio as gr
from app import get_me_instance, chat_interface

# Create the demo for Hugging Face
demo = gr.ChatInterface(
    fn=chat_interface,
    title="🤖 AI Chatbot with RAG",
    description="Chat with Muhammad Iqbal Hilmy Izzulhaq's AI assistant with RAG knowledge base",
    examples=[
        "What's your thesis topic?",
        "Tell me about your experience with Python",
        "What skills do you have?",
        "What projects have you worked on?",
        "Tell me about your background"
    ]
)

# For Hugging Face Spaces
if __name__ == "__main__":
    demo.launch() 