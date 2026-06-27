from pydantic import BaseModel,Field
from langchain_core.tools import StructuredTool

class WeatherInput(BaseModel):
    city:str = Field(...,description = "城市名（中文），例如：北京")
    day:int = Field(1,description = "预报天数 1-7",ge = 1,le = 7)

def fetch_weather(city:str,days:int)->str:
    return f"{city} 未来 {days} 天天气：晴 22℃"

weather_tool = StructuredTool.from_function(
    func = fetch_weather,
    name = "weather_tool",
    description = "查询某个城市未来几天的天气",
    args_schema = WeatherInput
)