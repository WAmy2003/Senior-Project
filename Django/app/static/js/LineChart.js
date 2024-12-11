async function fetchAndRenderChart() {
  try {
    // 從後端 API 獲取數據
    const response = await fetch('/api/chart-data/');
    const chartData = await response.json();

    // 格式化數據
    const data = {
      labels: chartData.labels,  // X軸的日期
      datasets: [
        {
          label: '0050 報酬率',
          data: chartData.return_0050,  // Y軸的 0050 報酬率
          borderColor: 'rgba(206, 202, 198, 1)', // 折線顏色
          borderWidth: 2,
          fill: false,
          pointStyle: 'circle',  // 點的形狀，這裡是圓形
          pointRadius: 2,         // 點的大小
          pointBackgroundColor: 'rgba(206, 202, 198, 1)' // 點的顏色
        },
        {
          label: '加權指數 報酬率',
          data: chartData.return_0000,  // Y軸的 0000 報酬率
          borderColor: 'rgba(100, 96, 101, 1)', // 折線顏色
          borderWidth: 2,
          fill: false,
          pointStyle: 'circle',  // 點的形狀，這裡是圓形
          pointRadius: 2,         // 點的大小
          pointBackgroundColor: 'rgba(100, 96, 101, 1)' // 點的顏色
        },
        {
          label: 'Smart Pick 報酬率',
          data: chartData.smart_pick,  // Y軸的 Smart Pick 報酬率
          borderColor: 'rgba(252, 109, 38, 1)', // 折線顏色
          borderWidth: 2,
          fill: false,
          pointStyle: 'circle',  // 點的形狀，這裡是圓形
          pointRadius: 2,         // 點的大小
          pointBackgroundColor: 'rgba(252, 109, 38, 1)' // 點的顏色
        }
      ]
    };

    renderLineChart(data);  // 渲染圖表
  } catch (error) {
    console.error('Error fetching chart data:', error);
  }
}

// 渲染折線圖的函數
function renderLineChart(data) {
  const ctx = document.getElementById('lineChart').getContext('2d');

  // 使用 Chart.js 來創建折線圖
  new Chart(ctx, {
    type: 'line',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: '日期'
          }
        },
        y: {
          title: {
            display: true,
            text: '報酬率'
          }
        }
      }
    }
  });
}

// 假設在頁面加載時自動加載數據
window.onload = fetchAndRenderChart;
