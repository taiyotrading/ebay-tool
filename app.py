"""
eBay 利益分析ツール - Flask サーバー
"""

import os
import logging
from datetime import datetime

# ===== ロギング設定 =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== インポート =====
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import (
    SUPPORTED_COUNTRIES,
    EXPORT_FIELDS,
    validate_config,
)
from ebay_client import EBayClient
from mercari_scraper import scrape_mercari
from calc import calculate_profit

# ===== グローバル変数 =====
ebay_client = None
logger = logging.getLogger(__name__)

# ===== Flask アプリ初期化 =====
app = Flask(__name__)
CORS(app)  # 🔓 GitHub Pages からのアクセスを許可

logger.info("✅ Flask アプリケーション初期化完了")


def initialize_tools():
    """ツール初期化"""
    global ebay_client
    try:
        ebay_client = EBayClient()
        logger.info("✅ EBayClient 初期化完了")
    except Exception as e:
        logger.error(f"❌ EBayClient 初期化エラー: {e}")


# ===== API エンドポイント =====

@app.route('/', methods=['GET'])
def index():
    """ルートパス"""
    return jsonify({
        'message': 'eBay Profit Analyzer API',
        'version': '1.0',
        'endpoints': {
            'health': 'GET /api/health',
            'search': 'POST /api/search',
            'analyze': 'POST /api/analyze',
            'compare': 'POST /api/compare'
        },
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/health', methods=['GET'])
def health():
    """ヘルスチェック"""
    return jsonify({
        'status': 'ok',
        'message': 'eBay 利益分析ツール サーバー稼働中',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/search', methods=['POST'])
def api_search():
    """
    eBay 検索 API
    
    リクエスト例：
    {
        "keyword": "keyboard",
        "seller_country": "US",
        "limit": 10
    }
    
    レスポンス例：
    {
        "success": true,
        "count": 5,
        "results": [
            {
                "item_id": "123456789",
                "title": "Mechanical Keyboard",
                "price_usd": 150.00,
                "condition": "NEW",
                "item_url": "https://ebay.com/itm/123456789"
            }
        ]
    }
    """
    try:
        initialize_tools()
        
        # リクエストデータを取得
        data = request.get_json() or {}
        keyword = data.get('keyword', '').strip()
        seller_country = data.get('seller_country', 'US')
        limit = int(data.get('limit', 10))
        
        # バリデーション
        if not keyword:
            return jsonify({
                'success': False,
                'error': 'キーワードが必要です'
            }), 400
        
        if seller_country not in SUPPORTED_COUNTRIES:
            return jsonify({
                'success': False,
                'error': f'サポートされていない国です: {seller_country}'
            }), 400
        
        logger.info(f"🔍 検索: {keyword} (国: {seller_country}, 件数: {limit})")
        
        # eBay 検索
        items = ebay_client.search(
            keyword, 
            country=seller_country, 
            limit=limit
        )
        
        if not items:
            return jsonify({
                'success': True,
                'count': 0,
                'results': [],
                'message': '検索結果がありません'
            })
        
        # 各アイテムを整形
        results = []
        for item in items[:limit]:
            try:
                # eBay API のレスポンス形式に対応
                result_item = {
                    'item_id': item.get('itemId', 'N/A'),
                    'title': item.get('title', 'N/A'),
                    'price_usd': float(
                        item.get('price', {}).get('value', 0) or 0
                    ),
                    'condition': item.get('condition', 'N/A'),
                    'image_url': item.get('image', {}).get('imageUrl', ''),
                    'item_url': item.get('itemWebUrl', ''),
                    'seller_country': seller_country,
                    'source': 'ebay'
                }
                results.append(result_item)
            except Exception as e:
                logger.warning(f"⚠️ アイテム処理エラー: {e}")
                continue
        
        logger.info(f"✅ {len(results)} 件を返却します")
        
        return jsonify({
            'success': True,
            'count': len(results),
            'keyword': keyword,
            'country': seller_country,
            'results': results
        })
    
    except Exception as e:
        logger.error(f"❌ 検索 API エラー: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    手動分析 API
    
    リクエスト例：
    {
        "items": [
            {
                "title": "Apple AirPods",
                "price_usd": 150,
                "weight_kg": 0.3,
                "seller_country": "US",
                "is_ddp": false
            }
        ]
    }
    
    レスポンス例：
    {
        "success": true,
        "count": 1,
        "results": [
            {
                "title": "Apple AirPods",
                "price_usd": 150,
                "profit_jpy": 5000,
                "margin_pct": 25.5,
                "rank": "✅ 検討"
            }
        ]
    }
    """
    try:
        initialize_tools()
        
        # リクエストデータを取得
        data = request.get_json() or {}
        items = data.get('items', [])
        
        # バリデーション
        if not items:
            return jsonify({
                'success': False,
                'error': 'アイテムが必要です'
            }), 400
        
        results = []
        
        for item in items:
            try:
                # 必須フィールドをチェック
                if not all(key in item for key in ['title', 'price_usd', 'weight_kg']):
                    logger.warning(f"⚠️ 必須フィールドが不足: {item}")
                    continue
                
                seller_country = item.get('seller_country', 'US')
                is_ddp = item.get('is_ddp', False)
                
                # 利益計算
                result = calculate_profit(
                    price_usd=float(item['price_usd']),
                    weight_kg=float(item['weight_kg']),
                    seller_country=seller_country,
                    is_ddp=is_ddp
                )
                
                # ランキング判定
                margin = result.get('margin_pct', 0)
                if margin >= 30:
                    rank = "🔥 推奨"
                elif margin >= 20:
                    rank = "✅ 検討"
                elif margin >= 10:
                    rank = "⚠️ 要検討"
                else:
                    rank = "❌ 見送り"
                
                analysis = {
                    'title': item['title'],
                    'price_usd': item['price_usd'],
                    'weight_kg': item['weight_kg'],
                    'seller_country': seller_country,
                    'profit_jpy': result.get('profit_jpy', 0),
                    'margin_pct': margin,
                    'rank': rank,
                    'purchase_price_jpy': result.get('purchase_price_jpy', 0),
                    'shipping_cost': result.get('shipping_cost', 0),
                    'tariff': result.get('tariff', 0),
                    'total_cost_jpy': result.get('total_cost_jpy', 0),
                    'sales_price_jpy': result.get('sales_jpy', 0)
                }
                results.append(analysis)
                
                logger.info(f"✅ 分析完了: {item['title']} (利益率: {margin:.1f}%)")
                
            except Exception as e:
                logger.error(f"❌ アイテム分析エラー: {e}")
                continue
        
        if not results:
            return jsonify({
                'success': False,
                'error': '分析可能なアイテムがありません'
            }), 400
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results
        })
    
    except Exception as e:
        logger.error(f"❌ 分析 API エラー: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/compare', methods=['POST'])
def api_compare():
    """
    eBay と メルカリの価格比較 API
    
    リクエスト例：
    {
        "keyword": "keyboard",
        "seller_country": "US"
    }
    """
    try:
        initialize_tools()
        
        data = request.get_json() or {}
        keyword = data.get('keyword', '').strip()
        seller_country = data.get('seller_country', 'US')
        
        if not keyword:
            return jsonify({
                'success': False,
                'error': 'キーワードが必要です'
            }), 400
        
        logger.info(f"🔄 価格比較: {keyword}")
        
        # eBay 検索
        ebay_items = ebay_client.search(
            keyword, 
            country=seller_country, 
            limit=5
        )
        
        # メルカリ検索
        mercari_items = scrape_mercari(keyword)
        
        return jsonify({
            'success': True,
            'keyword': keyword,
            'ebay': {
                'count': len(ebay_items),
                'items': ebay_items[:5]
            },
            'mercari': {
                'count': len(mercari_items),
                'items': mercari_items[:5]
            }
        })
    
    except Exception as e:
        logger.error(f"❌ 比較 API エラー: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ===== エラーハンドリング =====

@app.errorhandler(404)
def not_found(error):
    """404 エラー"""
    return jsonify({
        'success': False,
        'error': 'エンドポイントが見つかりません'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """500 エラー"""
    return jsonify({
        'success': False,
        'error': 'サーバーエラーが発生しました'
    }), 500


# ===== サーバー起動 =====
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"🚀 サーバーを起動します... (ポート: {port})")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )