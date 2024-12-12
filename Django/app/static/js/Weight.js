let smartPickChartInstance = null;
let chart0050Instance = null;

document.addEventListener("DOMContentLoaded", () => {
  const smartPickChartCanvas = document.getElementById("chart-smart-pick");
  const chart0050Canvas = document.getElementById("chart-0050");

  if (smartPickChartCanvas && chart0050Canvas) {
    const ctxSmartPick = smartPickChartCanvas.getContext("2d");
    const ctx0050 = chart0050Canvas.getContext("2d");

    // 從後端獲取 Smart Pick 圓餅圖數據
    fetch('/api/smartpick-weights/')
      .then(response => response.json())
      .then(data => {
        // 銷毀舊的 Smart Pick 圓餅圖實例
        if (smartPickChartInstance) {
          smartPickChartInstance.destroy();
        }

        if (data && data.length > 0) {
          const labels = data.map(item => item.stock_name);
          const weights = data.map(item => item.weights);
          const colors = generateGradientColors("#FC6D26", weights.length); // 顏色梯度

          // 創建新圖表
          smartPickChartInstance = new Chart(ctxSmartPick, {
            type: "doughnut",
            data: {
              labels: labels,
              datasets: [{
                data: weights,
                backgroundColor: colors,
              }],
            },
            options: {
              responsive: true,
              maintainAspectRatio: true,
              plugins: {
                legend: { display: false},
                tooltip: {
                  enabled: false, // 禁用默認提示框
                  external: (context) => renderCustomTooltip(context), // 使用自定義提示框邏輯
                },
              },
            },
          });
        } else {
          console.error("No data available for Smart Pick chart");
        }
      })
      .catch(error => {
        console.error('Error loading Smart Pick data:', error);
      });

    // 從後端獲取 0050 圓餅圖數據
    fetch('/api/0050-weights/')
      .then(response => response.json())
      .then(data => {
        // 銷毀舊的 0050 圓餅圖實例
        if (chart0050Instance) {
          chart0050Instance.destroy();
        }

        if (data && data.length > 0) {
          const labels = data.map(item => item.stock_name);
          const weights = data.map(item => item.weights);
          const colors = generateGradientColors("#bad3e3", weights.length); // 顏色梯度

          // 創建新圖表
          chart0050Instance = new Chart(ctx0050, {
            type: "doughnut",
            data: {
              labels: labels,
              datasets: [{
                data: weights,
                backgroundColor: colors,
              }],
            },
            options: {
              responsive: true,
              maintainAspectRatio: true,
              plugins: {
                legend: { display: false },
                tooltip: {
                  enabled: false, // 禁用默認提示框
                  external: (context) => renderCustomTooltip(context), // 使用自定義提示框邏輯
                },
              },
            },
          });
        } else {
          console.error("No data available for 0050 chart");
        }
      })
      .catch(error => {
        console.error('Error loading 0050 data:', error);
      });
  } else {
    console.error("Canvas elements not found.");
  }
});

// 生成顏色梯度
function generateGradientColors(baseColor, count) {
  const colors = [];
  for (let i = 0; i < count; i++) {
    const alpha = 1 - (i / count) * 0.7; // 顏色透明度從 1 遞減到 0.3
    const alphaHex = Math.round(alpha * 255).toString(16).padStart(2, '0');
    colors.push(`${baseColor}${alphaHex}`);
  }
  return colors;
}

// 自定義提示框邏輯
function renderCustomTooltip(context) {
  const tooltipModel = context.tooltip;
  const chart = context.chart;

  // 如果沒有提示框數據，則返回
  if (!tooltipModel || !tooltipModel.dataPoints) return;

  // 獲取提示框的數據
  const dataPoint = tooltipModel.dataPoints[0];
  const value = dataPoint.raw;
  const label = dataPoint.label;

  // 獲取甜甜圈中心點位置
  const { width, height } = chart;
  const centerX = width / 2;
  const centerY = height / 2;

  // 在中心顯示提示框數據
  let tooltipEl = document.getElementById('custom-tooltip');
  if (!tooltipEl) {
    tooltipEl = document.createElement('div');
    tooltipEl.id = 'custom-tooltip';
    tooltipEl.style.position = 'absolute';
    tooltipEl.style.pointerEvents = 'none';
    tooltipEl.style.textAlign = 'center';
    tooltipEl.style.color = '#000000';
    tooltipEl.style.fontSize = '16px';
    tooltipEl.style.fontWeight = 'bold';
    tooltipEl.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
    tooltipEl.style.borderRadius = '5px';
    tooltipEl.style.padding = '5px';
    document.body.appendChild(tooltipEl);
  }

  // 更新內容和位置
  tooltipEl.innerHTML = `<div>${label}<br>${(value * 100).toFixed(2)}%</div>`;
  const tooltipRect = tooltipEl.getBoundingClientRect();
  tooltipEl.style.left = `${chart.canvas.offsetLeft + centerX - tooltipRect.width / 2}px`;
  tooltipEl.style.top = `${chart.canvas.offsetTop + centerY - tooltipRect.height / 2}px`;
}
