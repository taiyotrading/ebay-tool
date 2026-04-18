import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# researcher.py（デバッグモード対応版）
import logging
from mercari_scraper import scrape_mercari
from ebay_api import search_ebay
from research_analyzer import analyze_and_rank
from config import KEYWORD
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_output.txt'),
        logging.StreamHandler()
    ]
)


class ResearchOrchestrator:
    def __init__(self, keyword: str):
        self.keyword = keyword
    
    def run(self, debug_ebay: bool = True):  # ★デバッグモードを有効化
        """リサーチ全体を実行"""
        logger.info(f"🚀 キーワード '{self.keyword}' でリサーチ開始")
        
        # [1/3] Mercari スクレイピング
        logger.info(f"🌐 [1/3] Mercari で商品を検索中...")
        mercari_items = scrape_mercari(self.keyword, max_results=100)
        logger.info(f"✅ {len(mercari_items)} 個の商品を取得しました")
        
        # [2/3] eBay 検索
        logger.info(f"🌐 [2/3] eBay で商品を検索中...")
        # 確実に動かすために debug= 引数を消し、max_resultsを合わせる
        ebay_items = search_ebay(self.keyword, max_results=50) 
        logger.info(f"✅ {len(ebay_items)} 個の商品を取得しました")
        
        # [3/3] 利益分析
        logger.info(f"📊 [3/3] 利益分析中...")
        # 条件をゆるくする（メルカリ5件以上、eBay1件以上あれば表を出す）
        if len(mercari_items) >= 5 and len(ebay_items) >= 1:
            results = analyze_and_rank(mercari_items, ebay_items, self.keyword)
            print(results) # 表を確実に表示させる
        else:
            logger.warning(f"❌ 比較できるデータが足りません")
            logger.warning(f"   Mercari: {len(mercari_items)}, eBay: {len(ebay_items)}")
        
        logger.info("\n✅ リサーチ完了！")

if __name__ == "__main__":
    print("\n" + "="*30)
    user_input = input("🔍 リサーチしたい商品名を入力してください: ")
    print("="*30 + "\n")
    
    if user_input.strip():
        # Orchestrator ではなく ResearchOrchestrator に直す
        orchestrator = ResearchOrchestrator(user_input)
        orchestrator.run()
    else:
        print("❌ キーワードが入力されなかったため、終了します。")
