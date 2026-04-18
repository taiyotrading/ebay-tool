from ebay_client import get_active_items, get_sold_items


def get_ebay_items(keyword, mode="active"):
    """
    eBayから商品を取得
    mode: "active" = 出品中, "sold" = 売却済み
    """
    if mode == "sold":
        return get_sold_items(keyword)
    else:
        return get_active_items(keyword)
