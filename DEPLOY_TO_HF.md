# Deploy to Hugging Face

## Quick Deployment Guide

### **Step 1: Create Hugging Face Space**

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - **Owner**: Your username
   - **Space name**: `your-chatbot-name`
   - **License**: MIT
   - **SDK**: Gradio
   - **Python version**: 3.10

### **Step 2: Upload Files**

Upload these files to your Hugging Face Space:

#### **1. Main App File (`app.py`)**
- Upload the entire `app.py` file from your local project
- This file now includes the Gradio interface for Hugging Face

#### **2. Requirements File (`requirements.txt`)**
- Upload the `requirements.txt` file from your local project

#### **3. Documents Folder (`me/`)**
- Upload your entire `me/` folder with all your PDF and text files
- This includes: `linkedin.pdf`, `CV Data Scientist Muhammad Iqbal Hilmy Izzulhaq.pdf`, `Full Profile.pdf`, `Iqbal_RAG_Profile.pdf`, `summary.txt`

### **Step 3: Set Environment Variables**

In your Hugging Face Space settings, add:
- `GEMINI_API_KEY`: Your Gemini API key
- `PUSHOVER_TOKEN`: Your Pushover token (optional)
- `PUSHOVER_USER`: Your Pushover user (optional)

### **Step 4: Deploy**

1. **Commit and push** all files
2. **Wait for build** (2-5 minutes)
3. **Test your deployment**

## **File Structure for Hugging Face**

Your Hugging Face Space should look like this:
```
your-hf-space/
├── app.py              # Main app with Gradio interface
├── requirements.txt    # Dependencies
├── me/                # Your documents
│   ├── linkedin.pdf
│   ├── CV Data Scientist Muhammad Iqbal Hilmy Izzulhaq.pdf
│   ├── Full Profile.pdf
│   ├── Iqbal_RAG_Profile.pdf
│   └── summary.txt
└── README.md
```

## **Testing Your Deployment**

Once deployed, test with:
- "What's your thesis topic?"
- "Tell me about your experience with Python"
- "What skills do you have?"
- "What projects have you worked on?"

## **Troubleshooting**

### **If build fails:**
1. Check `requirements.txt` has all dependencies
2. Verify Python version is 3.10
3. Check for missing imports

### **If RAG doesn't work:**
1. Verify `me/` folder is uploaded
2. Check environment variables are set
3. Look at build logs for errors

### **If documents aren't loading:**
1. Check file paths in the code
2. Verify PDF files are not corrupted
3. Ensure text extraction is working

## **Updates**

To update your deployment:
1. **Update local files**
2. **Upload new files** to Hugging Face
3. **Redeploy** the space

The RAG system will automatically reprocess documents on first load. 