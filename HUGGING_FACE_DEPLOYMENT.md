# Hugging Face Deployment with RAG

## Problem
Your local chatbot has RAG knowledge, but your Hugging Face deployment doesn't because:
- Vector database is local to your machine
- Documents are not included in the deployment
- Hugging Face doesn't have access to your local files

## Solution: Deploy with Documents Included

### **Step 1: Prepare Your Repository**

Your Hugging Face Space should have this structure:
```
your-hf-space/
├── app_hf.py              # Main app file
├── requirements_hf.txt     # Dependencies
├── me/                    # Your documents folder
│   ├── linkedin.pdf
│   ├── CV Data Scientist Muhammad Iqbal Hilmy Izzulhaq.pdf
│   ├── Full Profile.pdf
│   ├── Iqbal_RAG_Profile.pdf
│   └── summary.txt
└── README.md
```

### **Step 2: Create Hugging Face Space**

1. **Go to Hugging Face Spaces**: https://huggingface.co/spaces
2. **Create New Space**:
   - Name: `your-username/your-chatbot-name`
   - License: MIT
   - SDK: Gradio
   - Python version: 3.10

### **Step 3: Upload Files**

Upload these files to your Hugging Face Space:

#### **Main App File (`app_hf.py`):**
```python
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
```

#### **Requirements File (`requirements_hf.txt`):**
```
gradio>=4.0.0
openai>=1.0.0
python-dotenv>=1.0.0
pypdf>=3.0.0
chromadb>=0.4.0
numpy>=1.24.0
requests>=2.31.0
```

#### **Main App Code (`app.py`):**
Upload the entire `app.py` file from your local project.

#### **Documents Folder (`me/`):**
Upload your entire `me/` folder with all your PDF and text files.

### **Step 4: Set Environment Variables**

In your Hugging Face Space settings, add these environment variables:
- `GEMINI_API_KEY`: Your Gemini API key
- `PUSHOVER_TOKEN`: Your Pushover token (optional)
- `PUSHOVER_USER`: Your Pushover user (optional)

### **Step 5: Deploy**

1. **Commit and push** all files to your Hugging Face Space
2. **Wait for build** (usually 2-5 minutes)
3. **Test your deployment**

## **Alternative: Use Hugging Face CLI**

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login to Hugging Face
huggingface-cli login

# Create space
huggingface-cli repo create your-chatbot-name --type space --space-sdk gradio

# Upload files
huggingface-cli upload your-username/your-chatbot-name app_hf.py
huggingface-cli upload your-username/your-chatbot-name requirements_hf.txt
huggingface-cli upload your-username/your-chatbot-name app.py
huggingface-cli upload your-username/your-chatbot-name me/ --recursive
```

## **Testing Your Deployment**

Once deployed, test with these questions:
- "What's your thesis topic?"
- "Tell me about your experience with Python"
- "What skills do you have?"
- "What projects have you worked on?"

## **Troubleshooting**

### **If RAG doesn't work:**
1. Check if documents are uploaded correctly
2. Verify environment variables are set
3. Check build logs for errors
4. Ensure `me/` folder is included

### **If build fails:**
1. Check `requirements_hf.txt` for correct dependencies
2. Verify Python version compatibility
3. Check for missing imports

### **If documents aren't loading:**
1. Verify file paths in the code
2. Check if PDF files are corrupted
3. Ensure text extraction is working

## **Performance Notes**

- **First load**: Will be slower as it processes documents
- **Subsequent loads**: Faster due to caching
- **Memory usage**: Higher due to vector database
- **API calls**: Same as local version

## **Security Notes**

- **API keys**: Store in Hugging Face environment variables
- **Documents**: Be careful with sensitive information
- **Public access**: Your documents will be in the repository

## **Updates**

To update your deployment:
1. **Update local files**
2. **Upload new files** to Hugging Face
3. **Redeploy** the space

The RAG system will automatically reprocess documents on first load. 