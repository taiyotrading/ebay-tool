import logging
from config import (
    EXCHANGE_RATE,
    EBAY_FEE_RATE,
    IMPORT_TAX_RATE,
    MERCARI_FEE_RATE,
    SHIPPING_METHODS,
    DEFAULT_SHIPPING,
)
from calc import calculate_shipping_cost, calculate_profit

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def analyze_and_rank(mercari_items, ebay_search_results):
    if not mercari_items or not ebay_search_results:
        logger.warning("❌ Mercari または eBay のデータが不足しています")
        return []
    
    analyzed_items = []
    
    for mercari_item in mercari_items:
        mercari_price = mercari_item.get('price', 0)
        mercari_title = mercari_item.get('title', 'Unknown')
        
        matching_ebay = [
            item for item in ebay_search_results
            if _is_matching_item(mercari_title, item.get('title', ''))
        ]
        
        if not matching_ebay:
            logger.debug(f"⚠️  '{mercari_title}' に合致する eBay アイテムがありません")
            continue
        
        best_ebay = max(matching_ebay, key=lambda x: float(x.get('price', 0)))
        ebay_price = float(best_ebay.get('price', 0))
        
        shipping_cost_jpy = calculate_shipping_cost(
            weight_kg=mercari_item.get('weight', 0.5),
            method=DEFAULT_SHIPPING
        )
        
        profit_usd, profit_jpy, profit_rate = calculate_profit(
            mercari_price_jpy=mercari_price,
            ebay_price_usd=ebay_price,
            shipping_cost_jpy=shipping_cost_jpy,
            exchange_rate=EXCHANGE_RATE,
            ebay_fee_rate=EBAY_FEE_RATE,
            import_tax_rate=IMPORT_TAX_RATE,
            mercari_fee_rate=MERCARI_FEE_RATE,
        )
        
        analyzed_items.append({
            'mercari_title': mercari_title,
            'mercari_price_jpy': mercari_price,
            'ebay_title': best_ebay.get('title'),
            'ebay_price_usd': ebay_price,
            'shipping_cost_jpy': shipping_cost_jpy,
            'profit_usd': profit_usd,
            'profit_jpy': profit_jpy,
            'profit_rate': profit_rate,
        })
    
    ranked_items = sorted(analyzed_items, key=lambda x: x['profit_rate'], reverse=True)
    
    logger.info("📊 利益分析完了")
    logger.info(f"分析対象: {len(analyzed_items)} アイテム")
    
    if ranked_items:
        logger.info("\n🏆 TOP 3 利益アイテム:")
        for idx, item in enumerate(ranked_items[:3], 1):
            logger.info(
                f"\n{idx}. {item['mercari_title']}\n"
                f"   Mercari: ¥{item['mercari_price_jpy']:,.0f}\n"
                f"   eBay: \n"
                f"   利益: ¥{item['profit_jpy']:,.0f} ({item['profit_rate']:.1f}%)"
            )
    
    return ranked_items


def _is_matching_item(mercari_title, ebay_title):
    mercari_words = set(mercari_title.lower().split())
    ebay_words = set(ebay_title.lower().split())
    common = mercari_words & ebay_words
    return len(common) >= 3