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

folder_path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集'

# 定義需要獲取的財務指標
financial_statements_cols = {
    'IncomeAfterTaxes': ['IncomeAfterTaxes', 'IncomeAfterTax'],
    'TotalConsolidatedProfitForThePeriod': ['TotalConsolidatedProfitForThePeriod', 'OtherComprehensiveIncomeAfterTaxThePeriod'],
    'Revenue': ['Revenue'],
    'GrossProfit': ['GrossProfit', 'NetInterestIncome']
}
balance_sheet_cols = {
    'CurrentAssets':['CurrentAssets'],
    'CurrentLiabilities':['CurrentLiabilities'],
    'NonCurrentLiabilities':['NoncurrentLiabilities'],
    'Equity':['Equity']}
cash_flows_cols = {'NetCashInflowFromOperatingActivities':['NetCashInflowFromOperatingActivities']}


for id in stock_ids:

    # # 獲取個股綜合損益表數據
    # financial_data = loader.taiwan_stock_financial_statement(stock_id=id,start_date='2023-12-31',end_date='2024-03-31')
    # # 篩選需要的財務指標
    # selected_data_frames = []
    # for col_name, possible_types in financial_statements_cols.items():
    #     filtered_data = financial_data[financial_data['type'].isin(possible_types)].copy()
    #     filtered_data.loc[:, 'type'] = col_name  # 將列名標準化
    #     selected_data_frames.append(filtered_data)
    # # 綜合損益表特例
    # # 如果沒有 GrossProfit 或 NetInterestIncome，計算 Revenue - CostOfGoodsSold
    # if not any(financial_data['type'].isin(['GrossProfit', 'NetInterestIncome'])):
    #     revenue_data = financial_data[financial_data['type'] == 'Revenue'].copy()
    #     cogs_data = financial_data[financial_data['type'] == 'CostOfGoodsSold'].copy()
        
    #     if not revenue_data.empty and not cogs_data.empty:
    #         revenue_data.set_index('date', inplace=True)
    #         cogs_data.set_index('date', inplace=True)
    #         gross_profit_data = revenue_data['value'] - cogs_data['value']
    #         gross_profit_df = gross_profit_data.reset_index()
    #         gross_profit_df['type'] = 'GrossProfit'
    #         selected_data_frames.append(gross_profit_df)
    # # 如果沒有 Revenue，使用 NetInterestIncome + NetNonInterestIncome
    # if 'Revenue' not in financial_data['type'].unique():
    #     nii_data = financial_data[financial_data['type'] == 'NetInterestIncome'].copy()
    #     nnii_data = financial_data[financial_data['type'] == 'NetNonInterestIncome'].copy()
        
    #     if not nii_data.empty and not nnii_data.empty:
    #         nii_data.set_index('date', inplace=True)
    #         nnii_data.set_index('date', inplace=True)
    #         revenue_data = nii_data['value'] + nnii_data['value']
    #         revenue_df = revenue_data.reset_index()
    #         revenue_df['type'] = 'Revenue'
    #         selected_data_frames.append(revenue_df)
    
    # # 獲取個股資產負債表數據
    # financial_data = loader.taiwan_stock_balance_sheet(stock_id=id,start_date='2023-12-31',end_date='2024-03-31')
    # # 篩選需要的財務指標
    # selected_data_frames = []
    # for col_name, possible_types in balance_sheet_cols.items():
    #     filtered_data = financial_data[financial_data['type'].isin(possible_types)].copy()
    #     filtered_data.loc[:, 'type'] = col_name  # 將列名標準化
    #     selected_data_frames.append(filtered_data)
    
    # 獲取個股現金流量表數據
    financial_data = loader.taiwan_stock_cash_flows_statement(stock_id=id, start_date='2023-12-31', end_date='2024-03-31')
    # 篩選需要的財務指標
    selected_data_frames = []
    for col_name, possible_types in cash_flows_cols.items():
        filtered_data = financial_data[financial_data['type'].isin(possible_types)].copy()
        filtered_data.loc[:, 'type'] = col_name  # 將列名標準化
        selected_data_frames.append(filtered_data)



    # 合併所有篩選後的數據
    if selected_data_frames:
        financial_data_filtered = pd.concat(selected_data_frames)
        financial_data_pivot = financial_data_filtered.pivot_table(index='date', columns='type', values='value')
    else:
        financial_data_pivot = pd.DataFrame(index=financial_data['date'].unique())
    
    # # 資產負債表特例
    # # 添加缺失的欄位並設置為空值
    # for col in balance_sheet_cols.keys():
    #     if col not in financial_data_pivot.columns:
    #         financial_data_pivot[col] = np.nan


    # financial_data_pivot = financial_data_pivot[list(financial_statements_cols.keys())]
    # financial_data_pivot = financial_data_pivot[list(balance_sheet_cols.keys())]
    financial_data_pivot = financial_data_pivot[list(cash_flows_cols.keys())]

    # 刪除 'date' 欄位
    # financial_data_pivot.reset_index(drop=True, inplace=True)

    # 構造文件路徑
    output_file = os.path.join(folder_path, f'{id}_基本面.csv')

    # 將數據追加保存到現有的 CSV 文件
    if os.path.exists(output_file):
        existing_data = pd.read_csv(output_file, encoding='utf-8-sig')
        existing_data = pd.concat([existing_data, financial_data_pivot.reset_index(drop=True)], axis=1)
        existing_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    else:
        financial_data_pivot.reset_index().to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f'數據已成功保存至 {output_file}')
print('數據已全數存取')


    # financial_data_pivot = financial_data_pivot[list(financial_statements_cols.values())]
    # financial_data_pivot.columns = ['IncomeAfterTaxes', 'TotalConsolidatedProfitForThePeriod', 'Revenue', 'GrossProfit']
    # # 重設索引，以確保 'date' 列存在
    # financial_data_pivot.reset_index(inplace=True)
    # output_file = f'{id}_基本面.csv'
    # financial_data_pivot.to_csv(output_file, index=False, encoding='utf-8-sig')
    # balance_sheet_data = loader.taiwan_stock_balance_sheet(stock_id=id,start_date='2024-03-01',end_date='2024-06-30')
    # cash_flows_data = loader.taiwan_stock_cash_flows_statement(stock_id=id,start_date='2024-03-01',end_date='2024-06-30')

# 篩選需要的財務指標
    
    # balance_sheet_filtered = balance_sheet_data[balance_sheet_data['type'].isin(balance_sheet_cols)]
    # cash_flows_filtered = cash_flows_data[cash_flows_data['type'].isin(cash_flows_cols)]

    # 將數據透過 'date' 和 'type' 進行透視，整理成橫向表格
    
    # balance_sheet_pivot = balance_sheet_filtered.pivot_table(index='date', columns='type', values='value')
    # cash_flows_pivot = cash_flows_filtered.pivot_table(index='date', columns='type', values='value')

    # 合併數據框
    # merged_data = pd.concat([financial_data_pivot, balance_sheet_pivot, cash_flows_pivot], axis=1)

