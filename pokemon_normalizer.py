# pokemon_normalizer.py
import re
from typing import List, Dict, Any

def normalize_pokemon_data(input_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    eBay売却済み商品データを正規化してグループ化
    
    Args:
        input_data: [{"title": "...", "price": 100}, ...]
    
    Returns:
        [
            {
                "name": "Pikachu_10_#028",
                "sold_count": 2,
                "average_price": 155.0,
                "min_price": 150.0,
                "max_price": 160.0
            },
            ...
        ]
    """
    pokemon_names = ["pikachu", "charizard", "blastoise", "venusaur", "mewtwo"]
    psa_pattern = r'PSA[:\s]*(\d+)'  # "PSA 10" または "PSA:10" に対応
    set_pattern = r'(#\d{3}|\d+/\d+)'
    
    grouped = {}
    
    for item in input_data:
        title = item.get("title", "")
        price = item.get("price", 0)
        
        # ポケモン名抽出
        pokemon = next(
            (p for p in pokemon_names if p.lower() in title.lower()),
            None
        )
        
        # PSA グレード抽出
        psa_match = re.search(psa_pattern, title, re.IGNORECASE)
        
        # セット番号抽出
        set_match = re.search(set_pattern, title)
        
        # すべてのフィールドが揃っている場合のみ処理
        if pokemon and psa_match and set_match:
            key = f"{pokemon.capitalize()}_{psa_match.group(1)}_{set_match.group(1)}"
            if key not in grouped:
                grouped[key] = {"prices": []}
            grouped[key]["prices"].append(price)
    
    # 結果生成
    result = []
    for k, v in grouped.items():
        prices = v["prices"]
        result.append({
            "name": k,
            "sold_count": len(prices),
            "average_price": round(sum(prices) / len(prices), 2),
            "min_price": min(prices),
            "max_price": max(prices)
        })
    
    return result


# テスト用
if __name__ == "__main__":
    test_data = [
        {"title": "2022 Pokemon Go Pikachu Holo #028 PSA 10", "price": 160.0},
        {"title": "Pokemon Go Pikachu PSA:10 #028", "price": 150.0},
        {"title": "PSA 10 Charizard 4/102 Base Set", "price": 500.0},
    ]
    
    result = normalize_pokemon_data(test_data)
    
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
