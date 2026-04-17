# ebay_auth.py
import os
import json
import webbrowser
from dotenv import load_dotenv
import requests

load_dotenv()

APP_ID = os.getenv('EBAY_CLIENT_ID')
CLIENT_SECRET = os.getenv('EBAY_CLIENT_SECRET')
REDIRECT_URI = "https://localhost:8080/callback"
SANDBOX_AUTH_URL = "https://auth.sandbox.ebay.com/oauth2/authorize"
SANDBOX_TOKEN_URL = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"

def get_authorization_code():
    """Authorization Code フロー - ステップ1: ユーザー認可"""
    
    auth_params = {
        "client_id": APP_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    
    auth_url = f"{SANDBOX_AUTH_URL}?{'&'.join(f'{k}={v}' for k, v in auth_params.items())}"
    print(f"\n🌐 ブラウザで以下のURLにアクセスしてください:\n{auth_url}\n")
    webbrowser.open(auth_url)
    
    auth_code = input("リダイレクト後のURLから 'code=' パラメータをコピペしてください: ").strip()
    return auth_code

def exchange_code_for_token(auth_code: str) -> str:
    """Authorization Code フロー - ステップ2: アクセストークン取得"""
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": APP_ID,
        "client_secret": CLIENT_SECRET,
    }
    
    try:
        response = requests.post(SANDBOX_TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        print(f"\n✅ アクセストークン取得成功!")
        print(f"Token: {access_token}\n")
        
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"❌ トークン取得失敗: {e}")
        return None

def main():
    """メイン処理"""
    print("="*60)
    print("eBay OAuth2 認証フロー")
    print("="*60)
    
    if not APP_ID or not CLIENT_SECRET:
        print("❌ EBAY_CLIENT_ID または EBAY_CLIENT_SECRET が設定されていません")
        return
    
    auth_code = get_authorization_code()
    if auth_code:
        exchange_code_for_token(auth_code)

if __name__ == "__main__":
    main()
