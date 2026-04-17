# ebay_api_tool.py
import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class eBayProfitCalculator:
    """eBay売却済み商品検索 + 利益計算"""
    
    # 定数
    EXCHANGE_RATE = 155  # JPY/USD
    FEE_RATE = 0.20  # 20% (15% + 5%)
    SHIPPING_RATES = {
        0.5: 2060, 0.9: 2820, 1.0: 3020, 1.5: 3816, 2.0: 5245,
    }
    DEFAULT_SHIPPING = 6000
    
    POKEMON_PATTERN = r'(pikachu|charizard|mewtwo|bulbasaur|squirtle|venusaur|blastoise)'
    
    def __init__(self):
        """初期化"""
        pass
    
    def search_sold_items(self, query: str, limit: int = 200) -> List[Dict[str, Any]]:
        """
        eBay Browse API で売却済み商品を検索
        
        Args:
            query: 検索ワード（例: "Pikachu PSA 10"）
            limit: 最大取得件数
        
        Returns:
            [{"title": "...", "price": 100.0, "galleryURL": "..."}, ...]
        """
        # TODO: 実装時に ebay_auth.py から access_token を取得
        # TODO: Browse API エンドポイント呼び出し
        # TODO: soldItems フィルター適用
        
        items = [
            {
                "title": "2022 Pokemon Go Pikachu Holo #028 PSA 10",
                "price": 160.0,
                "galleryURL": "https://example.com/image1.jpg"
            },
            {
                "title": "Pokemon Go Pikachu PSA10 #028",
                "price": 150.0,
                "galleryURL": "https://example.com/image2.jpg"
            },
        ]
        return items[:limit]
    
    def extract_pokemon_name(self, title: str) -> str:
        """タイトルからポケモン名を抽出"""
        match = re.search(self.POKEMON_PATTERN, title, re.IGNORECASE)
        return match.group(0).capitalize() if match else "Unknown"
    
    def calculate_profit(self, price_usd: float, cost_jpy: float, weight_kg: float = 1.0) -> Dict[str, Any]:
        """
        利益を計算（ebay_profit_csv.py の calc_profit() を統合）
        
        Args:
            price_usd: eBay売却価格（USD）
            cost_jpy: 日本仕入価格（JPY）
            weight_kg: 重量（デフォルト: 1.0kg）
        
        Returns:
            {
                "profit_usd": 25.50,
                "profit_jpy": 3950,
                "profit_rate": 12.5,
                "shipping_jpy": 3020,
                "shipping_usd": 19.55
            }
        """
        # 送料決定
        shipping_jpy = self.DEFAULT_SHIPPING
        for weight_threshold in sorted(self.SHIPPING_RATES.keys()):
            if weight_kg <= weight_threshold:
                shipping_jpy = self.SHIPPING_RATES[weight_threshold]
                break
        
        # 利益計算
        shipping_usd = shipping_jpy / self.EXCHANGE_RATE
        revenue_usd = price_usd * (1 - self.FEE_RATE)
        cost_usd = cost_jpy / self.EXCHANGE_RATE
        profit_usd = revenue_usd - cost_usd - shipping_usd
        profit_jpy = int(profit_usd * self.EXCHANGE_RATE)
        profit_rate = (profit_usd / price_usd) * 100 if price_usd > 0 else 0
        
        return {
            "profit_usd": round(profit_usd, 2),
            "profit_jpy": profit_jpy,
            "profit_rate": round(profit_rate, 1),
            "shipping_jpy": shipping_jpy,
            "shipping_usd": round(shipping_usd, 2)
        }
    
    def analyze_and_display(self, items: List[Dict[str, Any]], min_profit: float = 20.0):
        """
        商品を分析して表示（40%以上の利益率をフィルター）
        
        Args:
            items: eBay APIから取得した商品リスト
            min_profit: 最小利益額（USD）
        """
        print("="*80)
        print(f"{'Pokemon':<15} {'Avg Price':<12} {'Profit $':<12} {'Profit ¥':<12} {'Rate %':<8}")
        print("="*80)
        
        for item in items:
            pokemon = self.extract_pokemon_name(item.get("title", ""))
            price = item.get("price", 0)
            
            # デフォルト仕入価格（実際はDBから取得）
            cost_jpy = price * self.EXCHANGE_RATE * 0.6
            result = self.calculate_profit(price, cost_jpy, weight_kg=1.0)
            
            if result["profit_rate"] >= 40:
                print(
                    f"{pokemon:<15} ${price:<11.2f} ${result['profit_usd']:<11.2f} "
                    f"¥{result['profit_jpy']:<11} {result['profit_rate']:<7.1f}%"
                )
        
        print("="*80)
