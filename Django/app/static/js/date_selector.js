// 初始化日期選擇器
function initializeDateSelector() {
    const dateSelect = document.getElementById('dateSelect');

    // 從API獲取日期數據
    fetch('http://localhost:8000/api/get_available_dates/')
        .then(response => response.json())
        .then(result => {
            if (result.status === 'success') {
                const dates = result.data;

                // 填充日期選項
                dates.forEach(date => {
                    const option = document.createElement('option');
                    option.value = date;
                    option.textContent = formatDate(date);
                    dateSelect.appendChild(option);
                });

                // 設置最新日期為默認選項
                if (dates.length > 0) {
                    dateSelect.value = dates[0];
                    // 初始化時載入第一個日期的數據
                    updateReturnRates(dates[0]);
                }
            }
        })
        .catch(error => console.error('Error fetching dates:', error));

    // 添加變更事件監聽器
    dateSelect.addEventListener('change', function (e) {
        const selectedDate = e.target.value;
        updateReturnRates(selectedDate);
    });
}

// 格式化日期顯示
function formatDate(dateString) {
    const date = new Date(dateString);
    return `${date.getFullYear()}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}`;
}

// 根據選擇的日期更新表格
function updateReturnRates(date) {
    // 從 portfolio-weights API 取得股票代號
    fetch('http://localhost:8000/api/portfolio-weights/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const stockIds = data.data.stock_ids;

                // 使用取得的 stock_ids 來呼叫 get_available_data API
                const queryString = stockIds.join(',');
                return fetch(`http://localhost:8000/api/get_available_data/${date}?stock_ids=${queryString}`);
            } else {
                throw new Error('Failed to fetch portfolio weights');
            }
        })
        .then(response => response.json())
        .then(result => {
            if (result.status === 'success') {
                // 更新每一列的報酬率
                const portfolioTable = document.getElementById('portfolioTable');
                const rows = portfolioTable.getElementsByTagName('tr');

                for (let row of rows) {
                    const stockId = row.cells[1]?.textContent.trim();
                    const returnRate = result.data[stockId];
                    if (returnRate == null) {
                        row.cells[3].textContent = `${returnRate}`;
                    }
                    else {
                        const formattedRate = (Number(returnRate.toFixed(4)) * 100).toFixed(2);
                        row.cells[3].textContent = `${formattedRate}%`;

                        // 根據報酬率的正負值設置顏色
                        row.cells[3].style.color = returnRate > 0 ? '#FF3B30' : returnRate < 0 ? '#4CD964' : '';
                    }
                }
            } else {
                console.error('Failed to update return rates:', result.message);
            }
        })
        .catch(error => console.error('Error updating return rates:', error));
}



// 在頁面加載時初始化
document.addEventListener('DOMContentLoaded', function () {
    initializeDateSelector();
});