#!/usr/bin/env python3
import urllib.request
import re
import json

url = "https://drive.google.com/drive/folders/1uXKazl5HZ8wiC1IOG1HB7Ezt5a7yMT3X"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})

html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

# Extract file items with ID and Name from initial JS state
pattern = r'\["([a-zA-Z0-9_-]{25,})","([^"]+\.pdf)"'
matches = re.findall(pattern, html)

print(f"Found {len(matches)} PDF files with IDs:")
file_map = {}
with open('/Users/gdone/dev/codyssey/gdrive_pdf_map.txt', 'w', encoding='utf-8') as f:
    for fid, fname in sorted(matches, key=lambda x: x[1]):
        # Unicode normalize filename
        import unicodedata
        fname_norm = unicodedata.normalize('NFC', fname)
        file_map[fname_norm] = fid
        f.write(f"{fname_norm} -> {fid}\n")
        print(f" - {fname_norm} : {fid}")
