import os
import json

def parse_news_file(file_path):
    news_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('日期:'):
                # 解析日期和標題
                parts = line.split('．')
                date = parts[0].replace('日期: ', '').strip()
                title_part = parts[-1].split('標題: ')
                title = title_part[1].split('.')[1].strip() if len(title_part) > 1 else ""
                news_data.append({"date": date, "title": title})
    return news_data

def process_folder(folder_path):
    all_data = []
    seen_titles = set()  # 用來過濾重複的新聞標題
    for filename in os.listdir(folder_path):
        if filename.endswith('_新聞.txt'):
            stock_id = filename.split('_')[0]
            file_path = os.path.join(folder_path, filename)
            news_data = parse_news_file(file_path)
            # 過濾重複新聞
            filtered_news = []
            for news in news_data:
                if news['title'] not in seen_titles:
                    seen_titles.add(news['title'])
                    filtered_news.append(news)
            if filtered_news:
                all_data.append({"stockID": stock_id, "news": filtered_news})
    return all_data

def save_to_file(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 主程式
folder_path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\新聞資料'  # 替換為你的資料夾路徑
output_file = 'processed_news.txt'  # 儲存最終結果的檔案
all_news_data = process_folder(folder_path)
save_to_file(all_news_data, output_file)
print("處理完成，資料已儲存到", output_file)
