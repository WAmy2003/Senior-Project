import os
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By

# 自動安裝或確認 ChromeDriver 版本
chromedriver_autoinstaller.install()

# 設定 Chrome 參數
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # 無頭模式（不顯示 GUI）
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 如果知道 Chrome 的路徑，可以明確設定
chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# 初始化 WebDriver
driver = webdriver.Chrome(options=chrome_options)

# 假設你的字典叫做 stocks_dict
stocks_dict = {
    "1101": [["台泥", "台灣水泥"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321488%3B%26%2327877%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "1216": [["統一"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2332113%3B%26%2319968%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "1301": [["台塑", "台灣塑膠"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321488%3B%26%2322609%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
	"1303": [["南亞"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321335%3B%26%2320126%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "1326": [["台化", "台灣化學"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321488%3B%26%2321270%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "1590": [["亞德客-KY", "亞德客"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2320126%3B%26%2324503%3B%26%2323458%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2002": [["中鋼", "台灣鋼鐵"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2320013%3B%26%2337628%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2207": [["和泰車", "和泰汽車", "和泰"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321644%3B%26%2327888%3B%26%2336554%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2301": [["光寶科", "光寶"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2320809%3B%26%2323542%3B%26%2331185%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2303": [["聯電", "聯華電子"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2332879%3B%26%2338651%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2308": [["台達電"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321488%3B%26%2336948%3B%26%2338651%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2317": [["鴻海"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2340251%3B%26%2328023%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2327": [["國巨"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2322283%3B%26%2324040%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2330": [["台積電", "台積"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%A5%78%BF%6E%B9%71%2B%A4%E9%B4%C1%26gt%3B%3D20240401%2B%A4%E9%B4%C1%26lt%3B%3D20240630%2B%B3%F8%A7%4F%3D%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2345": [["智邦"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2326234%3B%26%2337030%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2357": [["華碩"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2333775%3B%26%2330889%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2379": [["瑞昱"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%B7%E7%AC%52%2B%A4%E9%B4%C1%26gt%3B%3D20240401%2B%A4%E9%B4%C1%26lt%3B%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2382": [["廣達"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%BC%73%B9%46%2B%A4%E9%B4%C1%26gt%3B%3D20240401%2B%A4%E9%B4%C1%26lt%3B%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2395": [["研華"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2330740%3B%26%2333775%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2408": [["南亞科"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321335%3B%26%2320126%3B%26%2331185%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2412": [["中華電"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2320013%3B%26%2333775%3B%26%2338651%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2454": [["聯發科"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2332879%3B%26%2330332%3B%26%2331185%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2603": [["長榮", "貨櫃"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2338263%3B%26%2327054%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2880": [["華南金","華南", "華銀"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2333775%3B%26%2321335%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2881": [["富邦金","富邦"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2323500%3B%26%2337030%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2882": [["國泰金", "國泰"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2322283%3B%26%2327888%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2883": [["開發金", "凱基"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2338283%3B%26%2330332%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2884": [["玉山金", "玉山"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2329577%3B%26%2323665%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2885": [["元大金", "元大"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2320803%3B%26%2322823%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2886": [["兆豐金", "兆豐"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2320806%3B%26%2335920%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2887": [["台新金", "台新", "新光"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321488%3B%26%2326032%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2890": [["永豐金", "永豐"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2327704%3B%26%2335920%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2891": [["中信金", "中國信託", "中信"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2320013%3B%26%2320449%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2892": [["第一金"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2331532%3B%26%2319968%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "2912": [["統一超", "統一超商", "7-ELEVEN"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2332113%3B%26%2319968%3B%26%2336229%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "3008": [["大立光"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2322823%3B%26%2331435%3B%26%2320809%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "3017": [["奇鋐"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2322855%3B%26%2337584%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "3034": [["聯詠"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2332879%3B%26%2335424%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "3037": [["欣興"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2327427%3B%26%2333288%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "3045": [["台灣大", "台灣大哥大", "電信三雄"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321488%3B%26%2328771%3B%26%2322823%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "3231": [["緯創"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2332239%3B%26%2321109%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "3661": [["世芯-KY", "世芯"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2319990%3B%26%2333455%3B-KY%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "3711": [["日月光投控", "日月光"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2326085%3B%26%2326376%3B%26%2320809%3B%26%2325237%3B%26%2325511%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "4904": [["遠傳", "電信三雄"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2336960%3B%26%2320659%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "4938": [["和碩", "童子賢"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321644%3B%26%2330889%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "5871": [["中租-KY", "中租"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2320013%3B%26%2331199%3B-KY%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "5876": [["上海商銀", "上海"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2319978%3B%26%2328023%3B%26%2321830%3B%26%2337504%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "5880": [["合庫金", "合作金庫", "合庫"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321512%3B%26%2324235%3B%26%2337329%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "6505": [["台塑化", "台塑"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2321488%3B%26%2322609%3B%26%2321270%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"],
    "6669": [["緯穎"], "https://insight.udndata.com/ndapp/Searchdec?udndbid=udnfree&page={}&SearchString=%26%2332239%3B%26%2331310%3B%2B%A4%E9%B4%C1%3E%3D20240401%2B%A4%E9%B4%C1%3C%3D20240630%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8&sharepage=20&select=1&kind=2"]
}


# 遍歷每個股票代號
for stock_code, (keywords, base_url) in stocks_dict.items():
    results = []
    page_number = 1

    while True:
        url = base_url.format(page_number)
        print(f"正在抓取股票代號 {stock_code} 的第 {page_number} 頁：{url}")

        # 使用 Selenium 加載頁面
        driver.get(url)

        # 等待網頁完全加載
        driver.implicitly_wait(10)

        # 查找所有文章標題元素
        news_items = driver.find_elements(By.CLASS_NAME, 'news')

        # 如果找不到任何文章，則停止
        if not news_items:
            print(f"沒有找到更多 {stock_code} 的文章，結束抓取。")
            break

        # 處理新聞標題
        for item in news_items:
            title_tag = item.find_element(By.TAG_NAME, 'a')
            title = title_tag.text
            for keyword in keywords:
                if keyword in title:
                    date = item.find_element(By.CLASS_NAME, 'source').text.split('·')[0].strip()
                    results.append({'date': date, 'title': title})

        # 跳到下一頁
        page_number += 1

        # 儲存結果到對應的 txt 檔案
        file_name = f"{stock_code}_新聞.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            for result in results:
                f.write(f"日期: {result['date']}, 標題: {result['title']}\n")

    print(f"抓取完成，{stock_code} 的結果已儲存至 {file_name}")

    # 隨機等待時間（例如：1 到 3 秒之間）
    time.sleep(random.uniform(1, 3))

# 關閉瀏覽器
driver.quit()


