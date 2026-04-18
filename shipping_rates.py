# shipping_rates.py
"""
送料計算モジュール
- eBay SpeedPAK（アメリカ）
- Japan Post EPacket Light（その他地域）
"""

# ===== eBay SpeedPAK（アメリカ宛）=====
SPEEDPAK_USA_RATES = {
    0.1: 1227,
    0.2: 1367,
    0.3: 1581,
    0.4: 1778,
    0.5: 2060,
    0.6: 2222,
    0.7: 2321,
    0.8: 2703,
    0.9: 2820,
    1.0: 3020,
    1.1: 3136,
    1.2: 3250,
    1.3: 3366,
    1.4: 3704,
    1.5: 3816,
    1.6: 3935,
    1.7: 4046,
    1.8: 4165,
    1.9: 5056,
    2.0: 5245,
    2.5: 5582,
    3.0: 6333,
    3.5: 6958,
    4.0: 7704,
    4.5: 9135,
    5.0: 11733,
    5.5: 12500,
    6.0: 13335,
    6.5: 14160,
    7.0: 15209,
    7.5: 16058,
    8.0: 16893,
    8.5: 17562,
    9.0: 18152,
    9.5: 19106,
    10.0: 19639,
    10.5: 20276,
    11.0: 20864,
    11.5: 21565,
    12.0: 22199,
    12.5: 22887,
    13.0: 23466,
    13.5: 24054,
    14.0: 24869,
    14.5: 25200,
    15.0: 25988,
    15.5: 26656,
    16.0: 28149,
    16.5: 28775,
    17.0: 29495,
    17.5: 30196,
    18.0: 30902,
    18.5: 31478,
    19.0: 32204,
    19.5: 32936,
    20.0: 33947,
    20.5: 34655,
    21.0: 35426,
    21.5: 36145,
    22.0: 36859,
    22.5: 37602,
    23.0: 38516,
    23.5: 39084,
    24.0: 39678,
    24.5: 40374,
    25.0: 40955,
}

# ===== Japan Post EPacket Light（その他国） =====
# 第1地帯：中国・韓国・台湾
EPACKET_ZONE1 = {
    0.1: 720,
    0.2: 820,
    0.3: 920,
    0.4: 1020,
    0.5: 1120,
    0.6: 1220,
    0.7: 1320,
    0.8: 1420,
    0.9: 1520,
    1.0: 1620,
    1.1: 1720,
    1.2: 1820,
    1.3: 1920,
    1.4: 2020,
    1.5: 2120,
    1.6: 2220,
    1.7: 2320,
    1.8: 2420,
    1.9: 2520,
    2.0: 2620,
}

# 第2地帯：アジア（中国・韓国・台湾を除く）
EPACKET_ZONE2 = {
    0.1: 750,
    0.2: 870,
    0.3: 990,
    0.4: 1110,
    0.5: 1230,
    0.6: 1350,
    0.7: 1470,
    0.8: 1590,
    0.9: 1710,
    1.0: 1830,
    1.1: 1950,
    1.2: 2070,
    1.3: 2190,
    1.4: 2310,
    1.5: 2430,
    1.6: 2550,
    1.7: 2670,
    1.8: 2790,
    1.9: 2910,
    2.0: 3030,
}

# 第3地帯：オセアニア・カナダ・メキシコ・中近東・ヨーロッパ
EPACKET_ZONE3 = {
    0.1: 880,
    0.2: 1060,
    0.3: 1240,
    0.4: 1420,
    0.5: 1600,
    0.6: 1780,
    0.7: 1960,
    0.8: 2140,
    0.9: 2320,
    1.0: 2500,
    1.1: 2680,
    1.2: 2860,
    1.3: 3040,
    1.4: 3220,
    1.5: 3400,
    1.6: 3580,
    1.7: 3760,
    1.8: 3940,
    1.9: 4120,
    2.0: 4300,
}

# 第4地帯：米国（グアム等海外領土を含む）
EPACKET_ZONE4 = {
    0.1: 1200,
    0.2: 1410,
    0.3: 1620,
    0.4: 1830,
    0.5: 2040,
    0.6: 2250,
    0.7: 2460,
    0.8: 2670,
    0.9: 2880,
    1.0: 3090,
    1.1: 3300,
    1.2: 3510,
    1.3: 3720,
    1.4: 3930,
    1.5: 4140,
    1.6: 4350,
    1.7: 4560,
    1.8: 4770,
    1.9: 4980,
    2.0: 5190,
}

# 第5地帯：中南米（メキシコを除く）・アフリカ
EPACKET_ZONE5 = {
    0.1: 920,
    0.2: 1180,
    0.3: 1440,
    0.4: 1700,
    0.5: 1960,
    0.6: 2220,
    0.7: 2480,
    0.8: 2740,
    0.9: 3000,
    1.0: 3260,
    1.1: 3520,
    1.2: 3780,
    1.3: 4040,
    1.4: 4300,
    1.5: 4560,
    1.6: 4820,
    1.7: 5080,
    1.8: 5340,
    1.9: 5600,
    2.0: 5860,
}

# 国別ゾーンマッピング
COUNTRY_TO_ZONE = {
    # 第1地帯：中国・韓国・台湾
    "CN": "ZONE1",  # China
    "KR": "ZONE1",  # South Korea
    "TW": "ZONE1",  # Taiwan
    
    # 第2地帯：アジア（中国・韓国・台湾を除く）
    "JP": "ZONE2",  # Japan
    "TH": "ZONE2",  # Thailand
    "VN": "ZONE2",  # Vietnam
    "MY": "ZONE2",  # Malaysia
    "ID": "ZONE2",  # Indonesia
    "HK": "ZONE2",  # Hong Kong
    "SG": "ZONE2",  # Singapore
    "PH": "ZONE2",  # Philippines
    
    # 第3地帯：オセアニア・カナダ・メキシコ・中近東・ヨーロッパ
    "AU": "ZONE3",  # Australia
    "CA": "ZONE3",  # Canada
    "MX": "ZONE3",  # Mexico
    "DE": "ZONE3",  # Germany
    "FR": "ZONE3",  # France
    "IT": "ZONE3",  # Italy
    "ES": "ZONE3",  # Spain
    "CH": "ZONE3",  # Switzerland
    "GB": "ZONE3",  # United Kingdom
    "NL": "ZONE3",  # Netherlands
    "BE": "ZONE3",  # Belgium
    "AT": "ZONE3",  # Austria
    "AE": "ZONE3",  # UAE
    "SA": "ZONE3",  # Saudi Arabia
    
    # 第4地帯：米国（グアム等海外領土を含む）
    "US": "SPEEDPAK",  # USA - Uses SpeedPAK
    "GU": "ZONE4",  # Guam
    
    # 第5地帯：中南米（メキシコを除く）・アフリカ
    "BR": "ZONE5",  # Brazil
    "AR": "ZONE5",  # Argentina
    "ZA": "ZONE5",  # South Africa
    "EG": "ZONE5",  # Egypt
    "NG": "ZONE5",  # Nigeria
}

# EMS レート表
EMS_RATES = {
    "ZONE1": EPACKET_ZONE1,
    "ZONE2": EPACKET_ZONE2,
    "ZONE3": EPACKET_ZONE3,
    "ZONE4": EPACKET_ZONE4,
    "ZONE5": EPACKET_ZONE5,
}


def get_shipping_cost(weight_kg: float, seller_country: str = "US") -> int:
    """
    送料を計算
    
    Args:
        weight_kg: 商品重量（kg）
        seller_country: セラーの国コード（デフォルト: US）
    
    Returns:
        送料（JPY）
    """
    # 重量を切り上げ（0.1kg単位）
    import math
    weight_rounded = math.ceil(weight_kg * 10) / 10
    
    # アメリカの場合
    if seller_country == "US":
        rates = SPEEDPAK_USA_RATES
        for weight_threshold in sorted(rates.keys()):
            if weight_rounded <= weight_threshold:
                return rates[weight_threshold]
        return rates[max(rates.keys())]  # 最大重量以上の場合
    
    # その他の国
    zone = COUNTRY_TO_ZONE.get(seller_country, "ZONE3")
    if zone == "SPEEDPAK":
        zone = "ZONE4"  # SpeedPAK以外の場合は第4地帯
    
    rates = EMS_RATES.get(zone, EPACKET_ZONE3)
    
    for weight_threshold in sorted(rates.keys()):
        if weight_rounded <= weight_threshold:
            return rates[weight_threshold]
    
    return rates[max(rates.keys())]  # 最大重量以上の場合


def get_shipping_zone(seller_country: str) -> str:
    """配送ゾーン名を取得"""
    zone = COUNTRY_TO_ZONE.get(seller_country, "ZONE3")
    zone_names = {
        "SPEEDPAK": "eBay SpeedPAK (USA)",
        "ZONE1": "EPacket Zone1 (CN/KR/TW)",
        "ZONE2": "EPacket Zone2 (Asia)",
        "ZONE3": "EPacket Zone3 (EU/Oceania)",
        "ZONE4": "EPacket Zone4 (US/Territory)",
        "ZONE5": "EPacket Zone5 (Americas/Africa)",
    }
    return zone_names.get(zone, "Unknown")
