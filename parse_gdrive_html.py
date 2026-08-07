#!/usr/bin/env python3
import urllib.request
import re

url = "https://drive.google.com/drive/folders/1uXKazl5HZ8wiC1IOG1HB7Ezt5a7yMT3X"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})

html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

print("HTML length:", len(html))

# Find string patterns matching mission names or pdf files
matches = re.findall(r'\["(.*?)"', html)
strings = set()
for m in matches:
    if any(k in m for k in ['미션', '과제', 'PDF', 'pdf', '4-', '04', '4.']):
        strings.add(m)

with open('/Users/gdone/dev/codyssey/gdrive_parsed.txt', 'w', encoding='utf-8') as f:
    for s in sorted(strings):
        f.write(s + '\n')

# Also search for all occurrence of 4-1 or 4_1 or linux
all_found = re.findall(r'.{0,50}(?:4-1|4_1|미션 4|4단계|linux).{0,50}', html, re.IGNORECASE)
with open('/Users/gdone/dev/codyssey/gdrive_matches.txt', 'w', encoding='utf-8') as f:
    f.write(f"Matches count: {len(all_found)}\n")
    for item in all_found[:100]:
        f.write(item + '\n')

print(f"Found {len(all_found)} matches.")
