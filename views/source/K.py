from fugle_marketdata import RestClient
import datetime as dt

# 獲取今天和一年前的日期
end_date = dt.date.today()
start_date = end_date - dt.timedelta(days=365)

key = "Njg1M2VkY2ItZjQ2NC00M2VjLTk5NjMtODFlMjA3YzA2NzdlIDY3NGQ3ZTRmLWZkNDktNGVkNy1iMTkyLTUzZDk4ODY4YzkwMw=="
client = RestClient(api_key = key) 
stock = client.stock  # Stock REST API client

def get_stock_data(stock_id):
    data = stock.historical.candles(**{"symbol": stock_id, "from": start_date.strftime('%Y-%m-%d'), "to": end_date.strftime('%Y-%m-%d'), "fields": "open,high,low,close,volume,change"})
    return  data