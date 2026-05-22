import os # 导入os模块，用于访问环境变量
import sys # 导入sys模块，用于访问命令行参数
import argparse # 导入argparse模块，用于解析命令行参数
import requests # 导入requests模块，用于发送HTTP请求
from dotenv import load_dotenv

load_dotenv() # 加载环境变量
# 从环境变量中获取高德地图API的key
AMAP_KEY = os.getenv("AMAP_KEY")

# 城市代码映射
CITY_MAP = {
    "beijing": "110000", "北京": "110000",
    "shanghai": "310000", "上海": "310000",
    "shenzhen": "440300", "深圳": "440300",
    "guangzhou": "440100", "广州": "440100",
    "hangzhou": "330100", "杭州": "330100",
}

def get_weather(city: str)->dict:
    code = CITY_MAP.get(city.lower()) # 默认使用北京的城市代码
    if not code:
        raise ValueError(f"暂不支持城市: {city}") # 如果城市不在映射表中，抛出异常
    if not AMAP_KEY:
         raise RuntimeError("未配置 AMAP_KEY，请先在 .env 中填入") # 如果没有设置API key，抛出异常
    url = "https://restapi.amap.com/v3/weather/weatherInfo" # 高德地图天气API的URL
    params = {"key": AMAP_KEY, "city": code, "extensions": "base"} # 请求参数，包括API key、城市代码和返回的天气信息类型
    r = requests.get(url,params=params,timeout=5) # 发送GET请求，获取天气信息，设置超时时间为5秒
    r.raise_for_status() # 如果请求失败，抛出HTTPError异常
    data = r.json() # 返回JSON格式的天气信息
    if data.get("status") != "1":
        raise RuntimeError(f"API 错误: {data.get('info')}") # 如果API返回的状态不是成功，抛出异常
    return data["lives"][0] # 返回天气信息中的第一条记录

def main():
    parser = argparse.ArgumentParser(description= "查询城市实时天气") # 创建命令行参数解析器
    parser.add_argument("city", help="城市名（中文或拼音），如 北京 / beijing") # 添加一个位置参数，用于指定要查询的城市
    args = parser.parse_args() # 解析命令行参数
    try:
        live = get_weather(args.city)
        print(f"📍 {live['city']}")
        print(f"🌤  {live['weather']} {live['temperature']}℃")
        print(f"💨 {live['winddirection']}风 {live['windpower']}级")
        print(f"💧 湿度 {live['humidity']}%")
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr) # 输出错误信息
        sys.exit(1) # 如果发生异常，打印错误信息到标准错误，并以非零状态码退出程序

#测试
if __name__ == "__main__":
    main()