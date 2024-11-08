import pandas as pd
import numpy as np
import os
from FinMind.data import DataLoader

# 初始化 DataLoader
loader = DataLoader()

# 股票代號列表
stock_ids = [
    '2330', '2317', '2454', '2308', '2382', '2891', '2881', '2303', '3711', '2882',
    '2886', '2412', '2884', '1216', '2885', '3034', '2357', '2890', '2892', '3231',
    '2345', '3008', '2327', '5880', '2002', '2880', '2379', '1303', '2883', '6669',
    '1101', '2887', '3037', '2301', '3017', '1301', '4938', '2207', '3661', '2603',
    '2395', '3045', '5876', '1326', '4904', '2912', '1590', '5871', '6505', '2408'
]

folder_path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\原始數據\\'

# 設定日期範圍
start_date = '2024-04-01'
end_date = '2024-06-30'

# 迴圈處理每隻股票
for stock_id in stock_ids:
    # 獲取收盤價資料
    price_data = loader.taiwan_stock_daily(
        stock_id=stock_id,
        start_date=start_date,
        end_date=end_date
    )
    
    # 過濾只保留日期和收盤價
    price_df = price_data[['date', 'close']].copy()
    
    # 將日期格式轉換為 yyyy/m/d
    price_df['date'] = pd.to_datetime(price_df['date']).dt.strftime('%Y/%-m/%-d')

    # 設定輸出 CSV 檔案路徑
    output_file = os.path.join(folder_path, f'{stock_id}_數據蒐集.csv')

    # 讀取現有的數據檔案
    if os.path.exists(output_file):
        original_df = pd.read_csv(output_file, encoding='utf-8-sig')
        
        # 檢查是否已經有 close 欄位
        if 'close' in original_df.columns:
            print(f"{stock_id} 已有 close 欄位，跳過合併。")
            continue
        
        # 確保原始資料的日期格式也為 yyyy/m/d
        original_df['date'] = pd.to_datetime(original_df['date']).dt.strftime('%Y/%-m/%-d')
        
        # 合併收盤價資料
        merged_df = pd.merge(original_df, price_df, on='date', how='left')
        
        # 檢查合併後是否有非空的 close 值
        if merged_df['close'].isna().all():
            print(f"{stock_id} 合併後的 close 欄位為空，請檢查日期格式或數據來源。")
            continue
    else:
        # 若檔案不存在，則直接使用收盤價資料
        merged_df = price_df

    # 將合併後的 DataFrame 存成 CSV
    merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f'數據已成功保存至 {output_file}')