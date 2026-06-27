import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

# 导入环境变量
load_dotenv()

AMAP_KEY = os.getenv("AMAP_KEY")

CITY_MAP = {
    "北京": "110000", "上海": "310000", "广州": "440100",
    "深圳": "440300", "杭州": "330100", "成都": "510100",
    "武汉": "420100", "西安": "610100", "南京": "320100",
}

@tool
def get_weather(city:str)->str:
    """查询中国主要城市的实时天气。

    参数 city: 城市名（中文），例如：北京、上海
    返回：天气描述字符串
    """
    code = CITY_MAP.get(city) # 获取城市代码
    if not code:
        return f"暂不支持 {city}，仅支持：{list(CITY_MAP.keys())}"
    try:
        r = requests.get(
            "https://restapi.amap.com/v3/weather/weatherInfo",
            params = {"key": AMAP_KEY, "city": code, "extensions": "base"},  #  实时天气
            timeout = 5,
            )
        live = r.json()["lives"][0]
        return f"{live['city']}：{live['weather']} {live['temperature']}℃，{live['winddirection']}风{live['windpower']}级，湿度 {live['humidity']}%"
    except Exception as e:
        return f"查询天气失败：{e}"

# 日历 / 提醒
@tool
def add_calendar_event(title:str,date:str,time:str = "09:00")->str:
    """添加日历事件（mock 版）。
    参数：
        title: 事件标题
        date: YYYY-MM-DD 格式
        time: HH:MM 格式，默认 09:00
    """
    # 这里 mock，存到 SQLite
    import sqlite3
    conn = sqlite3.connect("calendar.db")
    c = conn.cursor() # 创建表
    c.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, title TEXT, date TEXT, time TEXT)")
    c.execute("INSERT INTO events(title, date, time) VALUES(?,?,?)", (title, date, time))
    conn.commit() # 提交
    conn.close()
    return f"已添加日历事件：{title}，时间：{date} {time}"

@tool
def list_calendar_events(date:str)->str:
    """查询某天的日历事件。
    参数 date: YYYY-MM-DD 格式
    """
    import sqlite3
    conn = sqlite3.connect("calendar.db")
    c = conn.cursor()
    c.execute("SELECT title, time FROM events WHERE date=?", (date,))
    events = c.fetchall()
    conn.close()
    if not events:
        return f"{date} 无日程"
    return f"{date} 的日程：\n" + "\n".join(f"  {t} - {title}" for title, t in events)

#加密货币
@tool
def get_crypto_price(symbol:str)->str:
   """查询加密货币价格。
    参数 symbol: 例如 BTC / ETH / DOGE
    """
   try:
       r = requests.get(
           f"https://api.coingecko.com/api/v3/simple/price",
           params = {"ids":symbol.lower(),"vs_currencies":"usd"},
              timeout = 5,
       )
       data = r.json()
       if not data:
           return f"找不到 {symbol}"
       return f"{symbol.upper()}: ${list(data.values())[0]['usd']}"
   except Exception as e:
       return f"查询失败：{e}"

