document.addEventListener("DOMContentLoaded", () => {
    const startDateInput = document.getElementById("start-date");
    const investmentInput = document.getElementById("investment-amount");
    const calculateButton = document.getElementById("calculate-button");
    const profitResult = document.getElementById("profit-result");
    const chartOptions = document.querySelectorAll("input[name='chart-option']");
    const smartPickContainer = document.getElementById("smart-pick-container");
    const weightComparisonContainer = document.getElementById("weight-comparison-container");
  
  
    // 設定可選日期範圍
    const minDate = "2024-07-01";
    startDateInput.setAttribute("min", minDate); 
    startDateInput.value = minDate;// 預設值
  
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

    // 加載動畫控制
    let loadingInterval;

    const startLoadingAnimation = () => {
        let dots = 0;
        profitResult.textContent = "計算中.";
        loadingInterval = setInterval(() => {
        dots = (dots + 1) % 4; // 循環顯示 0~3 個點
        profitResult.textContent = "計算中" + ".".repeat(dots);
        }, 500); // 每 500ms 更新一次
    };

    const stopLoadingAnimation = () => {
        clearInterval(loadingInterval); // 停止動畫
    };

    // 確定按鈕事件監聽器
    if (calculateButton) {
    calculateButton.addEventListener("click", () => {
      const selectedDate = startDateInput.value;
      const investmentAmount = parseFloat(investmentInput.value);

      // 檢查是否完整填寫
      if (!selectedDate || isNaN(investmentAmount)) {
        profitResult.textContent = "請完整填寫日期與金額！";
        profitResult.classList.add("error"); // 新增錯誤樣式
        return;
      }

      // 檢查金額是否小於 10,000
      if (investmentAmount < 10000) {
        profitResult.textContent = "投資金額不可小於 10,000！";
        profitResult.classList.add("error"); // 新增錯誤樣式
        return;
      }

      // 開始加載動畫
      profitResult.classList.remove("error"); // 移除錯誤樣式
      startLoadingAnimation();

      // 發送 POST 請求至後端 API
      fetch("/api/portfolio-profit-loss/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          start_date: selectedDate,
          investment_amount: investmentAmount,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("API 回應失敗");
          }
          return response.json();
        })
        .then((data) => {
          // 停止加載動畫
          stopLoadingAnimation();

          // 顯示回傳的盈虧數據
          if (data.profit_loss !== undefined) {
            profitResult.textContent = `預估損益：${data.profit_loss.toFixed(0)} 元`;
            profitResult.classList.remove("error"); // 移除錯誤樣式
          } else {
            profitResult.textContent = "後端未返回預期結果";
            profitResult.classList.add("error"); // 新增錯誤樣式
          }
        })
        .catch((error) => {
          // 停止加載動畫
          stopLoadingAnimation();

          // 處理錯誤
          profitResult.textContent = `發生錯誤：${error.message}`;
          profitResult.classList.add("error"); // 新增錯誤樣式
        });
    });
  }
});