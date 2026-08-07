#!/usr/bin/env python3
import sys
sys.path.append('/Users/gdone/Library/Python/3.9/lib/python/site-packages')
import pypdf

reader = pypdf.PdfReader('/Users/gdone/dev/codyssey/downloaded_mission.pdf')
print(f"Total pages: {len(reader.pages)}")

with open('/Users/gdone/dev/codyssey/pdf_out.txt', 'w', encoding='utf-8') as f:
    for i, page in enumerate(reader.pages):
        f.write(f"=== PAGE {i+1} ===\n")
        f.write(page.extract_text() + "\n")

print("Done extracting PDF text.")
