import logging
import requests
from datetime import datetime

from config import (
    EXCHANGE_RATE,
    EBAY_FEE_RATE,
    IMPORT_TAX_RATE,
    MERCARI_FEE_RATE,
    SHIPPING_METHODS,
    DEFAULT_SHIPPING,
)
from calc import calculate_shipping_cost, calculate_profit

logger = logging.getLogger(__name__)

class ItemAnalyzer:
    def __init__(self):
        self.items = []
    
    def _is_matching_item(self, mercari_title, ebay_title):
        """アイテムが一致しているか判定"""
        mercari_words = set(mercari_title.lower().split())
        ebay_words = set(ebay_title.lower().split())
        common = mercari_words.intersection(ebay_words)
        return len(common) >= 3
    
    def analyze_and_rank(self, mercari_items, ebay_search_results):
        """複数アイテムを分析"""
        return []
    
    def add_item(self, **kwargs):
        """アイテムを追加"""
        self.items.append(kwargs)
        name = kwargs.get('title', 'アイテム')
        print(f"✅ {name} を追加しました")
    
    def analyze(self, *args, **kwargs):
        """分析実行"""
        return self.items
