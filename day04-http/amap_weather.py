import os # 导入os模块，用于访问环境变量
import requests # 导入requests模块，用于发送HTTP请求
from dotenv import load_dotenv # 从dotenv模块导入load_dotenv函数，用于加载环境变量

load_dotenv() # 加载环境变量
# 从环境变量中获取高德地图API的key
AMAP_KEY = os.getenv("AMAP_KEY")

# 定义一个函数，获取指定城市的天气信息
def get_weather(city_code:str=110000):
    url = "https://restapi.amap.com/v3/weather/weatherInfo" # 高德地图天气API的URL
    params={"key": AMAP_KEY, "city": city_code,"extensions": "all"}# 请求参数，包括API key、城市代码和返回的天气信息类型
    r = requests.get(url,params = params,timeout = 5)# 发送GET请求，获取天气信息，设置超时时间为5秒
    r.raise_for_status() # 如果请求失败，抛出HTTPError异常
    return r.json()

# 获取北京的天气信息，并打印结果
if __name__ == "__main__":
    data = get_weather("420100")
    live = data["forecasts"][0]["casts"] # 从返回的JSON数据中提取天气信息
    city = data["forecasts"][0]["city"]
    print(f"{city}天气预报：")
    for day in live:
        print(f"{day['date']}: {day['dayweather']}, {day['daytemp']}℃, {day['daywind']}风{day['daypower']}级")
    #print(f"{city}: {live['weather']}, {live['temperature']}℃, {live['winddirection']}风{live['windpower']}级")
