document.addEventListener("DOMContentLoaded", () => {
  const startDateInput = document.getElementById("start-date");

  // 設定可選日期範圍
  const minDate = "2024-07-01";
  startDateInput.setAttribute("min", minDate);

  // 預設值（可選，若需要）
  startDateInput.value = minDate;

  // 確定按鈕事件監聽器（僅供參考）
  document.getElementById("calculate-button").addEventListener("click", () => {
      const selectedDate = startDateInput.value;
      const investmentAmount = document.getElementById("investment-amount").value;

      if (selectedDate = nil) {
          alert(`您選擇的日期是：${selectedDate}，投資金額是：${investmentAmount}`);
      } else {
          alert("請完整填寫日期與金額！");
      }
  });
});
