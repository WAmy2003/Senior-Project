// 模擬的假數據，這將顯示在圖表中
const fakeData = {
  labels: ['2024-12-01', '2024-12-02', '2024-12-03', '2024-12-04', '2024-12-05'],  // 假設的日期數據
  data: [12, 15, 10, 17, 25]  // 假設的報酬率數據
};

// 渲染折線圖的函數
function renderLineChart(data) {
  const ctx = document.getElementById('lineChart').getContext('2d');

  // 使用 Chart.js 來創建折線圖
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels,  // X軸的日期
      datasets: [{
        label: '每日報酬率',
        data: data.data,  // Y軸的報酬率數據
        borderColor: 'rgba(75, 192, 192, 1)', // 折線顏色
        borderWidth: 2,
        fill: false,  // 不填充顏色
        tension: 0.1  // 控制折線的彎曲度
      }]
    },
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
window.onload = function() {
  renderLineChart(fakeData);
};
