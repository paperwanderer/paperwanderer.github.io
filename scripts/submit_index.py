#!/usr/bin/env python3
"""
Google Indexing API — sitemap URL 일괄 색인 요청
사용법: python3 scripts/submit_index.py
"""

import json
import time
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleRequest

SCOPES = ["https://www.googleapis.com/auth/indexing"]
SITEMAP_URL = "https://paperwanderer.github.io/sitemap.xml"
API_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

# 프로젝트 루트에서 JSON 키 파일 자동 탐색
def find_key_file():
    root = Path(__file__).parent.parent
    keys = list(root.glob("*.json"))
    if not keys:
        raise FileNotFoundError("서비스 계정 JSON 파일을 찾을 수 없습니다.")
    return str(keys[0])

def get_credentials():
    key_file = find_key_file()
    creds = service_account.Credentials.from_service_account_file(key_file, scopes=SCOPES)
    creds.refresh(GoogleRequest())
    return creds

def get_sitemap_urls():
    print(f"사이트맵 확인: {SITEMAP_URL}")
    resp = requests.get(SITEMAP_URL, timeout=15)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in root.findall(".//sm:loc", ns)]
    print(f"총 {len(urls)}개 URL 발견\n")
    return urls

def submit_url(session, token, url):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {"url": url, "type": "URL_UPDATED"}
    resp = session.post(API_ENDPOINT, headers=headers, json=body, timeout=15)
    return resp.status_code, resp.json()

def main():
    creds = get_credentials()
    token = creds.token

    urls = get_sitemap_urls()
    session = requests.Session()

    ok, fail = 0, 0
    for i, url in enumerate(urls, 1):
        status, result = submit_url(session, token, url)
        if status == 200:
            print(f"[{i:3}/{len(urls)}] ✅ {url}")
            ok += 1
        else:
            err = result.get("error", {}).get("message", str(result))
            print(f"[{i:3}/{len(urls)}] ❌ {url} — {err}")
            fail += 1
        # API 할당량: 초당 200건 허용, 여유 있게 0.1초 간격
        time.sleep(0.1)

    print(f"\n완료: 성공 {ok}건 / 실패 {fail}건")

if __name__ == "__main__":
    main()
