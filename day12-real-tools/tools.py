import os 
import requests
import time
from dotenv import load_dotenv
from tavily import TavilyClient # 这是一个假设的库，用于与 Tavily API 交互

# 加载环境变量
load_dotenv()
AMAP_KEY = os.getenv("AMAP_KEY") # 从环境变量中获取高德地图API的key

tavily = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))# 初始化 Tavily 客户端，使用环境变量中的 API key

# 城市代码
CITY_MAP = {
    "北京": "110000", "上海": "310000", "广州": "440100",
    "深圳": "440300", "杭州": "330100", "成都": "510100",
    "武汉": "420100", "西安": "610100", "南京": "320100",
}

# 获取天气信息的工具函数
def get_weather(city:str)->dict:
    time.sleep(1)  # 模拟网络延迟
    code = CITY_MAP.get(city)  # 根据城市名称获取对应的城市代码
    if not code:
        return {"error": f"暂不支持城市: {city}", "supported": list(CITY_MAP.keys())}
    if not AMAP_KEY:
        return {"error": "未配置 AMAP_KEY"}
    try:
        r = requests.get("https://restapi.amap.com/v3/weather/weatherInfo", # 高德天气API的URL
                         params={"key": AMAP_KEY, "city": code, "extensions": "base"},  # 请求参数
                         timeout = 5,  # 设置请求超时时间
                         )
        data = r.json() # 解析JSON响应
        if data["status"] !="1":
            return {"error": f"API 错误: {data.get('info')}"}
        live = data["lives"][0] # 获取天气信息
        return {
            "city": live["city"],
            "weather": live["weather"],
            "temperature": live["temperature"],
            "wind": f"{live['winddirection']}风{live['windpower']}级",
            "humidity": live["humidity"],
        }
    except Exception as e:
        return {"error": str(e)}

# 接搜索 API
def web_search(query:str,top_k:int = 3)->list: # 模拟一个搜索工具,query:搜索关键词,top_k:返回的搜索结果数量
    """搜索互联网最新信息"""
    try:
        result = tavily.search(query = query,max_results = top_k,search_depth = "basic") # 调用 Tavily 的搜索方法，传入查询关键词和返回结果数量
        return [
            {"title": r["title"], "url": r["url"], "content": r["content"][:300]} # 截取内容的前300个字符,返回标题、URL和内容摘要,组成一个字典列表
            for r in result.get("results", []) # 遍历搜索结果,如果 result 里有 "results"，就取它；如果没有，就返回空列表 []，避免程序报错。
        ]
    except Exception as e:
        return [{"error": str(e)}]  #把错误信息返回成列表形式。

#测试
if __name__ == "__main__":
    print(web_search("武汉今天天气？", top_k=5)) # 测试搜索工具，查询武汉今天天气的信息，返回前5条结果