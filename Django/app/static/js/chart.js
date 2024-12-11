function showStockInfo(stockId, companyName) {
    document.getElementById('modalTitle').textContent = companyName;
    $('#stockModal').fadeIn();
    fetchStockData(stockId);
}

function fetchStockData(stockId) {
    console.log('開始獲取股票數據:', stockId);
    document.getElementById('stockPrice').textContent = '資料載入中...';

    const apiUrl = `http://localhost:8000/api/stock-data/?stock_id=${stockId}`;
    console.log('請求 URL:', apiUrl);

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(response => {
            console.log('收到的數據:', response);
            const stockData = response.data.data;

            if (stockData.length > 0) {
                const chartData = prepareChartData(stockData);
                updateChart(chartData, stockId);
                updatePriceDisplay(stockData[stockData.length - 1]);
            } else {
                throw new Error('無效的數據格式或空數據');
            }
        })
        .catch(error => {
            console.error('詳細錯誤資訊:', error);
            document.getElementById('stockPrice').textContent = '資料獲取錯誤，請稍後再試。';
        });
}

function prepareChartData(stockData) {
    try {
        // 反轉數據順序，確保最舊的數據在前
        const sortedData = stockData.sort((a, b) =>
            new Date(a.date) - new Date(b.date)
        );

        return sortedData.map(item => {
            // 格式化日期字符串 (YYYY-MM-DD)
            const dateStr = item.date.split('T')[0];

            return {
                time: dateStr,  // 直接使用日期字符串而不是時間戳
                open: Number(item.open),
                high: Number(item.high),
                low: Number(item.low),
                close: Number(item.close),
                volume: Number(item.volume)
            };
        });
    } catch (error) {
        console.error('數據處理錯誤:', error);
        return [];
    }
}

function updatePriceDisplay(latestData) {
    // 將 latestData.date 轉換為格式化日期
    const formattedDate = new Date(latestData.date).toISOString().split('T')[0].replace(/-/g, '/');

    // 更新數據顯示
    document.getElementById('stockPrice').innerHTML = `
        <div class="data-title">最新數據 (${formattedDate})</div>
        <div class="data-container">
            <!-- 第一行 -->
            <div class="data-row">
                <div class="data-item">
                    <div class="data-line"></div>
                    <span class="data-label">開盤：</span>
                    <span>${latestData.open}</span>
                </div>
                <div class="data-item">
                    <div class="data-line"></div>
                    <span class="data-label">收盤：</span>
                    <span>${latestData.close}</span>
                </div>
            </div>
            <!-- 第二行 -->
            <div class="data-row">
                <div class="data-item">
                    <div class="data-line"></div>
                    <span class="data-label">最高：</span>
                    <span>${latestData.high}</span>
                </div>
                <div class="data-item">
                    <div class="data-line"></div>
                    <span class="data-label">成交量：</span>
                    <span>${latestData.volume.toLocaleString()}</span>
                </div>
            </div>
            <!-- 最低獨占一行 -->
            <div class="data-item single-row">
                <div class="data-line"></div>
                <span class="data-label">最低：</span>
                <span>${latestData.low}</span>
            </div>
        </div>
    `;
}



// 修改 updateChart 函數
function updateChart(chartData, stockId) {
    try {
        console.log('開始更新圖表，數據:', chartData);

        // 清除舊圖表
        const chartElement = document.getElementById('chart');
        chartElement.innerHTML = '';

        // 建立新圖表
        const chart = LightweightCharts.createChart(chartElement, {
            width: chartElement.offsetWidth,
            height: 600,
            layout: {
                backgroundColor: '#ffffff',
                textColor: '#333',
            },
            grid: {
                vertLines: {
                    color: '#e1e1e1',
                },
                horzLines: {
                    color: '#e1e1e1',
                },
            },
            crosshair: {
                mode: LightweightCharts.CrosshairMode.Normal,
            },
            rightPriceScale: {
                borderColor: '#e1e1e1',
                scaleMargins: {
                    top: 0.1,
                    bottom: 0.3,
                },
            },
            timeScale: {
                borderColor: '#e1e1e1',
                timeVisible: true,
                secondsVisible: false,
                fixLeftEdge: true,
                fixRightEdge: true,
            },
        });

        // 過濾無效數據
        const validData = chartData.filter(item =>
            item.open != null &&
            item.high != null &&
            item.low != null &&
            item.close != null &&
            item.volume != null
        );

        if (validData.length === 0) {
            throw new Error('沒有有效的數據');
        }

        // 新增 K線圖系列
        const candlestickSeries = chart.addCandlestickSeries({
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderVisible: false,
            wickUpColor: '#26a69a',
            wickDownColor: '#ef5350'
        });

        // 新增成交量系列
        const volumeSeries = chart.addHistogramSeries({
            priceFormat: {
                type: 'volume',
            },
            priceScaleId: '',
            scaleMargins: {
                top: 0.8,
                bottom: 0,
            },
        });

        // 設置 K線數據
        candlestickSeries.setData(validData);

        // 設置成交量數據
        const volumeData = validData.map(item => ({
            time: item.time,
            value: item.volume,
            color: "rgba(202, 233, 252, 0.3)"
        }));

        volumeSeries.setData(volumeData);

        // 調整時間範圍以顯示所有數據
        chart.timeScale().fitContent();

        // 設置圖表自適應
        const resizeChart = () => {
            chart.applyOptions({
                width: chartElement.offsetWidth
            });
        };

        // 監聽窗口大小變化
        window.addEventListener('resize', resizeChart);

        // 監聽 modal 顯示事件
        const modal = document.getElementById('stockModal');
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' &&
                    mutation.attributeName === 'style' &&
                    modal.style.display === 'block') {
                    resizeChart();
                }
            });
        });

        observer.observe(modal, { attributes: true });

        // 保存圖表實例以便後續清理
        window.stockChart = {
            chart: chart,
            observer: observer,
            resizeListener: resizeChart
        };

    } catch (error) {
        console.error('圖表更新錯誤:', error);
        const chartElement = document.getElementById('chart');
        chartElement.innerHTML = `<div style="text-align: center; padding: 20px;">圖表載入失敗: ${error.message}</div>`;
    }
}

// 修改關閉按鈕事件處理
document.querySelector('.close').onclick = function () {
    if (window.stockChart) {
        // 移除事件監聽器
        window.removeEventListener('resize', window.stockChart.resizeListener);
        // 停止觀察
        window.stockChart.observer.disconnect();
        // 銷毀圖表
        window.stockChart.chart.remove();
        window.stockChart = null;
    }
    $('#stockModal').fadeOut();
};