import re
import os
import requests
import json
import base64
from dotenv import load_dotenv

def extract_item_id(url):
    match = re.search(r'/itm/(\d+)', url)
    return match.group(1) if match else None

class EBayClient:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path, override=True)
        
        # 認証情報を取得
        self.client_id = os.getenv('EBAY_CLIENT_ID')
        self.client_secret = os.getenv('EBAY_CLIENT_SECRET')
        self.runame = os.getenv('EBAY_RU_NAME')
        
        if not all([self.client_id, self.client_secret, self.runame]):
            # エラーで止めず、デバッグ情報を出す
            print("⚠️ eBay認証情報が.envに見つかりません。API機能は制限されます。")
            self.bearer_token = None
        else:
            self.bearer_token = self._get_oauth_token()
    
    def _get_oauth_token(self):
        print("🔐 OAuth トークンを取得中...")
        url = "https://api.ebay.com/identity/v1/oauth2/token"
        credentials = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {credentials}"
        }
        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                print("✅ トークン取得成功")
                return response.json().get('access_token')
            return None
        except:
            return None
    
    def search(self, keyword, country='US', **kwargs):
        # ← ここが右にずれているのが重要！
        if not self.bearer_token:
            print("❌ 認証トークンがないため検索をスキップします")
            return []
        
        print(f"🔍 '{keyword}' を検索中... (国: {country})")
        url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Accept': 'application/json'
        }
        params = {'q': keyword, 'limit': 10}
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            return response.json().get('itemSummaries', [])
        except Exception as e:
            print(f"❌ 検索エラー: {e}")
            return []

# main.pyが別の名前で呼んでも大丈夫なように設定
EBayClient.search_items = EBayClient.search
