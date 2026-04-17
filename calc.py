import logging

# ロガー設定
logger = logging.getLogger(__name__)

# ========== 定数 ==========
DEFAULT_SHIPPING = "standard"

SHIPPING_METHODS = {
    "standard": {"cost_base": 800, "cost_per_kg": 100},
    "express": {"cost_base": 1500, "cost_per_kg": 200},
    "dhl": {"cost_base": 2000, "cost_per_kg": 300},
}

CURRENCY_RATE = 150  # 1 USD = 150 JPY

TARIFF_RATES = {
    "US": 0.05,
    "CN": 0.15,
    "GB": 0.03,
    "JP": 0.0,
}

# ========== eBay手数料・税金定数 ========== ← これを追加！
EBAY_FEE_RATE = 0.125  # 12.5%
IMPORT_TAX_RATE = 0.08  # 8%

# ========== 配送料計算 ==========
def calculate_shipping_cost(weight_kg: float, method: str = DEFAULT_SHIPPING) -> int:
    """配送料を計算（¥）"""
    if method not in SHIPPING_METHODS:
        method = DEFAULT_SHIPPING
    
    shipping_info = SHIPPING_METHODS[method]
    cost = shipping_info["cost_base"] + (weight_kg * shipping_info["cost_per_kg"])
    
    return int(cost)


# ========== 関税計算 ==========
def calculate_tariff(price_usd: float, seller_country: str) -> float:
    """関税を計算（¥）"""
    tariff_rate = TARIFF_RATES.get(seller_country, 0.1)
    price_jpy = price_usd * CURRENCY_RATE
    tariff = price_jpy * tariff_rate
    
    return tariff


# ========== メイン利益計算 ==========
def calculate_profit(price_usd: float, weight_kg: float, seller_country: str, is_ddp: bool) -> dict:
    """利益を計算（USD → JPY）"""
    
    # 1. 仕入価格をJPYに変換
    purchase_price_jpy = price_usd * CURRENCY_RATE
    
    # 2. 配送料を計算
    shipping_cost = calculate_shipping_cost(weight_kg)
    
    # 3. 関税を計算
    tariff = 0 if is_ddp else calculate_tariff(price_usd, seller_country)
    
    # 4. 合計仕入価格
    total_cost_jpy = purchase_price_jpy + shipping_cost + tariff
    
    # 5. 販売価格（35%マージン）
    margin_multiplier = 1.35
    sales_jpy = total_cost_jpy * margin_multiplier
    
    # 6. 利益と利益率
    profit_jpy = sales_jpy - total_cost_jpy
    margin_pct = (profit_jpy / total_cost_jpy) * 100 if total_cost_jpy > 0 else 0
    
    return {
        'purchase_price_jpy': round(purchase_price_jpy, 2),
        'shipping_cost': shipping_cost,
        'tariff': round(tariff, 2),
        'total_cost_jpy': round(total_cost_jpy, 2),
        'sales_jpy': round(sales_jpy, 2),
        'profit_jpy': round(profit_jpy, 2),
        'margin_pct': round(margin_pct, 2)
    }


# ========== 利益スコア計算 ==========
def calculate_profit_score(ebay_item: dict, seller_country: str = "US") -> dict:
    """
    eBayアイテムの利益スコアを計算
    
    Args:
        ebay_item: eBay APIから取得したアイテム辞書
        seller_country: セラーの国コード
    
    Returns:
        分析結果の辞書
    """
    try:
        # アイテム情報を抽出
        title = ebay_item.get('title', '不明')
        price_usd = float(ebay_item.get('price', {}).get('value', 0))
        condition = ebay_item.get('condition', '不明')
        
        # 仮の重量（実装時に調整）
        weight_kg = 0.5
        
        # 利益計算
        profit_data = calculate_profit(
            price_usd=price_usd,
            weight_kg=weight_kg,
            seller_country=seller_country,
            is_ddp=False
        )
        
        # スコア計算（利益 * 利幅）
        profit_jpy = profit_data['profit_jpy']
        margin_pct = profit_data['margin_pct']
        score = (profit_jpy / 1000) * (margin_pct / 10) if profit_jpy > 0 else 0
        
        # ランク判定
        if score >= 100:
            rank = "⭐⭐⭐⭐⭐ (優良)"
        elif score >= 50:
            rank = "⭐⭐⭐⭐ (良好)"
        elif score >= 20:
            rank = "⭐⭐⭐ (普通)"
        elif score >= 0:
            rank = "⭐⭐ (要検討)"
        else:
            rank = "⭐ (非推奨)"
        
        return {
            'title': title,
            'price_usd': price_usd,
            'condition': condition,
            'purchase_price_jpy': profit_data['purchase_price_jpy'],
            'shipping_jpy': profit_data['shipping_cost'],
            'tariff_jpy': profit_data['tariff'],
            'sales_jpy': profit_data['sales_jpy'],
            'ebay_fee_jpy': profit_data['sales_jpy'] * EBAY_FEE_RATE,
            'tax_jpy': profit_data['sales_jpy'] * IMPORT_TAX_RATE,
            'profit_jpy': profit_jpy,
            'profit_margin': margin_pct,
            'rank': rank,
            'score': round(score, 2),
            'seller_country': seller_country,
        }
    
    except Exception as e:
        logger.error(f"利益スコア計算エラー: {e}")
        return {
            'title': '計算エラー',
            'price_usd': 0,
            'profit_jpy': 0,
            'profit_margin': 0,
            'rank': '❌ エラー',
            'score': 0,
        }


def get_rating(score: float) -> str:
    """
    スコアに基づいて評価を返す
    
    Args:
        score: スコア値
    
    Returns:
        評価文字列
    """
    if score >= 100:
        return "🟢 最高評価"
    elif score >= 50:
        return "🟢 高評価"
    elif score >= 20:
        return "🟡 中評価"
    elif score >= 0:
        return "🟠 低評価"
    else:
        return "🔴 非推奨"
