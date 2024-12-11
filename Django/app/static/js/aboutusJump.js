document.addEventListener('DOMContentLoaded', function () {
  // 取得「關於我們」的鏈接
  const aboutUsLink = document.querySelector('a[href="/aboutus/"]');  // 修改為正確的 URL

  // 當點擊「關於我們」時，顯示開發團隊部分
  aboutUsLink.addEventListener('click', function (event) {
      event.preventDefault();  // 阻止默認跳轉行為
      
      // 隱藏所有其他區域
      document.getElementById('techSection').style.display = 'none';
      document.getElementById('timeSection').style.display = 'none';
      
      // 顯示開發團隊區域
      document.getElementById('teamSection').style.display = 'block';
  });

  window.addEventListener('scroll', function () {
    const teamSectionBottom = document.getElementById('teamSection').getBoundingClientRect().bottom;
    const techSectionTop = document.getElementById('techSection').getBoundingClientRect().top;

    // 當滾動到開發團隊底部時，顯示開發技術
    if (teamSectionBottom <= window.innerHeight) {
        const techSection = document.getElementById('techSection');
        techSection.style.display = 'block';
        techSection.style.opacity = '1';
        techSection.style.height = 'auto';
    }

    // 當滾動到開發技術底部時，顯示開發時程
    if (techSectionTop <= window.innerHeight) {
        const timeSection = document.getElementById('timeSection');
        timeSection.style.display = 'block';
        timeSection.style.opacity = '1';
        timeSection.style.height = 'auto';
    }
});

})

// 顯示 techSection 區域
document.getElementById('techSection').style.display = 'block';
document.getElementById('techSection').style.opacity = '1';
document.getElementById('techSection').style.height = 'auto'; // 或設置明確高度


// 顯示開發時程區塊
document.getElementById('timeSection').style.display = 'block';
document.getElementById('timeSection').style.opacity = '1';
document.getElementById('timeSection').style.height = 'auto'; // 或設置明確高度

