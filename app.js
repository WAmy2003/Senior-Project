//在 app.js 中建立 Express 伺服器，並設定路由來顯示各個頁面：

console.log("Starting the server...");
const express = require('express');
const app = express();
const PORT = 3000;

// 設定 EJS 模板引擎
app.set('view engine', 'ejs');
app.use(express.static('public'));

// 首頁路由
app.get('/', (req, res) => {
    res.render('index');
});

// 投資組合頁面路由
app.get('/portfolio', (req, res) => {
    const companies = [/* 放置蒐集的50家公司資訊陣列 */];
    res.render('portfolio', { companies });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
    