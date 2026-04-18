# ebay_api.py（正しい API URL 版）
import logging
import requests
import base64
import os
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

EBAY_APP_ID = os.getenv("EBAY_APP_ID")
EBAY_CERT_ID = os.getenv("EBAY_CERT_ID")

if not EBAY_APP_ID or not EBAY_CERT_ID:
    print('❌ .env が正しく設定されていません')
else:
    print('✅ .env は OK')

# ★★★ 正しい eBay API エンドポイント ★★★
EBAY_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"
EBAY_BROWSE_API_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

def get_fresh_token():
    """OAuth 2.0 でトークンを取得"""
    
    if not EBAY_APP_ID or not EBAY_CERT_ID:
        logger.error("❌ EBAY_APP_ID または EBAY_CERT_ID が設定されていません")
        return None
    
    # ★ Base64 エンコード（APP_ID:CERT_ID）
    auth_str = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # ★ OAuth リクエスト
    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    
    try:
        logger.debug(f"🔐 eBay OAuth トークン取得中...")
        response = requests.post(
            EBAY_OAUTH_URL,
            headers=headers,
            data=data,
            timeout=10
        )
        
        logger.debug(f"📡 ステータス: {response.status_code}")
        logger.debug(f"📝 レスポンス: {response.text[:200]}")
        
        if response.status_code != 200:
            logger.error(f"❌ トークン取得失敗: {response.status_code}")
            logger.error(f"詳細: {response.text}")
            return None
        
        token = response.json().get("access_token")
        if token:
            logger.info(f"✅ トークン取得成功（有効期限: {response.json().get('expires_in')}秒）")
            return token
        else:
            logger.error(f"❌ access_token が見つかりません")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 通信エラー: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ トークン取得エラー: {e}")
        return None


def search_ebay(keyword: str, max_results: int = 5, debug: bool = False) -> list:
    """eBay Browse API で商品検索"""
    
    # トークンを取得
    token = get_fresh_token()
    if not token:
        logger.error("❌ eBay トークンが取得できません")
        return []
    
    # ★ API リクエストヘッダー
    headers = {
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # ★ クエリパラメータ
    params = {
        "q": keyword,
        "limit": max_results,
        "filter": "buyingOptions:{FIXED_PRICE}",  # 定価品のみ
        "sort": "PRICE"  # 価格順
    }
    
    try:
        logger.info(f"🔍 eBay Browse API で '{keyword}' を検索中...")
        
        response = requests.get(
            EBAY_BROWSE_API_URL,
            headers=headers,
            params=params,
            timeout=10
        )
        
        logger.debug(f"📡 ステータス: {response.status_code}")
        logger.debug(f"📝 レスポンス: {response.text[:300]}")
        
        if response.status_code != 200:
            logger.error(f"❌ API エラー: {response.status_code}")
            logger.error(f"詳細: {response.text}")
            return []
        
        data = response.json()
        
        if "itemSummaries" not in data:
            logger.warning(f"⚠️ eBay から商品が見つかりません")
            return []
        
        items = []
        for idx, item in enumerate(data.get("itemSummaries", [])):
            try:
                title = item.get("title", "")
                
                # 価格取得
                price_info = item.get("price", {})
                if isinstance(price_info, dict):
                    price_usd = float(price_info.get("value", 0))
                else:
                    price_usd = float(str(price_info).replace("$", "").replace(",", ""))
                
                if price_usd <= 0 or not title:
                    logger.debug(f"Item {idx}: 除外（価格={price_usd}, タイトル={title}）")
                    continue
                
                item_id = item.get("itemId", "")
                link = f"https://www.ebay.com/itm/{item_id}"
                
                items.append({
                    "title": title,
                    "price": price_usd,
                    "link": link,
                    "source": "ebay"
                })
                
                logger.info(f"✓ [{idx+1}] {title[:40]} - ${price_usd}")
                
            except Exception as e:
                logger.debug(f"Item {idx}: パースエラー: {e}")
                continue
        
        logger.info(f"✅ eBay から {len(items)} 件の商品を取得しました")
        return items
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 通信エラー: {e}")
        return []
    except Exception as e:
        logger.error(f"❌ eBay 検索エラー: {e}")
        import traceback
        traceback.print_exc()
        return []
