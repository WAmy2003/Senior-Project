// script.js

document.addEventListener('DOMContentLoaded', function() {
    // 獲取結束日期選擇框
    const endDateSelect = document.getElementById('end-date');
    const stockReturnRateDiv = document.getElementById('stock-return-rate');
    const infoIcon = document.getElementById('info-icon');
    const infoBox = document.getElementById('info-box');
    
    // 計算並顯示個股報酬率
    function updateStockReturnRate(startDate, endDate) {
      // 這裡你可以加入實際的計算邏輯，這邊只是示範
      stockReturnRateDiv.innerText = `${startDate} ~ ${endDate} 的個股報酬率：5%`;
    }
  
    // 當結束日期變更時，更新報酬率
    endDateSelect.addEventListener('change', function() {
      const selectedEndDate = endDateSelect.value;
      updateStockReturnRate('2024/07/01', selectedEndDate);
    });
  
    // 頁面加載時，設置初始顯示
    updateStockReturnRate('2024/07/01', '2024/09/30');
    
    // 顯示提示框
    infoIcon.addEventListener('mouseover', function() {
      infoBox.style.display = 'block';
      const rect = infoIcon.getBoundingClientRect();
      infoBox.style.top = `${rect.top + window.scrollY + 20}px`;
      infoBox.style.left = `${rect.left + window.scrollX + 10}px`;
    });
  
    // 鼠標移出時隱藏提示框
    infoIcon.addEventListener('mouseout', function() {
      infoBox.style.display = 'none';
    });
  });
  