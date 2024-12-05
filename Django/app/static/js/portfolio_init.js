// 全局變數
let stock_ids = [];
let company_names = [];
let weights = [];

// 自訂提示框
const tooltip = document.createElement('div');
tooltip.classList.add('tooltip');
document.body.appendChild(tooltip);

// 從後端獲取資料並初始化表格
async function initializePortfolio() {
    try {
        const response = await fetch('http://localhost:8000/api/portfolio-weights/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.status === 'success') {
            // 更新全局變數
            stock_ids = data.data.stock_ids;
            company_names = data.data.company_names;
            weights = data.data.weights;

            // 初始化表格
            populateTable();
        } else {
            throw new Error('Failed to fetch portfolio data');
        }
    } catch (error) {
        console.error('Error initializing portfolio:', error);
        const tableBody = document.getElementById('portfolioTable');
        tableBody.innerHTML = `
            <tr>
                <td colspan="11" style="text-align: center; color: red;">
                    載入投資組合資料失敗，請重新整理頁面或聯繫系統管理員
                </td>
            </tr>
        `;
    }
}

function populateTable() {
    const tableBody = document.getElementById('portfolioTable');
    let rows = '';

    for (let i = 0; i < stock_ids.length; i++) {
        weights[i] = (weights[i] * 100).toFixed(2) + '%';
        rows += `
            <tr id="stock-row-${stock_ids[i]}" onclick="showStockInfo('${stock_ids[i]}', '${company_names[i]}')">
                <td onmouseover="showTooltip(event, '公司名稱')" onmouseout="hideTooltip()"> ${company_names[i]}</td>
                <td onmouseover="showTooltip(event, '股票代號')" onmouseout="hideTooltip()"> ${stock_ids[i]}</td>
                <td onmouseover="showTooltip(event, '權重')" onmouseout="hideTooltip()"> ${weights[i]}</td>
                <td onmouseover="showTooltip(event, '個股報酬率')" onmouseout="hideTooltip()"> — </td>
                <td onmouseover="showTooltip(event, '開盤價')" onmouseout="hideTooltip()"> — </td>
                <td onmouseover="showTooltip(event, '收盤價')" onmouseout="hideTooltip()"> — </td>
                <td onmouseover="showTooltip(event, '漲跌')" onmouseout="hideTooltip()"> — </td>
                <td onmouseover="showTooltip(event, '最高')" onmouseout="hideTooltip()"> — </td>
                <td onmouseover="showTooltip(event, '最低')" onmouseout="hideTooltip()"> — </td>
                <td onmouseover="showTooltip(event, '總成交量')" onmouseout="hideTooltip()"> — </td>
            </tr>
        `;
    }
    tableBody.innerHTML = rows;

    // 為每個股票獲取數據
    stock_ids.forEach(stockId => {
        fetchStockDataForTable(stockId);
    });
}

function showTooltip(event, text) {
    tooltip.style.opacity = '1'; // 顯示提示框
    tooltip.textContent = text;
    tooltip.style.left = `${event.pageX + 10}px`; // 右側顯示
    tooltip.style.top = `${event.pageY + 10}px`; // 上方顯示
}

function hideTooltip() {
    tooltip.style.opacity = '0'; // 隱藏提示框
}
