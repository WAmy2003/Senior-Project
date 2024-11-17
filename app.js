import Headroom from "headroom.js";

// 選取導覽列
const navbar = document.querySelector("header");

// 初始化 Headroom
const headroom = new Headroom(navbar, {
    offset: 100, // 滾動超過 100px 後才觸發
    tolerance: 5, // 允許 5px 的滾動容忍值
    classes: {
        pinned: "headroom--pinned", // 當 header 固定時的類名
        unpinned: "headroom--unpinned", // 當 header 隱藏時的類名
    },
});
headroom.init(); // 啟用 Headroom
