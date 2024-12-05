document.addEventListener('DOMContentLoaded', function () {
  // 創建工具提示元素
  const tooltip = document.createElement('div');
  tooltip.style.position = 'absolute';
  tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
  tooltip.style.color = '#fff';
  tooltip.style.padding = '5px 10px';
  tooltip.style.borderRadius = '4px';
  tooltip.style.pointerEvents = 'none';
  tooltip.style.opacity = '0'; // 初始透明
  tooltip.style.transition = 'opacity 0.2s ease';
  tooltip.style.zIndex = '10000';
  document.body.appendChild(tooltip);

  // 為所有的 `info-icon` 綁定事件
  document.querySelectorAll('.info-icon').forEach(function (icon) {
      icon.addEventListener('mouseenter', function (event) {
          const tooltipText = event.target.getAttribute('data-tooltip'); // 獲取自定義屬性內容
          if (tooltipText) {
              tooltip.textContent = tooltipText;
              tooltip.style.display = 'block';
              tooltip.style.opacity = '1'; // 顯示提示框
          }
      });

      icon.addEventListener('mousemove', function (event) {
          tooltip.style.left = event.pageX + 10 + 'px';
          tooltip.style.top = event.pageY + 10 + 'px';
      });

      icon.addEventListener('mouseleave', function () {
          tooltip.style.display = 'none';
          tooltip.style.opacity = '0'; // 隱藏提示框
      });
  });
});


document.addEventListener('DOMContentLoaded', function () {
  // 初始化 Flatpickr 日期選擇器
  flatpickr(".datepicker", {
    defaultDate: "2024/09/30", // 預設日期
    minDate: "2024/07/01", // 最小日期
    maxDate: "2024/09/30", // 最大日期
    dateFormat: "Y/m/d", // 日期格式
    onChange: function (selectedDates, dateStr) {
      console.log(`選擇的日期為：${dateStr}`);
      updateDateRange(dateStr);
    }
  });

  // 點擊下拉圖標觸發日期選擇器
  const dropdownIcon = document.querySelector('.dropdown-icon');
  dropdownIcon.addEventListener('click', function() {
    const dateInput = document.querySelector('.datepicker');
    dateInput.focus(); // 使日期框獲得焦點，觸發下拉日曆
  });
});

// 更新日期範圍的函數
function updateDateRange(endDate) {
  const startDate = "2024/07/01"; // 固定開始日期
  console.log(`日期範圍：${startDate} ~ ${endDate}`);
  // 在這裡可以觸發更新報酬率的邏輯
}

