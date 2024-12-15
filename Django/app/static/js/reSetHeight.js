// 函數：根據右側內容高度動態調整左側面板高度
function adjustLeftPanelHeight() {
  const leftPanel = document.querySelector('.left-panel');
  const performanceSection = document.querySelector('.right-panel-down');
  const chartSection = document.querySelector('.right-panel');

  // 判斷目前顯示的內容（每日報酬率或權重比較）
  if (performanceSection && performanceSection.offsetHeight > 0) {
      // 每日報酬率模式：高度對齊折線圖
      leftPanel.style.height = chartSection.offsetHeight + 'px';
  } else if (chartSection && chartSection.offsetHeight > 0) {
      // 權重比較模式：高度對齊甜甜圈圖外框
      leftPanel.style.height = chartSection.offsetHeight + 'px';
  } else {
      leftPanel.style.height = 'auto'; // 預設為自適應
  }
}

// 監聽視窗調整事件，確保即時調整高度
window.addEventListener('resize', adjustLeftPanelHeight);
document.addEventListener('DOMContentLoaded', adjustLeftPanelHeight);
