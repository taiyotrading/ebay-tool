# ===== eBay API Configuration =====
import os
from dotenv import load_dotenv

load_dotenv()

# eBay API Credentials
EBAY_APP_ID = "KAORIAMA-reserach-PRD-fbf3e7de3-0d061dd3"
EBAY_API_ENDPOINT = "https://svcs.ebay.com/services/search/FindingService/v1"

# Exchange Rate
EXCHANGE_RATE = 155

# Fee Rates
EBAY_FEE_RATE = 0.20
IMPORT_TAX_RATE = 0.10
MERCARI_FEE_RATE = 0.10

# Shipping Methods
SHIPPING_METHODS = {
    'speedpak': {'name': 'SpeedPAK', 'base_cost': 800, 'per_unit': 400},
    'ems': {'name': 'EMS', 'base_cost': 1500, 'per_unit': 500}
}

DEFAULT_SHIPPING = 'speedpak'

# Search Settings
MIN_MERCARI_LISTINGS = 3
MIN_EBAY_LISTINGS = 3
KEYWORD = "keyboard"

# Supported Countries
SUPPORTED_COUNTRIES = {
    'US': {'name': 'United States', 'apply_tariff': True, 'tariff_rate': 0.1},
    'CA': {'name': 'Canada', 'apply_tariff': True, 'tariff_rate': 0.1},
    'UK': {'name': 'United Kingdom', 'apply_tariff': True, 'tariff_rate': 0.2},
    'JP': {'name': 'Japan', 'apply_tariff': False, 'tariff_rate': 0.0}
}

# Export Fields
EXPORT_FIELDS = {
    'item_id': 'ID',
    'title': 'Title',
    'price': 'Price'
}

# Output Path
LENS_CSV_OUTPUT = 'output.csv'
TARGET_MARKET = 'JP'
apply_tariff = True

# eBay Configuration
EBAY_CONF = {
    'apply_tariff': True,
    'exchange_rate': 150.0,
    'ebay_fee_rate': 0.15,
    'import_tax_rate': 0.1,
}

# Validation Function
def validate_config():
    """Validate configuration values"""
    if not SUPPORTED_COUNTRIES:
        raise ValueError("SUPPORTED_COUNTRIES is not defined")
    if not EXPORT_FIELDS:
        raise ValueError("EXPORT_FIELDS is not defined")
    return True

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