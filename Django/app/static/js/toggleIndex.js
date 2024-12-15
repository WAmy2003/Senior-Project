document.addEventListener("DOMContentLoaded", function () {
  const btnSmartPick = document.getElementById("btn-smartpick");
  const btn0050 = document.getElementById("btn-0050");
  const returnRate = document.getElementById("return-rate");
  const volatilityRate = document.getElementById("volatility-rate");
  const sharpeRatio = document.getElementById("sharpe-ratio");

  // 定義績效指標數據
  const data = {
      smartPick: {
          returnRate: "4.47%",
          volatilityRate: "0.26",
          sharpeRatio: "0.11",
      },
      _0050: {
          returnRate: "2.90%",
          volatilityRate: "0.36",
          sharpeRatio: "0.03",
      },
  };

  // 按鈕點擊事件處理
  btnSmartPick.addEventListener("click", () => {
      updatePerformance("smartPick");
      toggleActiveButton(btnSmartPick, btn0050);
  });

  btn0050.addEventListener("click", () => {
      updatePerformance("_0050");
      toggleActiveButton(btn0050, btnSmartPick);
  });

  // 更新績效指標
  function updatePerformance(type) {
      returnRate.textContent = data[type].returnRate;
      volatilityRate.textContent = data[type].volatilityRate;
      sharpeRatio.textContent = data[type].sharpeRatio;
  }

  // 切換按鈕樣式
  function toggleActiveButton(active, inactive) {
      active.classList.add("active");
      inactive.classList.remove("active");
  }

  // 預設載入 Smart Pick 數據
  updatePerformance("smartPick");
}); 