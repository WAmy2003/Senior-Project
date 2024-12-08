document.addEventListener("DOMContentLoaded", () => {
  const investmentInput = document.getElementById("investment-amount");
  const calculateButton = document.getElementById("calculate-button");
  const profitResult = document.getElementById("profit-result");
  const chartOptions = document.querySelectorAll("input[name='chart-option']");
  const chartSmartPick = document.getElementById("chart-smart-pick-canvas");
  const chart0050 = document.getElementById("chart-0050-canvas");

  // 初始化空圖表
  const initializeCharts = () => {
      chartSmartPick.getContext("2d").clearRect(0, 0, chartSmartPick.width, chartSmartPick.height);
      chart0050.getContext("2d").clearRect(0, 0, chart0050.width, chart0050.height);
  };

  // 更新圖表
  const updateCharts = (option) => {
      initializeCharts();
      if (option === "return") {
          chartSmartPick.getContext("2d").fillText("折線圖 (Smart Pick)", 50, 50);
          chart0050.getContext("2d").fillText("折線圖 (0050)", 50, 50);
      } else if (option === "weight") {
          chartSmartPick.getContext("2d").fillText("餅圖 (Smart Pick)", 50, 50);
          chart0050.getContext("2d").fillText("餅圖 (0050)", 50, 50);
      }
  };

  // 初始狀態顯示折線圖
  updateCharts("return");

  // 切換圖表顯示
  chartOptions.forEach(option => {
      option.addEventListener("change", (event) => {
          updateCharts(event.target.value);
      });
  });

  // 計算盈虧
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
});
