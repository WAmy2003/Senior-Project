document.addEventListener('DOMContentLoaded', function () {
    // 創建工具提示元素
    const tooltip = document.createElement('div');
    tooltip.style.position = 'absolute';
    tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    tooltip.style.color = '#fff';
    tooltip.style.padding = '5px';
    tooltip.style.borderRadius = '5px';
    tooltip.style.pointerEvents = 'none';
    tooltip.style.display = 'none';
    document.body.appendChild(tooltip);

    // 這個是為了處理顯示鼠標懸停時的欄位標題
    document.querySelectorAll('td').forEach(function (cell) {
        cell.addEventListener('mouseenter', function (event) {
            const columnHeader = event.target.closest('table').querySelectorAll('th')[event.target.cellIndex].textContent;
            tooltip.textContent = columnHeader;
            tooltip.style.display = 'block';
        });

        cell.addEventListener('mousemove', function (event) {
            tooltip.style.left = event.pageX + 10 + 'px';
            tooltip.style.top = event.pageY + 10 + 'px';
        });

        cell.addEventListener('mouseleave', function () {
            tooltip.style.display = 'none';
        });
    });
});
