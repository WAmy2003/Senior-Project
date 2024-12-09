// 儲存圖表實例變數
let smartPickChartInstance = null;
let chart0050Instance = null;

// 初始化 Smart Pick 圓餅圖
function initializeSmartPickChart() {
  const ctxSmartPick = document.getElementById("chart-smart-pick").getContext("2d");

  // 如果已有舊圖表實例，先銷毀
  if (smartPickChartInstance) {
    smartPickChartInstance.destroy();
  }

  // 創建新圖表
  smartPickChartInstance = new Chart(ctxSmartPick, {
    type: "pie",
    data: {
      labels: ["A", "B", "C"],
      datasets: [
        {
          data: [50, 30, 20],
          backgroundColor: ["#ff9999", "#66b3ff", "#99ff99"],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "top" },
      },
    },
  });
}

// 初始化 0050 圓餅圖
function initialize0050Chart() {
  const ctx0050 = document.getElementById("chart-0050").getContext("2d");

  // 如果已有舊圖表實例，先銷毀
  if (chart0050Instance) {
    chart0050Instance.destroy();
  }

  // 創建新圖表
  chart0050Instance = new Chart(ctx0050, {
    type: "pie",
    data: {
      labels: ["X", "Y", "Z"],
      datasets: [
        {
          data: [40, 40, 20],
          backgroundColor: ["#ff9999", "#66b3ff", "#99ff99"],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "top" },
      },
    },
  });
}

