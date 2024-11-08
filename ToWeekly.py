import pandas as pd
import os

# 股票代碼清單
stock_ids = [
    '2330', '2317', '2454', '2308', '2382', '2891', '2881', '2303', '3711', '2882',
    '2886', '2412', '2884', '1216', '2885', '3034', '2357', '2890', '2892', '3231',
    '2345', '3008', '2327', '5880', '2002', '2880', '2379', '1303', '2883', '6669',
    '1101', '2887', '3037', '2301', '3017', '1301', '4938', '2207', '3661', '2603',
    '2395', '3045', '5876', '1326', '4904', '2912', '1590', '5871', '6505', '2408'
]

weekly_data_path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\原始數據_週'

for stock_id in stock_ids:
    try:
        # 讀取日資料
        df = pd.read_csv(f'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\原始數據\\{stock_id}_數據蒐集.csv', parse_dates=['date'])

        # 設定日期為索引並將資料按週聚合
        df.set_index('date', inplace=True)
        weekly_df = df.resample('W').agg({
            'Dealer': 'sum',  # 例子：交易員買賣取合計
            'Foreign_Investor': 'sum',  # 外資買賣取合計
            'Investment_Trust': 'sum',  # 投信買賣取合計
            'RSI': 'mean',  # RSI 取平均值
            'SMA': 'mean',  # SMA 取平均值取
            'WMA': 'mean',  # WMA 取平均值
            'MACD': 'mean',  # MACD 取平均值
            'MACD_Signal': 'mean',  # MACD_Signal 取平均值
            'KD_K': 'mean',  # KD_K 取平均值
            'KD_D': 'mean',  # KD_D 取平均值
            'Bollinger_Upper': 'mean',  # Bollinger_Upper 取平均值
            'Bollinger_Middle': 'mean',  # Bollinger_Middle 取平均值
            'Bollinger_Lower': 'mean',  # Bollinger_Lower 取平均值
            'CK_Index': 'mean',  # CK_Index 取平均值
            'sentiment_score': 'mean',  # sentiment_score 取平均值
            'close': 'last'  # close 收盤價取每週的最後一個值
        }).reset_index()

        # 檢查轉換後的結果
        weekly_df.to_csv(os.path.join(weekly_data_path, f'{stock_id}_數據蒐集.csv'), index=False)
        print(f"{stock_id} 週資料已儲存")
    
    except Exception as e:
        print(f"處理 {stock_id} 時發生錯誤: {e}")