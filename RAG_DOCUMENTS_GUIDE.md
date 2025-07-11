# RAG Documents Guide

## Current Setup

Your RAG system now automatically loads **ALL** PDF and text files from the `me/` folder.

## Documents Currently Available

Based on your `me/` folder, the following documents will be loaded:

### 📄 PDF Files:
- `linkedin.pdf` - Your LinkedIn profile
- `CV Data Scientist Muhammad Iqbal Hilmy Izzulhaq.pdf` - Your CV
- `Full Profile.pdf` - Additional profile information
- `Iqbal_RAG_Profile.pdf` - RAG-specific profile

### 📝 Text Files:
- `summary.txt` - Your summary

## How to Add More Documents

### Method 1: Add to `me/` folder (Recommended)
Simply place any PDF or text files in the `me/` folder:
```
1_foundations/
├── me/
│   ├── linkedin.pdf ✅ (loaded)
│   ├── CV Data Scientist Muhammad Iqbal Hilmy Izzulhaq.pdf ✅ (loaded)
│   ├── Full Profile.pdf ✅ (loaded)
│   ├── Iqbal_RAG_Profile.pdf ✅ (loaded)
│   ├── summary.txt ✅ (loaded)
│   ├── your_new_document.pdf ✅ (will be loaded)
│   └── your_new_document.txt ✅ (will be loaded)
```

### Method 2: Replace existing files
You can replace any of the existing files with updated versions.

## Supported File Types

- **PDF files** (`.pdf`) - All pages will be extracted
- **Text files** (`.txt`) - Plain text content
- **Markdown files** (`.md`) - Markdown formatted text

## What Happens When You Start the App

When you run the chatbot, you'll see output like:
```
Loading static content...
Initializing RAG processor...
Loading PDF: linkedin.pdf
Loading PDF: CV Data Scientist Muhammad Iqbal Hilmy Izzulhaq.pdf
Loading PDF: Full Profile.pdf
Loading PDF: Iqbal_RAG_Profile.pdf
Loading text file: summary.txt
Found 5 documents to process:
  - linkedin
  - CV Data Scientist Muhammad Iqbal Hilmy Izzulhaq
  - Full Profile
  - Iqbal_RAG_Profile
  - summary
Processing documents for RAG...
Processed X chunks from 5 documents
```

## Testing Your Documents

To test if your documents are being used, ask questions about:
- Content from `Full Profile.pdf`
- Information from `Iqbal_RAG_Profile.pdf`
- Any specific details from your documents

Example questions:
- "What's in your full profile?"
- "Tell me about your RAG profile"
- "What specific skills are mentioned in your documents?"

## Troubleshooting

### If documents aren't being loaded:
1. Check file names (no special characters)
2. Ensure files are in the `me/` folder
3. Check file permissions
4. Look for error messages in the console

### If RAG isn't working:
1. Check if the vector database exists (`./vector_db/`)
2. Restart the app to reprocess documents
3. Check console output for errors

## Performance Note

- More documents = longer startup time
- More documents = more comprehensive responses
- The system caches embeddings, so subsequent runs are faster 