# main_menu.py
import os
import csv
import sys
from dotenv import load_dotenv
from ebay_api_tool import eBayProfitCalculator
from pokemon_normalizer import normalize_pokemon_data

load_dotenv()

OUTPUT_PATH = r"C:\Users\yoshi\OneDrive\Desktop\ebay_lens.csv"
EBAY_CLIENT_ID = os.getenv('EBAY_CLIENT_ID')
EBAY_CLIENT_SECRET = os.getenv('EBAY_CLIENT_SECRET')

def diagnose_environment():
    """環境設定診断"""
    print("="*60)
    print("eBay API 環境設定診断")
    print("="*60)
    
    env_path = os.path.join(os.path.expanduser("~"), ".env")
    print(f"\n.env ファイルパス: {env_path}")
    print(f".env ファイル存在: {os.path.exists(env_path)}")
    
    print(f"\nEBAY_CLIENT_ID: {EBAY_CLIENT_ID if EBAY_CLIENT_ID else '❌ 設定されていません'}")
    print(f"EBAY_CLIENT_SECRET: {EBAY_CLIENT_SECRET if EBAY_CLIENT_SECRET else '❌ 設定されていません'}")
    
    if EBAY_CLIENT_ID and EBAY_CLIENT_SECRET:
        print("\n✓ 設定は正常です")
    else:
        print("\n❌ 設定に問題があります")
        print("\n解決方法:")
        print("1. C:\\Users\\yoshi\\.env を開く")
        print("2. 以下の内容が正しいか確認:")
        print("   EBAY_CLIENT_ID=あなたのクライアントID")
        print("   EBAY_CLIENT_SECRET=あなたのクライアントシークレット")
    print()

def run_profit_calculator():
    """利益計算ツール（run_calc.py を統合）"""
    print("="*60)
    print("eBay 利益計算ツール")
    print("="*60)
    
    calc = eBayProfitCalculator()
    query = input("\n検索ワード（例: Pikachu）: ").strip()
    
    if not query:
        print("❌ 検索ワードを入力してください")
        return
    
    print(f"\n🔍 '{query}' の売却済み商品を取得中...")
    items = calc.search_sold_items(query, limit=200)
    
    if not items:
        print("❌ 商品が見つかりませんでした")
        return
    
    print(f"✓ {len(items)} 件の商品を取得しました\n")
    calc.analyze_and_display(items, min_profit=20.0)
    print()

def create_lens_csv():
    """Google Lens CSV生成（ebay_lens_script.py を統合）"""
    print("="*60)
    print("Google Lens CSV ジェネレーター")
    print("="*60)
    
    calc = eBayProfitCalculator()
    query = input("\n検索ワード（例: Pikachu）: ").strip()
    
    if not query:
        print("❌ 検索ワードを入力してください")
        return
    
    print(f"\n🔍 '{query}' の売却済み商品を取得中...")
    items = calc.search_sold_items(query, limit=200)
    
    if not items:
        print("❌ 商品が見つかりませんでした")
        return
    
    print(f"✓ {len(items)} 件の商品を取得しました")
    
    def create_lens_url(image_url):
        """Google Lens URL生成"""
        return f"https://lens.google.com/uploadbyurl?url={image_url}"
    
    try:
        with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["title", "price", "lens_url"])
            
            count = 0
            for item in items:
                gallery_url = item.get("galleryURL", "")
                if gallery_url:
                    writer.writerow([
                        item.get("title", ""),
                        item.get("price", 0),
                        create_lens_url(gallery_url)
                    ])
                    count += 1
        
        print(f"\n✅ CSV作成完了: {OUTPUT_PATH}")
        print(f"   {count} 件の商品を記録しました\n")
    except Exception as e:
        print(f"❌ エラー: {e}\n")

def manual_profit_calc():
    """手動利益計算"""
    print("="*60)
    print("手動利益計算ツール")
    print("="*60)
    
    try:
        price_usd = float(input("\neBay売却価格(USD): $"))
        cost_jpy = float(input("日本仕入価格(JPY): ¥"))
        weight_kg = float(input("重量(kg): "))
        
        calc = eBayProfitCalculator()
        result = calc.calculate_profit(price_usd, cost_jpy, weight_kg)
        
        print("\n" + "="*40)
        print("📊 利益計算結果")
        print("="*40)
        print(f"送料:      ¥{result['shipping_jpy']} (${result['shipping_usd']})")
        print(f"利益:      ${result['profit_usd']} / ¥{result['profit_jpy']}")
        print(f"利益率:    {result['profit_rate']}%")
        print("="*40)
        
        if result['profit_rate'] >= 25:
            print("🟢 判定: 仕入推奨")
        elif result['profit_rate'] >= 15:
            print("🟡 判定: 要検討")
        else:
            print("🔴 判定: 非推奨")
        print()
    except ValueError:
        print("❌ 数値で入力してください\n")

def main_menu():
    """メインメニュー"""
    while True:
        print("="*60)
        print("🎮 eBay Sandbox Tool メインメニュー")
        print("="*60)
        print("1. 環境設定診断")
        print("2. eBay利益計算（API検索）")
        print("3. Google Lens CSV生成")
        print("4. 手動利益計算")
        print("5. 終了")
        print("="*60)
        
        choice = input("選択してください (1-5): ").strip()
        
        if choice == "1":
            diagnose_environment()
        elif choice == "2":
            run_profit_calculator()
        elif choice == "3":
            create_lens_csv()
        elif choice == "4":
            manual_profit_calc()
        elif choice == "5":
            print("👋 終了します")
            sys.exit(0)
        else:
            print("❌ 1-5 を入力してください\n")

if __name__ == "__main__":
    main_menu()
