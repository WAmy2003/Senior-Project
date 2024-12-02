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

            if (stockData && stockData.length > 0) {
                const chartData = prepareChartData(stockData);
                updateChart(chartData.ohlc, chartData.volume, stockId);
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
    const ohlc = stockData.map(item => ({
        x: new Date(item.date).getTime(),
        o: parseFloat(item.open),
        h: parseFloat(item.high),
        l: parseFloat(item.low),
        c: parseFloat(item.close)
    }));

    const volume = stockData.map(item => ({
        x: new Date(item.date),
        y: parseFloat(item.volume)
    }));

    return { ohlc, volume };
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
function updateChart(ohlcData, volumeData, stockId) {
    console.log('開始更新圖表，數據:', { ohlcData, volumeData });
    const ctx = document.getElementById('chartContainer').getContext('2d');

    // 如果已經存在圖表，先銷毀
    if (window.stockChart) {
        window.stockChart.destroy();
    }

    const filteredData = ohlcData.filter(d =>
        d.o !== null && d.h !== null && d.l !== null && d.c !== null
    );

    // 設定K線圖樣式
    const candlestickElement = {
        id: 'candlestick',
        beforeDatasetsDraw(chart, args, options) {
            const { ctx, data, scales: { x, y } } = chart;
            const candleWidth = 5;
            const wickWidth = 1;

            ctx.strokeStyle = 'rgba(0, 0, 0, 0.5)';
            ctx.lineWidth = wickWidth;

            data.datasets[0].data.forEach((point, i) => {
                if (point.o !== undefined) {
                    const open = y.getPixelForValue(point.o);
                    const high = y.getPixelForValue(point.h);
                    const low = y.getPixelForValue(point.l);
                    const close = y.getPixelForValue(point.c);
                    const x0 = x.getPixelForValue(point.x) - candleWidth / 2;

                    // 設置顏色（紅色或綠色）
                    const isBullish = close < open;
                    ctx.fillStyle = isBullish ? '#4CD964' : '#FF3B30';
                    ctx.strokeStyle = isBullish ? '#4CD964' : '#FF3B30';
                    ctx.lineWidth = wickWidth;

                    // 畫影線
                    ctx.beginPath();
                    ctx.moveTo(x0 + candleWidth / 2, high);
                    ctx.lineTo(x0 + candleWidth / 2, low);
                    ctx.stroke();

                    // 畫實體部分
                    ctx.fillRect(x0, Math.min(open, close), candleWidth, Math.abs(close - open));
                }
            });
        }
    };

    // 創建新圖表
    window.stockChart = new Chart(ctx, {
        type: 'candlestick',
        data: {
            datasets: [{
                label: '股價',
                data: filteredData.map(d => ({
                    x: d.x,
                    o: d.o,
                    h: d.h,
                    l: d.l,
                    c: d.c
                }))
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 20,
                    right: 20
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        displayFormats: {
                            day: 'yyyy/MM/dd'
                        }
                    },
                    distribution: 'linear',
                    ticks: {
                        source: 'data',
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 10  // 限制X軸標籤數量
                    },
                    grid: {
                        display: true,
                        drawOnChartArea: true
                    }
                },
                y: {
                    position: 'right',
                    grid: {
                        display: true,
                        drawOnChartArea: true
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: `${stockId} 股價走勢圖`
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const point = context.raw;
                            return [
                                `開盤: ${point.o}`,
                                `最高: ${point.h}`,
                                `最低: ${point.l}`,
                                `收盤: ${point.c}`
                            ];
                        }
                    }
                }
            }
        },
        plugins: [candlestickElement]
    });
}
document.querySelector('.close').onclick = function () {
    $('#stockModal').fadeOut();
};