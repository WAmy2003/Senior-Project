// 初始化日期選擇器
function initializeDateSelector() {
    const dateSelect = document.getElementById('dateSelect');

    // 從API獲取日期數據
    fetch('/api/get_available_dates/')
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
    // fetch(`/api/get_available_data/${date}?stock_ids=2912,2330`)
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error(`HTTP error! status: ${response.status}`);
    //         }
    //         return response.json();
    //     })
    //     .then(result => {
    //         if (result.status === 'success') {
    //             const portfolioTable = document.getElementById('portfolioTable');
    //             const rows = portfolioTable.getElementsByTagName('tr');

    //             Array.from(rows).forEach(row => {
    //                 const stockId = row.cells[1]?.textContent; // 股票代號
    //                 const returnRateCell = row.cells[3]; // 報酬率

    //                 if (stockId && returnRateCell) {
    //                     const returnRate = result.data[stockId];
    //                     returnRateCell.textContent = returnRate !== undefined ? `${returnRate}%` : `-`;
    //                 }
    //             });
    //         } else {
    //             console.error('API returned an error:', result.message);
    //         }
    //     })
    //     .catch(error => console.error('Error updating return rates:', error));
}


// 在頁面加載時初始化
document.addEventListener('DOMContentLoaded', function () {
    initializeDateSelector();
});