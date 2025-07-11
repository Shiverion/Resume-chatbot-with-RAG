#!/usr/bin/env python3
"""
Check if thesis content is actually in the PDF files
"""

from pypdf import PdfReader
import os

def check_thesis_content():
    """Check all PDF files for thesis-related content"""
    print("=== CHECKING FOR THESIS CONTENT ===")
    
    me_folder = "me"
    if os.path.exists(me_folder):
        for file_path in os.listdir(me_folder):
            if file_path.endswith('.pdf'):
                print(f"\n📄 Checking: {file_path}")
                try:
                    reader = PdfReader(f"me/{file_path}")
                    total_pages = len(reader.pages)
                    print(f"   Pages: {total_pages}")
                    
                    # Check each page for thesis content
                    thesis_found = False
                    for page_num, page in enumerate(reader.pages):
                        text = page.extract_text()
                        if text:
                            # Look for thesis-related keywords
                            thesis_keywords = ['thesis', 'research', 'dissertation', 'study', 'investigation']
                            found_keywords = []
                            for keyword in thesis_keywords:
                                if keyword.lower() in text.lower():
                                    found_keywords.append(keyword)
                            
                            if found_keywords:
                                thesis_found = True
                                print(f"   ✅ Page {page_num + 1}: Found keywords: {found_keywords}")
                                print(f"   Content preview: {text[:200]}...")
                    
                    if not thesis_found:
                        print(f"   ❌ No thesis-related keywords found in {file_path}")
                        
                except Exception as e:
                    print(f"   ❌ Error reading {file_path}: {e}")

if __name__ == "__main__":
    check_thesis_content() 