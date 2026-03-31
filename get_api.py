import requests
import pandas as pd
from datetime import datetime
import os

def get_translated_weather(api_key, city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=zh_tw"
    response = requests.get(url)
    
    if response.status_code == 200:
        raw_data = response.json()
        
        # 1. 使用 pandas 壓平 JSON
        df = pd.json_normalize(raw_data)
        
        # 2. 定義「中英文欄位對照表」
        # 你可以根據需要增加更多欄位
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
        
        # 3. 處理時間戳轉換 (將秒數轉成人類時間)
        time_columns = ['dt', 'sys.sunrise', 'sys.sunset']
        for col in time_columns:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
        
        # 4. 只保留我們有翻譯的欄位，並重新命名
        # 這樣就不會出現像是 'base' 或 'cod' 這些無意義的系統數據
        existing_cols = [c for c in translation_map.keys() if c in df.columns]
        final_df = df[existing_cols].rename(columns=translation_map)
        
        # 5. 寫入 CSV
        file_path = 'human_readable_weather.csv'
        file_exists = os.path.isfile(file_path)
        
        # encoding='utf-8-sig' 確保 Excel 打開中文不亂碼
        final_df.to_csv(file_path, mode='a', index=False, header=not file_exists, encoding='utf-8-sig')
        
        print(f"✅ 成功轉換！已將 {city_name} 的數據寫入 {file_path}")
        print(final_df.iloc[0]) # 在終端機印出轉換後的結果檢查
    else:
        print("❌ 抓取失敗，請確認 API Key。")

# --- 執行程式 ---
MY_API_KEY = "8ea92a8514a254bbc10f42f6fdfb1429"
get_translated_weather(MY_API_KEY, "Taoyuan")