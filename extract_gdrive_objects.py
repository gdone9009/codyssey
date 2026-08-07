#!/usr/bin/env python3
import urllib.request
import re
import unicodedata

url = "https://drive.google.com/drive/folders/1uXKazl5HZ8wiC1IOG1HB7Ezt5a7yMT3X"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

# Search for all strings ending in .pdf and surrounding 200 chars to find their file IDs
pdf_positions = [m.start() for m in re.finditer(r'\.pdf', html, re.IGNORECASE)]
file_entries = {}

for pos in pdf_positions:
    snippet = html[max(0, pos-300):min(len(html), pos+100)]
    # Find PDF filename
    name_match = re.search(r'["\']([^"\']+\.pdf)["\']', snippet, re.IGNORECASE)
    # Find Google Drive File ID (28-45 char base64url string)
    id_matches = re.findall(r'["\']([a-zA-Z0-9_-]{28,45})["\']', snippet)
    if name_match:
        name = unicodedata.normalize('NFC', name_match.group(1))
        # Filter out folder id
        ids = [i for i in id_matches if i != '1uXKazl5HZ8wiC1IOG1HB7Ezt5a7yMT3X']
        if ids:
            file_entries[name] = ids[0]

with open('/Users/gdone/dev/codyssey/gdrive_pdf_map.txt', 'w', encoding='utf-8') as f:
    for name, fid in sorted(file_entries.items()):
        f.write(f"{name} -> {fid}\n")
        print(f"📄 {name} : {fid}")
