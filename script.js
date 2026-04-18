// Constants
const CURRENCY_RATE = 150; // 1 USD = 150 JPY
const EBAY_FEE_RATE = 0.125; // 12.5%
const IMPORT_TAX_RATE = 0.08; // 8%

// Get DOM elements
const itemPriceInput = document.getElementById('itemPrice');
const shippingCostInput = document.getElementById('shippingCost');
const quantityInput = document.getElementById('quantity');

const priceJPYDisplay = document.getElementById('priceJPY');
const shippingJPYDisplay = document.getElementById('shippingJPY');
const totalCostDisplay = document.getElementById('totalCost');
const ebayFeeDisplay = document.getElementById('ebayFee');
const importTaxDisplay = document.getElementById('importTax');
const totalExpenseDisplay = document.getElementById('totalExpense');
const profitPerUnitDisplay = document.getElementById('profitPerUnit');
const totalProfitDisplay = document.getElementById('totalProfit');
const profitMarginDisplay = document.getElementById('profitMargin');

// Event listeners
itemPriceInput.addEventListener('input', calculate);
shippingCostInput.addEventListener('input', calculate);
quantityInput.addEventListener('input', calculate);

// Format number as Japanese currency
function formatJPY(amount) {
    return new Intl.NumberFormat('ja-JP', {
        style: 'currency',
        currency: 'JPY',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Main calculation function
function calculate() {
    // Get input values
    const itemPrice = parseFloat(itemPriceInput.value) || 0;
    const shippingCost = parseFloat(shippingCostInput.value) || 0;
    const quantity = parseInt(quantityInput.value) || 1;

    // Convert to JPY
    const priceJPY = itemPrice * CURRENCY_RATE;
    const shippingJPY = shippingCost * CURRENCY_RATE;

    // Calculate total cost per unit
    const totalCostPerUnit = priceJPY + shippingJPY;
    const totalCost = totalCostPerUnit * quantity;

    // Calculate fees
    const ebayFee = totalCost * EBAY_FEE_RATE;
    const importTax = totalCost * IMPORT_TAX_RATE;
    const totalExpense = totalCost + ebayFee + importTax;

    // Calculate profit
    const profitPerUnit = totalCostPerUnit - (totalCostPerUnit * EBAY_FEE_RATE) - (totalCostPerUnit * IMPORT_TAX_RATE);
    const totalProfit = profitPerUnit * quantity;
    const profitMargin = totalCostPerUnit > 0 ? (profitPerUnit / totalCostPerUnit * 100) : 0;

    // Display results
    priceJPYDisplay.textContent = formatJPY(priceJPY);
    shippingJPYDisplay.textContent = formatJPY(shippingJPY);
    totalCostDisplay.textContent = formatJPY(totalCost);
    ebayFeeDisplay.textContent = formatJPY(ebayFee);
    importTaxDisplay.textContent = formatJPY(importTax);
    totalExpenseDisplay.textContent = formatJPY(totalExpense);
    profitPerUnitDisplay.textContent = formatJPY(profitPerUnit);
    totalProfitDisplay.textContent = formatJPY(totalProfit);
    profitMarginDisplay.textContent = profitMargin.toFixed(1) + '%';
}

// Register service worker for PWA
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js')
        .then(reg => console.log('Service Worker registered'))
        .catch(err => console.log('Service Worker registration failed'));
}

// Initial calculation
calculate();
