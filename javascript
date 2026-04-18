// ステータスバーの更新
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

function updateOnlineStatus() {
    const statusBar = document.getElementById('status');
    if (navigator.onLine) {
        statusBar.textContent = '🌐 オンライン';
        statusBar.className = 'status-bar online';
    } else {
        statusBar.textContent = '📴 オフライン';
        statusBar.className = 'status-bar offline';
    }
}

// Service Worker 登録
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./service-worker.js')
            .then(registration => {
                console.log('Service Worker 登録成功:', registration);
            })
            .catch(error => {
                console.log('Service Worker 登録失敗:', error);
            });
    });
}

async function search() {
    const keyword = document.getElementById('keyword').value;
    const country = document.getElementById('country').value;
    const resultsDiv = document.getElementById('results');
    const loading = document.getElementById('loading');
    
    if (!keyword.trim()) {
        alert('キーワードを入力してください');
        return;
    }
    
    loading.style.display = 'block';
    resultsDiv.innerHTML = '';
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ keyword, country })
        });
        
        const data = await response.json();
        loading.style.display = 'none';
        
        if (data.status === 'success') {
            displayResults(data.results);
        } else {
            resultsDiv.innerHTML = `<div class="error">❌ エラー: ${data.message}</div>`;
        }
    } catch (error) {
        loading.style.display = 'none';
        resultsDiv.innerHTML = `<div class="error">❌ エラー: ${error.message}</div>`;
    }
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    
    if (results.length === 0) {
        resultsDiv.innerHTML = '<div class="error">結果が見つかりませんでした</div>';
        return;
    }
    
    let html = '';
    results.forEach((item, index) => {
        const scoreClass = item.score >= 150 ? 'score-good' : 'score-bad';
        html += `
            <div class="result-item">
                <div class="item-title">📦 ${index + 1}. ${item.title}</div>
                <div class="item-price">💵 $${item.price}</div>
                <div class="item-profit">💰 利益: ¥${Math.round(item.profit)}</div>
                <div class="item-rate">📊 利益率: ${(item.profit_rate * 100).toFixed(1)}%</div>
                <div class="item-score ${scoreClass}">
                    ⭐ スコア: ${item.score.toFixed(2)} - ${item.rating}
                </div>
            </div>
        `;
    });
    
    resultsDiv.innerHTML = html;
}

document.getElementById('keyword').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') search();
});

// 初期表示
updateOnlineStatus();
