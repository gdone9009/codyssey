#!/usr/bin/env python3
import urllib.request
import sys
sys.path.append('/Users/gdone/Library/Python/3.9/lib/python/site-packages')
import pypdf

def download_file(file_id, out_name):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f"Downloading {out_name} (ID: {file_id})...")
    content = urllib.request.urlopen(req).read()
    
    # If download returned html confirmation page for large files
    if b'confirm=' in content or b'<!DOCTYPE html>' in content:
        confirm_match = re.search(rb'confirm=([a-zA-Z0-9_-]+)', content)
        if confirm_match:
            confirm_code = confirm_match.group(1).decode()
            url = f"https://drive.google.com/uc?export=download&confirm={confirm_code}&id={file_id}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            content = urllib.request.urlopen(req).read()
            
    with open(out_name, 'wb') as f:
        f.write(content)
    print(f"Saved {out_name} ({len(content)} bytes)")

import re
download_file("1mtOcQEv4ANl5ooQvwItM5Dapt_H9DeeS", "/Users/gdone/dev/codyssey/mission_4_1_troubleshooting.pdf")
download_file("13b-laJfxSry3bx8Q2F-zhGuY3vWv-5Sh", "/Users/gdone/dev/codyssey/mission_4_2_monitoring.pdf")
