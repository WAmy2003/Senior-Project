import pandas as pd
import FinMind
from FinMind.data import DataLoader
import os

# 初始化 DataLoader
loader = DataLoader()

# 設定 API 金鑰
# loader.login_by_token(api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyNC0wNy0xMCAyMzowMTowMCIsInVzZXJfaWQiOiJhbXl3ZWkiLCJpcCI6IjEwMS4xMi4xMDMuNjgifQ.PWaTGzQ9DzodEQWnpriU9AIUSwYFIsdc-tKzVH1HbrA')

folder_path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\csv檔'

# 股票代號列表
stock_ids = [
    '2330', '2317', '2454', '2308', '2382', '2891', '2881', '2303', '3711', '2882',
    '2886', '2412', '2884', '1216', '2885', '3034', '2357', '2890', '2892', '3231',
    '2345', '3008', '2327', '5880', '2002', '2880', '2379', '1303', '2883', '6669',
    '1101', '2887', '3037', '2301', '3017', '1301', '4938', '2207', '3661', '2603',
    '2395', '3045', '5876', '1326', '4904', '2912', '1590', '5871', '6505', '2408'
]

# 迴圈處理每隻股票
for id in stock_ids:
# 獲取個股三大法人買賣超數據
    data = loader.taiwan_stock_institutional_investors(
    stock_id=id, 
    start_date='2024-04-01',
    end_date='2024-06-30'
)

# 將數據轉換為 DataFrame
df = pd.DataFrame(data)

# 縮減 name 欄位為 Foreign_Investor、Investment_Trust、Dealer
def reduce_name(name):
    if 'Foreign' in name:
        return 'Foreign_Investor'
    elif 'Investment' in name:
        return 'Investment_Trust'
    else:
        return 'Dealer'

df['name'] = df['name'].apply(reduce_name)

# 使用 groupby 和 agg 函數進行聚合
df = df.groupby(['date', 'name']).agg({
    'buy': 'sum',
    'sell': 'sum'
}).reset_index()

# 新增 buy_sell 欄位計算淨買賣超
df['buy_sell'] = df['buy'] - df['sell']

# # 顯示處理後的數據
# print(df)

# Pivot the DataFrame to get the desired format
pivot_df = df.pivot_table(index='date', columns='name', values='buy_sell', fill_value=0).reset_index()
    
# 確保所有需要的列都存在
for column in ['Foreign_Investor', 'Investment_Trust', 'Dealer']:
    if column not in pivot_df.columns:
        pivot_df[column] = 0
output_file = os.path.join(folder_path, f'{id}_數據蒐集.csv')
# 將 DataFrame 存為 csv 檔案
for id in stock_ids:
    output_file = f'{id}_數據蒐集.csv'
    pivot_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f'數據已成功保存至 {output_file}')