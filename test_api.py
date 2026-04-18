from ebay_client import get_sold_items

print("🔍 テスト開始...")
result = get_sold_items("256612")
print(f"📊 結果: {result}")
print(f"✅ 件数: {len(result)}")
