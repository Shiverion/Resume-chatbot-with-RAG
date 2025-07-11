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
import time
from functools import lru_cache
import hashlib


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
    """Optimized RAG processor with enhanced caching and faster retrieval"""
    
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
        self._embeddings_cache = {}
        self._context_cache = {}
        self._query_cache = {}
        
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
    
    def create_fast_embedding(self, text: str) -> List[float]:
        """Create a fast hash-based embedding for caching"""
        # Create a deterministic hash-based embedding
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to 1536-dimensional vector (same as OpenAI embeddings)
        embedding = []
        for i in range(1536):
            byte_index = i % len(hash_bytes)
            embedding.append(hash_bytes[byte_index] / 255.0)
        
        return embedding
    
    @lru_cache(maxsize=1000)
    def get_embeddings_cached(self, text: str) -> List[float]:
        """Get embeddings with caching to avoid repeated API calls"""
        # Check if we have a cached version first
        text_hash = hashlib.md5(text.encode()).hexdigest()
        if text_hash in self._embeddings_cache:
            return self._embeddings_cache[text_hash]
        
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=[text]
            )
            embedding = response.data[0].embedding
            # Cache the result
            self._embeddings_cache[text_hash] = embedding
            return embedding
        except Exception as e:
            print(f"Error getting embeddings: {e}")
            # Use fast hash-based embedding as fallback
            embedding = self.create_fast_embedding(text)
            self._embeddings_cache[text_hash] = embedding
            return embedding
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for a list of texts with caching"""
        embeddings = []
        for text in texts:
            embeddings.append(self.get_embeddings_cached(text))
        return embeddings
    
    def process_documents(self, documents: Dict[str, str]):
        """Process and store documents in the vector database"""
        # Check if documents are already processed
        try:
            count = self.collection.count()
            if count > 0:
                print(f"Vector database already contains {count} documents, skipping processing")
                return
        except:
            pass
        
        all_chunks = []
        all_metadata = []
        
        for doc_name, content in documents.items():
            chunks = self.chunk_text(content)
            all_chunks.extend(chunks)
            all_metadata.extend([{"source": doc_name, "chunk_index": i} for i in range(len(chunks))])
        
        if all_chunks:
            print("Processing documents for RAG...")
            embeddings = self.get_embeddings(all_chunks)
            
            # Add documents to collection
            self.collection.add(
                embeddings=embeddings,  # type: ignore
                documents=all_chunks,
                metadatas=all_metadata,
                ids=[f"chunk_{i}" for i in range(len(all_chunks))]
            )
            print(f"Processed {len(all_chunks)} chunks from {len(documents)} documents")
    
    def add_document(self, content: str, doc_name: str):
        """Add a single document to the RAG system"""
        try:
            chunks = self.chunk_text(content)
            if chunks:
                embeddings = self.get_embeddings(chunks)
                metadata = [{"source": doc_name, "chunk_index": i} for i in range(len(chunks))]
                ids = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]
                
                self.collection.add(
                    embeddings=embeddings,  # type: ignore
                    documents=chunks,
                    metadatas=metadata,  # type: ignore
                    ids=ids
                )
                print(f"Added document '{doc_name}' with {len(chunks)} chunks")
                return True
        except Exception as e:
            print(f"Error adding document '{doc_name}': {e}")
            return False
    
    def retrieve_relevant_context(self, query: str, top_k: int = 2) -> str:
        """Retrieve relevant context for a query with enhanced caching"""
        # Create a more robust cache key
        query_normalized = query.lower().strip()
        cache_key = f"{hashlib.md5(query_normalized.encode()).hexdigest()}_{top_k}"
        
        if cache_key in self._context_cache:
            return self._context_cache[cache_key]
        
        try:
            # Get query embedding
            query_embedding = self.get_embeddings_cached(query)
            
            # Search for similar documents
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            if results and results.get('documents') and results['documents'] and results['documents'][0]:
                context_parts = []
                for i, doc in enumerate(results['documents'][0]):
                    if results.get('metadatas') and results['metadatas'][0] and i < len(results['metadatas'][0]):
                        source = results['metadatas'][0][i].get('source', 'Unknown')
                    else:
                        source = 'Unknown'
                    context_parts.append(f"Source: {source}\n{doc}\n")
                
                context = "\n".join(context_parts)
                # Cache the result
                self._context_cache[cache_key] = context
                return context
            else:
                return ""
                
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return ""


class Me:

    def __init__(self):
        self.gemini = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=os.getenv("GEMINI_API_KEY"))
        self.name = "Muhammad Iqbal Hilmy Izzulhaq"
        
        # Load static content first for faster startup
        print("Loading static content...")
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
        
        # Initialize RAG processor
        print("Initializing RAG processor...")
        self.rag_processor = RAGProcessor(self.gemini)
        
        # Load and process documents in background
        self.load_and_process_documents()

    def load_and_process_documents(self):
        """Load all documents and process them for RAG"""
        documents = {}
        
        # Load ALL PDF and text files from me/ folder
        me_folder = "me"
        if os.path.exists(me_folder):
            for file_path in Path(me_folder).glob("*"):
                if file_path.is_file():
                    try:
                        if file_path.suffix.lower() == '.pdf':
                            print(f"Loading PDF: {file_path.name}")
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
        
        # Process documents for RAG
        if documents:
            print(f"Found {len(documents)} documents to process:")
            for doc_name in documents.keys():
                print(f"  - {doc_name}")
            self.rag_processor.process_documents(documents)
        else:
            print("No documents found to process")

    def add_document_to_rag(self, file_content, file_name):
        """Add a document to the RAG system via the UI"""
        if file_content and file_name:
            success = self.rag_processor.add_document(file_content, file_name)
            if success:
                return f"✅ Successfully added '{file_name}' to RAG knowledge base!"
            else:
                return f"❌ Failed to add '{file_name}' to RAG knowledge base."
        return "Please provide both file content and name."

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
        # More aggressive filtering for RAG usage
        rag_keywords = ['experience', 'skill', 'project', 'work', 'job', 'career', 'background', 
                       'python', 'data', 'machine', 'learning', 'ai', 'ml', 'analytics', 'research']
        
        use_rag = (len(message) > 30 or 
                  any(keyword in message.lower() for keyword in rag_keywords) or
                  '?' in message)
        
        relevant_context = ""
        if use_rag:
            # Use smaller top_k for faster retrieval
            relevant_context = self.rag_processor.retrieve_relevant_context(message, top_k=2)
        
        # Create system prompt with RAG context
        system_prompt = self.system_prompt(relevant_context)
        
        messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
        
        # Limit tool call iterations to prevent infinite loops
        max_iterations = 2  # Reduced from 3
        iteration = 0
        
        while iteration < max_iterations:
            response = self.gemini.chat.completions.create(
                model="gemini-2.5-flash",  # Use faster model
                messages=messages, 
                tools=tools,  # type: ignore
                max_tokens=2048,  # Increased for complete responses
                temperature=0.7  # Slightly lower for more focused responses
            )
            
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
                iteration += 1
            else:
                break
                
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()