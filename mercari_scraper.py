"""
メルカリ スクレイピング
"""

import logging
import time
import urllib.parse
from typing import List, Dict

logger = logging.getLogger(__name__)

# ===== デモデータ生成 =====

def _get_mercari_demo_data(keyword: str) -> List[Dict]:
    """
    デモデータを返す
    （Vercel 環境やテスト時用）
    """
    return [
        {
            "title": f"{keyword} - メルカリ出品例1",
            "price_jpy": 8000,
            "source": "mercari",
            "status": "新品未使用",
            "item_id": "m1001"
        },
        {
            "title": f"{keyword} - メルカリ出品例2",
            "price_jpy": 7500,
            "source": "mercari",
            "status": "未使用に近い",
            "item_id": "m1002"
        },
        {
            "title": f"{keyword} - メルカリ出品例3",
            "price_jpy": 6800,
            "source": "mercari",
            "status": "目立った傷や汚れなし",
            "item_id": "m1003"
        }
    ]


# ===== Selenium を使用したスクレイピング =====

def _scrape_mercari_selenium(keyword: str) -> List[Dict]:
    """
    Selenium を使用したスクレイピング
    （ローカル環境でのみ動作）
    
    ⚠️ Vercel では動作しません
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        logger.info(f"🌐 Selenium でメルカリをスクレイピング: {keyword}")
        
        # Chrome オプション設定
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        items = []
        
        try:
            # 検索 URL を構築
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"https://jp.mercari.com/search?keyword={encoded_keyword}"
            
            logger.info(f"🔍 URL: {url}")
            driver.get(url)
            
            # ページ読み込み待機（最大 30 秒）
            wait = WebDriverWait(driver, 30)
            
            try:
                wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "[data-testid='item-list-item']")
                    )
                )
                logger.info("✅ メルカリの商品リストを検出")
            except Exception as e:
                logger.warning(f"⚠️ 商品リスト検出タイムアウト: {e}")
            
            # スクロール（遅延読み込み対策）
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(2)
            
            # 商品要素を取得
            item_elements = driver.find_elements(
                By.CSS_SELECTOR, 
                "li[data-testid='item-list-item']"
            )
            
            logger.info(f"📦 {len(item_elements)} 個の商品要素を検出")
            
            # 各商品からデータを抽出
            for item in item_elements[:50]:
                try:
                    # タイトル取得
                    title = item.find_element(
                        By.CSS_SELECTOR, 
                        "span[class*='itemName']"
                    ).text.strip()
                    
                    # 価格取得
                    price_text = item.find_element(
                        By.CSS_SELECTOR, 
                        "span[class*='price']"
                    ).text.strip()
                    
                    # 価格をパース（例：¥8,000 → 8000）
                    price = int(
                        price_text.replace('¥', '')
                                  .replace(',', '')
                                  .strip()
                    )
                    
                    # データチェック
                    if title and price > 0:
                        items.append({
                            "title": title,
                            "price_jpy": price,
                            "source": "mercari",
                            "status": "出品中"
                        })
                        logger.debug(f"✅ 抽出: {title} - ¥{price:,}")
                
                except Exception as e:
                    logger.debug(f"⚠️ 商品抽出エラー: {e}")
                    continue
            
            logger.info(f"✅ メルカリから {len(items)} 件取得")
            return items
        
        finally:
            driver.quit()
    
    except Exception as e:
        logger.error(f"❌ Selenium エラー: {e}")
        return _get_mercari_demo_data(keyword)


# ===== メイン関数 =====

def scrape_mercari(keyword: str, use_selenium: bool = False, **kwargs) -> List[Dict]:
    """
    メルカリをスクレイピング
    
    Args:
        keyword (str): 検索キーワード
        use_selenium (bool): Selenium を使用するか（デフォルト: False）
        
    Returns:
        List[Dict]: 商品リスト
    
    例：
        items = scrape_mercari("キーボード")
        items = scrape_mercari("キーボード", use_selenium=True)  # ローカル環境
    """
    
    logger.info(f"🔍 メルカリ検索: {keyword}")
    
    # Selenium を使用する場合
    if use_selenium:
        logger.info("📌 Selenium モード")
        return _scrape_mercari_selenium(keyword)
    
    # Vercel やブラウザが使用不可の環境
    logger.info("📌 デモデータ モード")
    return _get_mercari_demo_data(keyword)
