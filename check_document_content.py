#!/usr/bin/env python3
"""
Check specific content in each document
"""

from pypdf import PdfReader
import os
from pathlib import Path

def check_document_content():
    """Check what content is in each document"""
    print("=== DOCUMENT CONTENT CHECK ===")
    
    me_folder = "me"
    if os.path.exists(me_folder):
        for file_path in Path(me_folder).glob("*"):
            if file_path.is_file():
                print(f"\n📄 File: {file_path.name}")
                
                try:
                    if file_path.suffix.lower() == '.pdf':
                        reader = PdfReader(str(file_path))
                        total_pages = len(reader.pages)
                        print(f"   Pages: {total_pages}")
                        
                        # Check each page for specific content
                        for page_num, page in enumerate(reader.pages):
                            text = page.extract_text()
                            if text:
                                # Look for specific keywords
                                keywords = {
                                    'thesis': ['thesis', 'research', 'study', 'investigation', 'dissertation'],
                                    'gpa': ['gpa', 'grade', 'point average', 'cgpa'],
                                    'education': ['education', 'university', 'college', 'degree'],
                                    'skills': ['skill', 'technology', 'programming', 'python', 'data'],
                                    'experience': ['experience', 'work', 'job', 'project']
                                }
                                
                                found_content = {}
                                for category, words in keywords.items():
                                    found = [word for word in words if word.lower() in text.lower()]
                                    if found:
                                        found_content[category] = found
                                
                                if found_content:
                                    print(f"   Page {page_num + 1}:")
                                    for category, words in found_content.items():
                                        print(f"     ✅ {category.title()}: {words}")
                                    
                                    # Show a preview of the content
                                    print(f"     Content preview: {text[:200]}...")
                                else:
                                    print(f"   Page {page_num + 1}: No specific keywords found")
                    
                    elif file_path.suffix.lower() in ['.txt', '.md']:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        # Check for keywords in text files
                        keywords = {
                            'thesis': ['thesis', 'research', 'study', 'investigation'],
                            'gpa': ['gpa', 'grade', 'point average'],
                            'education': ['education', 'university', 'college'],
                            'skills': ['skill', 'technology', 'programming'],
                            'experience': ['experience', 'work', 'job', 'project']
                        }
                        
                        found_content = {}
                        for category, words in keywords.items():
                            found = [word for word in words if word.lower() in content.lower()]
                            if found:
                                found_content[category] = found
                        
                        if found_content:
                            print(f"   Content found:")
                            for category, words in found_content.items():
                                print(f"     ✅ {category.title()}: {words}")
                            print(f"   Content preview: {content[:200]}...")
                        else:
                            print(f"   No specific keywords found")
                            
                except Exception as e:
                    print(f"   ❌ Error reading {file_path.name}: {e}")

if __name__ == "__main__":
    check_document_content() 