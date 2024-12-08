const ctxSmartPick = document.getElementById('chart-smart-pick').getContext('2d');
const ctx0050 = document.getElementById('chart-0050').getContext('2d');

const smartPickChart = new Chart(ctxSmartPick, {
    type: 'pie',
    data: {
        labels: ['A', 'B', 'C'],
        datasets: [{
            data: [50, 30, 20],
            backgroundColor: ['#ff9999','#66b3ff','#99ff99'],
            borderColor: ['#ff6666','#3399ff','#66ff66'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true, // 保持比例
        plugins: {
            legend: {
                position: 'top',
            },
        },
        aspectRatio: 1, // 圓餅圖保持正方形
        elements: {
            arc: {
                borderWidth: 1,
            }
        },
    }
});

const chart0050 = new Chart(ctx0050, {
    type: 'pie',
    data: {
        labels: ['X', 'Y', 'Z'],
        datasets: [{
            data: [40, 40, 20],
            backgroundColor: ['#ff9999','#66b3ff','#99ff99'],
            borderColor: ['#ff6666','#3399ff','#66ff66'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 1,
    }
});
