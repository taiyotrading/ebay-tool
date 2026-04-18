import os
from dotenv import load_dotenv
import requests

# .envファイルを読み込む
load_dotenv()

# 環境変数からトークンを取得
token = os.getenv('EBAY_TOKEN')

if not token:
    print("ERROR: EBAY_TOKEN not found in .env")
    exit(1)

print(f"Token Length: {len(token)}")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# --- ここから修正部分 ---
# まずは在庫確認のAPIで権限があるかテストします
url = "https://ebay.com"
# ----------------------

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("SUCCESS: Token is VALID for Inventory API!")
    elif response.status_code == 403:
        print("ERROR: 403 Forbidden - トークンの権限（Scope）が足りません")
        print(f"Detail: {response.text}")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")