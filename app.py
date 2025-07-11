from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
import chromadb
from chromadb.config import Settings
import numpy as np
from typing import List, Dict, Any
import re
from pathlib import Path


load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class RAGProcessor:
    """Simple RAG processor for document retrieval"""
    
    def __init__(self, openai_client: OpenAI):
        self.openai_client = openai_client
        self.chroma_client = chromadb.PersistentClient(
            path="./vector_db",
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
        
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundaries
            if end < len(text):
                last_period = chunk.rfind('.')
                last_exclamation = chunk.rfind('!')
                last_question = chunk.rfind('?')
                last_newline = chunk.rfind('\n')
                
                break_point = max(last_period, last_exclamation, last_question, last_newline)
                if break_point > chunk_size * 0.7:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
            
        return chunks
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for a list of texts"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            print(f"Error getting embeddings: {e}")
            # Fallback to simple hash-based embeddings
            return [[hash(text) % 1000 / 1000.0 for _ in range(1536)] for text in texts]
    
    def process_documents(self, documents: Dict[str, str]):
        """Process and store documents in the vector database"""
        all_chunks = []
        all_metadata = []
        
        for doc_name, content in documents.items():
            chunks = self.chunk_text(content)
            all_chunks.extend(chunks)
            all_metadata.extend([{"source": doc_name, "chunk_index": i} for i in range(len(chunks))])
        
        if all_chunks:
            embeddings = self.get_embeddings(all_chunks)
            
            # Add documents to collection
            self.collection.add(
                embeddings=embeddings,
                documents=all_chunks,
                metadatas=all_metadata,
                ids=[f"chunk_{i}" for i in range(len(all_chunks))]
            )
            print(f"Processed {len(all_chunks)} chunks from {len(documents)} documents")
    
    def retrieve_relevant_context(self, query: str, top_k: int = 5) -> str:
        """Retrieve relevant context for a query"""
        try:
            # Get query embedding
            query_embedding = self.get_embeddings([query])[0]
            
            # Search for similar documents
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            if results['documents'] and results['documents'][0]:
                context_parts = []
                for i, doc in enumerate(results['documents'][0]):
                    source = results['metadatas'][0][i]['source']
                    context_parts.append(f"Source: {source}\n{doc}\n")
                
                return "\n".join(context_parts)
            else:
                return ""
                
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return ""


class Me:

    def __init__(self):
        self.gemini = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=os.getenv("GEMINI_API_KEY"))
        self.name = "Muhammad Iqbal Hilmy Izzulhaq"
        
        # Initialize RAG processor
        self.rag_processor = RAGProcessor(self.gemini)
        
        # Load and process documents
        self.load_and_process_documents()
        
        # Load static content for fallback
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    def load_and_process_documents(self):
        """Load all documents and process them for RAG"""
        documents = {}
        
        # Load PDF documents
        pdf_files = ["me/linkedin.pdf", "me/CV Data Scientist Muhammad Iqbal Hilmy Izzulhaq.pdf"]
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                try:
                    reader = PdfReader(pdf_file)
                    content = ""
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            content += text + "\n"
                    documents[Path(pdf_file).stem] = content
                except Exception as e:
                    print(f"Error loading {pdf_file}: {e}")
        
        # Load text files
        text_files = ["me/summary.txt"]
        for text_file in text_files:
            if os.path.exists(text_file):
                try:
                    with open(text_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    documents[text_file] = content
                except Exception as e:
                    print(f"Error loading {text_file}: {e}")
        
        # Process documents for RAG
        if documents:
            self.rag_processor.process_documents(documents)
        else:
            print("No documents found to process")

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self, relevant_context: str = ""):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        
        # Add RAG context if available
        if relevant_context:
            system_prompt += f"\n## Relevant Information from Knowledge Base:\n{relevant_context}\n\n"
        
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        # Get relevant context using RAG
        relevant_context = self.rag_processor.retrieve_relevant_context(message)
        
        # Create system prompt with RAG context
        system_prompt = self.system_prompt(relevant_context)
        
        messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.gemini.chat.completions.create(model="gemini-2.5-pro", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()
    