import requests
import pandas as pd
from datetime import datetime
import os

def get_translated_weather():
    # 從 GitHub Secrets 讀取 API Key
    api_key = os.getenv('OPENWEATHER_API_KEY')
    city_name = "Taoyuan" 
    
    if not api_key:
        print("錯誤：找不到 API Key，請檢查 GitHub Secrets 設定。")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=zh_tw"
    response = requests.get(url)
    
    if response.status_code == 200:
        raw_data = response.json()
        df = pd.json_normalize(raw_data)
        
        # 欄位翻譯與轉換邏輯 (同前次對話內容)
        translation_map = {
            'name': '城市名稱',
            'dt': '數據更新時間',
            'main.temp': '目前氣溫(°C)',
            'main.feels_like': '體感溫度(°C)',
            'main.temp_min': '最低溫(°C)',
            'main.temp_max': '最高溫(°C)',
            'main.pressure': '大氣壓力(hPa)',
            'main.humidity': '濕度(%)',
            'main.sea_level': '海平面氣壓(hPa)',
            'main.grnd_level': '地面氣壓(hPa)',
            'visibility': '能見度(m)',
            'wind.speed': '風速(m/s)',
            'wind.deg': '風向(度)',
            'clouds.all': '雲量(%)',
            'sys.sunrise': '日出時間',
            'sys.sunset': '日落時間',
            'sys.country': '國家代碼',
            'coord.lon': '經度',
            'coord.lat': '緯度',
            'weather.0.description': '詳細天氣狀況',
            'weather.0.main': '天氣主類別'
        }
        
        if 'dt' in df.columns:
            df['dt'] = df['dt'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
        
        existing_cols = [c for c in translation_map.keys() if c in df.columns]
        final_df = df[existing_cols].rename(columns=translation_map)
        
        # 寫入 CSV
        file_path = 'human_readable_weather.csv'
        file_exists = os.path.isfile(file_path)
        final_df.to_csv(file_path, mode='a', index=False, header=not file_exists, encoding='utf-8-sig')
        print(f" 已更新數據：{datetime.now()}")
    else:
        print(f" 抓取失敗：{response.status_code}")

if __name__ == "__main__":
    get_translated_weather()