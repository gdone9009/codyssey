#!/usr/bin/env python3
# ==============================================================================
# 파일명: gdrive_service.py
# 설명: Google Drive API v3 연동 및 클라우드 파일 관리를 위한 핵심 서비스 모듈
# 작성 목적: 로컬 프로그램 통과 없이 구글 드라이브와 직접 통신하여 파일 목록 조회/다운로드/업로드 자동화
# ==============================================================================

import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# 1. Google Drive 접근 권한 범위(Scope) 설정
# drive.readonly: 읽기 전용 권한 / drive: 파일 생성 및 수정 포함 전체 권한
SCOPES = ['https://www.googleapis.com/auth/drive']

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.json')


def get_gdrive_service():
    """
    Google Drive API 인증을 수행하고 서비스 객체(Service)를 반환하는 함수.
    최초 1회 실행 시 브라우저 인증 창이 열리며, 인증 완료 후 token.json이 자동 생성됩니다.
    """
    creds = None

    # 1.1 기존에 생성된 token.json 파일이 존재하면 로드합니다.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 1.2 유효한 인증 정보가 없으면 브라우저 인증을 거칩니다.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 기존 만료된 토큰을 자동으로 갱신(Refresh)합니다.
            creds.refresh(Request())
        else:
            # credentials.json 파일 기반으로 OAuth2 로그인 플로우를 실행합니다.
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"인증 파일이 필요합니다: {CREDENTIALS_FILE}")

            import warnings
            warnings.filterwarnings("ignore")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080, prompt='consent')

        # 1.3 획득한 인증 정보를 token.json 파일에 저장하여 향후 자동 로드합니다.
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    # 1.4 Google Drive API v3 서비스 객체 생성 후 반환
    service = build('drive', 'v3', credentials=creds)
    return service


def list_gdrive_files(pageSize=20):
    """
    구글 드라이브 내의 파일 목록을 조회하여 출력하는 함수.
    """
    service = get_gdrive_service()
    results = service.files().list(
        pageSize=pageSize,
        fields="nextPageToken, files(id, name, mimeType, modifiedTime, size)"
    ).execute()

    items = results.get('files', [])
    print(f"\n📂 [Google Drive 파일 목록 (최대 {pageSize}개)]")
    if not items:
        print("  - 파일이 존재하지 않습니다.")
    else:
        for item in items:
            print(f"  - [{item['name']}] (ID: {item['id']}, Type: {item['mimeType']})")
    return items


if __name__ == '__main__':
    print("🚀 Google Drive API 최초 인증 프로세스를 시작합니다...")
    try:
        service = get_gdrive_service()
        print("✅ 인증 성공! token.json 생성이 완료되었습니다.")
        list_gdrive_files(10)
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
