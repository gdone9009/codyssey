#!/usr/bin/env python3
import sys
sys.path.append('/Users/gdone/Library/Python/3.9/lib/python/site-packages')
import pypdf

reader = pypdf.PdfReader('/Users/gdone/dev/codyssey/mission_4_1_troubleshooting.pdf')
print(f"Mission 4-1 Total Pages: {len(reader.pages)}")

with open('/Users/gdone/dev/codyssey/mission_4_1_text.txt', 'w', encoding='utf-8') as f:
    for i, page in enumerate(reader.pages):
        f.write(f"==================== PAGE {i+1} ====================\n")
        f.write(page.extract_text() + "\n")

print("Saved mission_4_1_text.txt")
