import requests
from config import EBAY_TOKEN

print("🔍 Testing eBay API with current token...\n")

headers = {
    'Authorization': f'Bearer {EBAY_TOKEN}',
    'Content-Type': 'application/json'
}

# テスト1: rate_tables
url1 = 'https://api.ebay.com/sell/account/v1/rate_tables'
print(f"Test 1: {url1}")
try:
    response = requests.get(url1, headers=headers, timeout=5)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        print("  ✅ Token is VALID\n")
    else:
        print(f"  ❌ Error: {response.status_code}\n")
except Exception as e:
    print(f"  ❌ Exception: {e}\n")

# テスト2: 在庫情報取得
url2 = 'https://api.ebay.com/sell/inventory/v1/inventory?limit=1'
print(f"Test 2: {url2}")
try:
    response = requests.get(url2, headers=headers, timeout=5)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        print("  ✅ Token is VALID\n")
    else:
        print(f"  ❌ Error: {response.status_code}")
        print(f"  Response: {response.text[:200]}\n")
except Exception as e:
    print(f"  ❌ Exception: {e}\n")

# テスト3: 注文情報取得
url3 = 'https://api.ebay.com/sell/fulfillment/v1/order?limit=1'
print(f"Test 3: {url3}")
try:
    response = requests.get(url3, headers=headers, timeout=5)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        print("  ✅ Token is VALID")
        data = response.json()
        print(f"  Orders found: {len(data.get('orders', []))}\n")
    else:
        print(f"  ❌ Error: {response.status_code}")
        print(f"  Response: {response.text[:200]}\n")
except Exception as e:
    print(f"  ❌ Exception: {e}\n")
