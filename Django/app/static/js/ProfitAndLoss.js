document.addEventListener("DOMContentLoaded", () => {
  const investmentInput = document.getElementById("investment-amount");
  const calculateButton = document.getElementById("calculate-button");
  const profitResult = document.getElementById("profit-result");
  const chartOptions = document.querySelectorAll("input[name='chart-option']");
  const chartSmartPick = document.getElementById("chart-smart-pick-canvas");
  const chart0050 = document.getElementById("chart-0050-canvas");
  const smartPickContainer = document.getElementById("smart-pick-container");
  const weightComparisonContainer = document.getElementById("weight-comparison-container");

  // 根據選擇切換內容
  const showContent = (option) => {
    if (option === "return") {
      smartPickContainer.style.display = "block";
      weightComparisonContainer.style.display = "none";
    } else if (option === "weight") {
      smartPickContainer.style.display = "none";
      weightComparisonContainer.style.display = "block";
    }
  };

  // 初始顯示 "每日報酬率" 頁面
  showContent("return");

  // 監聽按鈕切換
  chartOptions.forEach(option => {
    option.addEventListener("change", (event) => {
      showContent(event.target.value);
    });
  });

  // 這裡可以初始化圓餅圖或其他圖表
  // 更新圖表
  const updateCharts = () => {
    const smartPickChart = document.getElementById("chart-smart-pick");
    const chart0050 = document.getElementById("chart-0050");

    if (smartPickChart) {
      const ctxSmartPick = smartPickChart.getContext("2d");
      // 這裡初始化 Smart Pick 圓餅圖
      new Chart(ctxSmartPick, {
        type: "pie",
        data: {
          labels: ['A', 'B', 'C'],
          datasets: [{
            data: [10, 20, 30],
            backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56'],
          }]
        }
      });
    }

    if (chart0050) {
      const ctx0050 = chart0050.getContext("2d");
      // 這裡初始化 0050 圓餅圖
      new Chart(ctx0050, {
        type: "pie",
        data: {
          labels: ['X', 'Y', 'Z'],
          datasets: [{
            data: [15, 25, 35],
            backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56'],
          }]
        }
      });
    }
  };

  // 計算盈虧
  if (calculateButton) {
    calculateButton.addEventListener("click", () => {
      const amount = parseFloat(investmentInput.value);
      if (!isNaN(amount) && amount >= 0) {
        profitResult.textContent = `盈虧結果：${amount} (暫代，公式待更新)`;
        profitResult.classList.remove("error"); // 移除錯誤樣式
      } else {
        profitResult.textContent = "請輸入有效的金額";
        profitResult.classList.add("error"); // 新增錯誤樣式
      }
    });
  }
});
