#!/usr/bin/env python3
import sys
import os
sys.path.append('/Users/gdone/Library/Python/3.9/lib/python/site-packages')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_FILE = '/Users/gdone/dev/codyssey/token.json'
FOLDER_ID = '1uXKazl5HZ8wiC1IOG1HB7Ezt5a7yMT3X'

if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('drive', 'v3', credentials=creds)
    
    # Query files in folder
    query = f"'{FOLDER_ID}' in parents and trashed = false"
    results = service.files().list(q=query, pageSize=50, fields="files(id, name, mimeType, size)").execute()
    items = results.get('files', [])
    
    print(f"Folder items count: {len(items)}")
    with open('/Users/gdone/dev/codyssey/folder_items.txt', 'w', encoding='utf-8') as f:
        for item in items:
            f.write(f"[{item['name']}] (ID: {item['id']}, Type: {item['mimeType']})\n")
    print("SUCCESS")
else:
    print("TOKEN_FILE does not exist.")
