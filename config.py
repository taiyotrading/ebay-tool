# ===== eBay API 認証情報 =====
import os
from dotenv import load_dotenv

load_dotenv()

EBAY_APP_ID = "KAORIAMA-reserach-PRD-fbf3e7de3-0d061dd3"
EBAY_API_ENDPOINT = "https://svcs.ebay.com/services/search/FindingService/v1"

# 為替レート (JPY to USD)
EXCHANGE_RATE = 155

# 手数料・税金設定
EBAY_FEE_RATE = 0.20  # 20%
IMPORT_TAX_RATE = 0.10  # 10%
MERCARI_FEE_RATE = 0.10  # 10%

# 配送方法設定
SHIPPING_METHODS = {
    'speedpak': {
        'name': 'SpeedPAK',
        'base_cost': 800,  # ¥
        'per_unit': 400,   # ¥ per 0.5kg
    },
    'ems': {
        'name': 'EMS',
        'base_cost': 1500,  # ¥
        'per_unit': 500,    # ¥ per 0.5kg
    }
}

# デフォルト配送方法
DEFAULT_SHIPPING = 'speedpak'

# スクレイピング設定
MIN_MERCARI_LISTINGS = 3
MIN_EBAY_LISTINGS = 3

# 検索キーワード
KEYWORD = "keyboard"

# サポート国設定
SUPPORTED_COUNTRIES = {
    'US': {
        'name': 'United States',
        'apply_tariff': True,
        'tariff_rate': 0.1
    },
    'CA': {
        'name': 'Canada',
        'apply_tariff': True,
        'tariff_rate': 0.1
    },
    'UK': {
        'name': 'United Kingdom',
        'apply_tariff': True,
        'tariff_rate': 0.2
    },
    'JP': {
        'name': 'Japan',
        'apply_tariff': False,
        'tariff_rate': 0.0
    }
}

# エクスポート設定
EXPORT_FIELDS = {
    'item_id': 'ID',
    'title': '商品名',
    'price': '価格'
}

# CSV出力パス
LENS_CSV_OUTPUT = 'output.csv'

# その他設定
TARGET_MARKET = 'JP'
apply_tariff = True

EBAY_CONF = {
    'apply_tariff': True,
    'exchange_rate': 150.0,
    'ebay_fee_rate': 0.15,
    'import_tax_rate': 0.1,
}

# 検証関数
def validate_config():
    """設定値の検証"""
    return True

# エクスポート
__all__ = [
    'SUPPORTED_COUNTRIES',
    'EXPORT_FIELDS',
    'validate_config',
    'EXCHANGE_RATE',
    'EBAY_FEE_RATE',
    'IMPORT_TAX_RATE',
    'MERCARI_FEE_RATE',
    'SHIPPING_METHODS',
    'DEFAULT_SHIPPING',
]
