let smartPickChartInstance = null;
let chart0050Instance = null;

document.addEventListener("DOMContentLoaded", () => {
  const smartPickChartCanvas = document.getElementById("chart-smart-pick");
  const chart0050Canvas = document.getElementById("chart-0050");

  if (smartPickChartCanvas && chart0050Canvas) {
    const ctxSmartPick = smartPickChartCanvas.getContext("2d");
    const ctx0050 = chart0050Canvas.getContext("2d");

    // 銷毀舊的 Smart Pick 圓餅圖實例
    if (smartPickChartInstance) {
      smartPickChartInstance.destroy();
    }

    smartPickChartInstance = new Chart(ctxSmartPick, {
      type: "pie",
      data: {
        labels: ['A', 'B', 'C'],
        datasets: [{
          data: [10, 20, 30],
          backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56'],
        }]
      },
      options: {
        responsive: true, // 啟用響應式
        maintainAspectRatio: true,
        plugins: {
          legend: { display: false } // 隱藏圖例
        },
      }
    });

    // 銷毀舊的 0050 圓餅圖實例
    if (chart0050Instance) {
      chart0050Instance.destroy();
    }

    chart0050Instance = new Chart(ctx0050, {
      type: "pie",
      data: {
        labels: ['X', 'Y', 'Z'],
        datasets: [{
          data: [15, 25, 35],
          backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56'],
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { display: false } 
        },
      }
    });
  } else {
    console.error("Canvas elements not found!");
  }
});
