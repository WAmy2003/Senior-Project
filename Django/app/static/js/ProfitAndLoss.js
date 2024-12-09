document.addEventListener("DOMContentLoaded", () => {
  const investmentInput = document.getElementById("investment-amount");
  const calculateButton = document.getElementById("calculate-button");
  const profitResult = document.getElementById("profit-result");
  const chartOptions = document.querySelectorAll("input[name='chart-option']");
  const smartPickContainer = document.getElementById("smart-pick-container");
  const weightComparisonContainer = document.getElementById("weight-comparison-container");

  // 根據選擇切換內容
  const showContent = (option) => {
    if (option === "return") {
      smartPickContainer.style.display = "block";
      weightComparisonContainer.style.display = "none";
    } else if (option === "weight") {
      smartPickContainer.style.display = "none";
      weightComparisonContainer.style.display = "flex";
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
