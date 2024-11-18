function fetchStockDataForTable(stockId) {
    console.log('表開始獲取股票數據:', stockId);
    const apiUrl = `http://localhost:8000/api/stock-data/?stock_id=${stockId}`;

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(response => {
            console.log('收到的數據:', response);

            if (!response || !response.data || !Array.isArray(response.data.data)) {
                throw new Error('無效的數據格式');
            }

            const stockData = response.data.data;

            if (stockData && stockData.length > 0) {
                const earliestData = stockData[0];

                if (!earliestData.high || !earliestData.low || !earliestData.open ||
                    !earliestData.close || !earliestData.volume) {
                    throw new Error('數據缺少必要欄位');
                }

                updateTableRow(stockId, earliestData);
            } else {
                throw new Error('無股票數據');
            }
        })
        .catch(error => handleFetchError(stockId, error));
}

function updateTableRow(stockId, data) {
    const row = document.getElementById(`stock-row-${stockId}`);
    if (!row) {
        throw new Error(`找不到股票 ${stockId} 的表格行`);
    }

    const cells = row.cells;

    // 格式化數據並更新
    cells[7].textContent = parseFloat(data.high).toFixed(2);   // 最高
    cells[8].textContent = parseFloat(data.low).toFixed(2);    // 最低
    cells[4].textContent = parseFloat(data.open).toFixed(2);   // 開盤價
    cells[5].textContent = parseFloat(data.close).toFixed(2);  // 收盤價
    cells[6].textContent = parseFloat(data.change).toFixed(2);   // 漲跌
    cells[9].textContent = parseInt(data.volume).toLocaleString(); // 總成交量

    // 設定漲跌顏色
    const change = parseFloat(data.change);
    cells[6].style.color = change > 0 ? '#FF3B30' : change < 0 ? '#4CD964' : '';
}

function handleFetchError(stockId, error) {
    console.error(`股票 ${stockId} 數據獲取錯誤:`, error);
    const row = document.getElementById(`stock-row-${stockId}`);
    if (row) {
        const cells = row.cells;
        [3, 4, 6, 7, 10].forEach(index => {
            cells[index].textContent = '—';
            cells[index].style.color = '';
        });
    }
}