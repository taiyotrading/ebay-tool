# test_calc_mock.py
from statistics import mean
from collections import defaultdict
import re

class TestCalculator:
    """テスト用の簡易カルキュレーター"""
    
    POKEMON_NAMES = ['pikachu', 'charizard', 'mewtwo', 'bulbasaur', 'squirtle']
    EXCHANGE_RATE = 155
    
    def extract_product_info(self, title: str) -> tuple:
        """タイトルからポケモン名を抽出"""
        pokemon_name = ""
        psa_grade = ""
        set_number = ""
        
        # タイトルをクリーンアップ
        cleaned_title = re.sub(r'\s*\(.*?\)\s*', ' ', title)
        cleaned_title = re.sub(r'\s*(PSA|Graded).*$', '', cleaned_title, flags=re.IGNORECASE)
        
        # 不要ワード削除
        unwanted_patterns = ['pokemon', 'card', 'psa']
        for pattern in unwanted_patterns:
            cleaned_title = re.sub(pattern, ' ', cleaned_title, flags=re.IGNORECASE)
        
        # ポケモン名抽出
        words = cleaned_title.split()
        for word in words:
            word_clean = word.lower().strip('.,!-')
            if word_clean.isdigit():
                continue
            if word_clean in self.POKEMON_NAMES:
                pokemon_name = word
                break
        
        if not pokemon_name and words:
            pokemon_name = words[0]
        
        return pokemon_name, psa_grade, set_number
    
    def calculate_cost(self, avg_price_usd: float, markup_rate: float = 0.6) -> float:
        """
        日本仕入価格を計算
        
        Args:
            avg_price_usd: eBay平均売却価格（USD）
            markup_rate: マークアップ率（デフォルト: 60%）
        
        Returns:
            仕入価格（JPY）
        """
        return avg_price_usd * self.EXCHANGE_RATE * markup_rate
    
    def calculate_profit(self, avg_price_usd: float, cost_jpy: float) -> dict:
        """利益を計算"""
        fee_rate = 0.20
        revenue_usd = avg_price_usd * (1 - fee_rate)
        cost_usd = cost_jpy / self.EXCHANGE_RATE
        profit_usd = revenue_usd - cost_usd
        profit_jpy = profit_usd * self.EXCHANGE_RATE
        profit_rate = (profit_usd / avg_price_usd) * 100 if avg_price_usd > 0 else 0
        
        return {
            "profit_usd": profit_usd,
            "profit_jpy": profit_jpy,
            "profit_rate": profit_rate
        }
    
    def analyze_and_display(self, items: list, min_profit_rate: float = 40):
        """商品を分析して表示"""
        # 商品をポケモン名でグループ化
        groups = defaultdict(list)
        for item in items:
            pokemon_name, _, _ = self.extract_product_info(item['title'])
            groups[pokemon_name].append(item['price'])
        
        # 集計と表示
        print("="*60)
        print(f"{'ポケモン':<12} {'Avg Price':<12} {'Profit':<12} {'Rate %':<8}")
        print("="*60)
        
        for pokemon, prices in groups.items():
            avg_price = mean(prices)
            cost_jpy = self.calculate_cost(avg_price)
            result = self.calculate_profit(avg_price, cost_jpy)
            profit_rate = result["profit_rate"]
            
            if profit_rate >= min_profit_rate:
                print(
                    f"{pokemon:<12} ${avg_price:<11.2f} ${result['profit_usd']:<11.2f} "
                    f"{profit_rate:<7.2f}"
                )
        
        print("="*60)


# テスト実行
if __name__ == "__main__":
    mock_items = [
        {'title': 'Pikachu PSA 10', 'price': 100},
        {'title': 'Charizard PSA 9', 'price': 500},
        {'title': 'Mewtwo PSA 8', 'price': 150},
        {'title': 'Pikachu Promo', 'price': 80},
    ]
    
    calc = TestCalculator()
    calc.analyze_and_display(mock_items, min_profit_rate=40)
