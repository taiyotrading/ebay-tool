import logging
logger = logging.getLogger(__name__)

# ========== インポート ==========
from calc import calculate_profit
import json
import csv
from datetime import datetime


# ========== ItemAnalyzer クラス ==========
class ItemAnalyzer:
    def __init__(self):
        self.items = []
        self.results = []
    
    def add_item(self, item_id, title, current_price_usd, weight_kg, seller_country, is_ddp):
        """アイテムを追加"""
        self.items.append({
            'item_id': item_id,
            'title': title,
            'current_price_usd': current_price_usd,
            'weight_kg': weight_kg,
            'seller_country': seller_country,
            'is_ddp': is_ddp
        })
    
    def analyze_all(self):
        """全アイテムを分析"""
        self.results = []
        for item in self.items:
            result = calculate_profit(
                price_usd=item['current_price_usd'],
                weight_kg=item['weight_kg'],
                seller_country=item['seller_country'],
                is_ddp=item['is_ddp']
            )
            
            # ランキング判定
            margin = result['margin_pct']
            if margin >= 30:
                rank = "🔥 推奨"
            elif margin >= 20:
                rank = "✅ 検討"
            else:
                rank = "❌ 見送り"
            
            self.results.append({
                'item_id': item['item_id'],
                'title': item['title'],
                'current_price_usd': item['current_price_usd'],
                'weight_kg': item['weight_kg'],
                'seller_country': item['seller_country'],
                'is_ddp': item['is_ddp'],
                'purchase_price_jpy': result['purchase_price_jpy'],
                'shipping_cost': result['shipping_cost'],
                'tariff': result['tariff'],
                'total_cost_jpy': result['total_cost_jpy'],
                'sales_price_jpy': result['sales_jpy'],
                'profit_jpy': result['profit_jpy'],
                'margin_pct': result['margin_pct'],
                'rank': rank
            })
    
    def print_statistics(self):
        """統計情報を表示"""
        if not self.results:
            print("❌ 分析結果がありません")
            return
        
        print("\n" + "="*60)
        print("📊 分析結果サマリー")
        print("="*60)
        
        total_items = len(self.results)
        total_profit = sum(r['profit_jpy'] for r in self.results)
        avg_margin = sum(r['margin_pct'] for r in self.results) / total_items if total_items > 0 else 0
        
        recommended = len([r for r in self.results if r['rank'] == "🔥 推奨"])
        consider = len([r for r in self.results if r['rank'] == "✅ 検討"])
        skip = len([r for r in self.results if r['rank'] == "❌ 見送り"])
        
        print(f"📦 処理アイテム数: {total_items}")
        print(f"💰 合計利益: ¥{total_profit:,.0f}")
        print(f"📈 平均利益率: {avg_margin:.1f}%")
        print(f"🔥 推奨: {recommended}件 | ✅ 検討: {consider}件 | ❌ 見送り: {skip}件")
        print("="*60 + "\n")
    
    def print_results(self):
        """分析結果を表示"""
        if not self.results:
            print("❌ 分析結果がありません")
            return
        
        print("\n" + "="*80)
        print("🎯 詳細分析結果")
        print("="*80)
        
        for i, result in enumerate(self.results, 1):
            print(f"\n【{i}】 {result['rank']} {result['title']}")
            print(f"   商品ID: {result['item_id']}")
            print(f"   仕入価格: ${result['current_price_usd']} → ¥{result['purchase_price_jpy']:,.0f}")
            print(f"   配送料: ¥{result['shipping_cost']:,.0f}")
            print(f"   関税: ¥{result['tariff']:,.0f}")
            print(f"   合計仕入: ¥{result['total_cost_jpy']:,.0f}")
            print(f"   販売価格: ¥{result['sales_price_jpy']:,.0f}")
            print(f"   利益: ¥{result['profit_jpy']:,.0f} ({result['margin_pct']:.1f}%)")
        
        print("\n" + "="*80)
    
    def export_csv(self, filename='results.csv'):
        """結果をCSVにエクスポート"""
        if not self.results:
            print("❌ エクスポートするデータがありません")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'item_id', 'title', 'current_price_usd', 'weight_kg',
                    'seller_country', 'is_ddp', 'purchase_price_jpy',
                    'shipping_cost', 'tariff', 'total_cost_jpy',
                    'sales_price_jpy', 'profit_jpy', 'margin_pct', 'rank'
                ])
                writer.writeheader()
                writer.writerows(self.results)
            
            print(f"✅ {filename} に結果を保存しました")
        except Exception as e:
            print(f"❌ エクスポートエラー: {e}")
    
    def export_json(self, filename='results.json'):
        """結果をJSONにエクスポート"""
        if not self.results:
            print("❌ エクスポートするデータがありません")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {filename} に結果を保存しました")
        except Exception as e:
            print(f"❌ エクスポートエラー: {e}")


# ========== デモデータ ==========
def create_demo_data():
    """デモデータを作成"""
    analyzer = ItemAnalyzer()
    
    demo_items = [
        {
            'item_id': 'ITEM001',
            'title': 'Apple AirPods Pro',
            'current_price_usd': 150,
            'weight_kg': 0.3,
            'seller_country': 'US',
            'is_ddp': False
        },
        {
            'item_id': 'ITEM002',
            'title': 'Sony WH-1000XM5 Headphones',
            'current_price_usd': 250,
            'weight_kg': 0.5,
            'seller_country': 'JP',
            'is_ddp': True
        },
        {
            'item_id': 'ITEM003',
            'title': 'DJI Mini 3 Pro',
            'current_price_usd': 399,
            'weight_kg': 2.0,
            'seller_country': 'CN',
            'is_ddp': False
        },
        {
            'item_id': 'ITEM004',
            'title': 'GoPro Hero 11',
            'current_price_usd': 350,
            'weight_kg': 1.2,
            'seller_country': 'GB',
            'is_ddp': False
        }
    ]
    
    for item in demo_items:
        analyzer.add_item(
            item['item_id'],
            item['title'],
            item['current_price_usd'],
            item['weight_kg'],
            item['seller_country'],
            item['is_ddp']
        )
    
    return analyzer


# ========== モード選択 ==========
def demo_mode():
    """デモモード"""
    print("\n🎯 デモモード実行中...\n")
    
    analyzer = create_demo_data()
    analyzer.analyze_all()
    analyzer.print_results()
    analyzer.print_statistics()
    
    # エクスポート
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    analyzer.export_csv(f'results_{timestamp}.csv')
    analyzer.export_json(f'results_{timestamp}.json')


def manual_mode():
    """手動入力モード"""
    print("\n📝 手動入力モード\n")
    
    analyzer = ItemAnalyzer()
    
    while True:
        print("\n【新規アイテム追加】")
        
        try:
            item_id = input("商品ID (例: ITEM001): ").strip()
            if not item_id:
                print("❌ 商品IDは必須です")
                continue
            
            title = input("商品タイトル: ").strip()
            if not title:
                print("❌ タイトルは必須です")
                continue
            
            price_usd = float(input("eBay仕入価格 (USD): "))
            weight_kg = float(input("重量 (kg): "))
            
            print("販売国を選択:")
            print("1: US | 2: CN | 3: GB | 4: JP")
            country_choice = input("選択 (1-4): ").strip()
            country_map = {'1': 'US', '2': 'CN', '3': 'GB', '4': 'JP'}
            seller_country = country_map.get(country_choice, 'US')
            
            is_ddp_input = input("DDP配送か (y/n): ").strip().lower()
            is_ddp = is_ddp_input == 'y'
            
            analyzer.add_item(item_id, title, price_usd, weight_kg, seller_country, is_ddp)
            print(f"✅ {title} を追加しました")
            
            another = input("\nさらにアイテムを追加しますか? (y/n): ").strip().lower()
            if another != 'y':
                break
        
        except ValueError:
            print("❌ 数値を正しく入力してください")
            continue
    
    if analyzer.items:
        analyzer.analyze_all()
        analyzer.print_results()
        analyzer.print_statistics()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        analyzer.export_csv(f'results_{timestamp}.csv')
        analyzer.export_json(f'results_{timestamp}.json')
    else:
        print("❌ アイテムが追加されていません")


def main():
    """メイン関数"""
    print("\n" + "="*60)
    print("🚀 eBay利益計算ツール")
    print("="*60)
    print("\n1: 手動入力")
    print("2: デモ実行")
    print("3: 終了")
    print("="*60)
    
    choice = input("\n選択 (1-3): ").strip()
    
    if choice == '1':
        manual_mode()
    elif choice == '2':
        demo_mode()
    elif choice == '3':
        print("\n👋 終了します")
    else:
        print("\n❌ 無効な選択です")


# ========== エントリーポイント ==========
if __name__ == "__main__":
    main()
