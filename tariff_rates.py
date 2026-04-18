# tariff_rates.py
"""
関税率テーブル（国別）
DDP（Delivered Duty Paid）時の関税を計算
"""

TARIFF_RATES = {
    "JP": 0.15,   # Japan
    "CN": 0.42,   # China
    "DE": 0.17,   # Germany
    "FR": 0.17,   # France
    "IT": 0.17,   # Italy
    "ES": 0.17,   # Spain
    "CH": 0.52,   # Switzerland
    "VN": 0.33,   # Vietnam
    "TW": 0.22,   # Taiwan
    "TH": 0.30,   # Thailand
    "MY": 0.38,   # Malaysia
    "ID": 0.28,   # Indonesia
    "HK": 0.33,   # Hong Kong
    "GB": 0.21,   # United Kingdom
    "KR": 0.18,   # South Korea
    "US": 0.00,   # USA (no tariff for DDP)
    "CA": 0.05,   # Canada
    "AU": 0.10,   # Australia
    "Default": 0.15,  # その他の国
}


def get_tariff_rate(seller_country: str) -> float:
    """
    国別の関税率を取得
    
    Args:
        seller_country: セラーの国コード
    
    Returns:
        関税率（0.0-1.0）
    """
    return TARIFF_RATES.get(seller_country.upper(), TARIFF_RATES["Default"])


def get_tariff_jpy(sales_jpy: int, seller_country: str) -> int:
    """
    関税額を計算
    
    Args:
        sales_jpy: 売上（JPY）
        seller_country: セラーの国コード
    
    Returns:
        関税額（JPY）
    """
    tariff_rate = get_tariff_rate(seller_country)
    tariff_jpy = int(sales_jpy * tariff_rate)
    return tariff_jpy
