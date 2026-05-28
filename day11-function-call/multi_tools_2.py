import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))

# ---- 假工具实现 ----
def get_weather(city:str)->str:  # 模拟一个天气查询工具
    fake ={
         "北京": "晴 22℃ 北风 2 级",
        "上海": "多云 25℃ 东风 3 级",
        "深圳": "雷阵雨 28℃",
        "杭州": "阴 24℃",
    }
    return fake.get(city,f"未知城市 {city} 的天气")

def get_news(topic: str, top_k: int = 3)->str: # 模拟一个新闻查询工具
    fake = [
        {"title": f"关于「{topic}」的最新报道 1", "source": "新华社"},
        {"title": f"业内专家解读「{topic}」最新动态 2", "source": "财新"},
        {"title": f"「{topic}」相关数据公开 3", "source": "界面新闻"},
        {"title": f"「{topic}」现场直击 4", "source": "央视"},
    ]
    return fake[:top_k]

# ---- 工具注册表 ----
TOOL_FUNCS={ # 将工具名称映射到实际函数
     "get_weather": get_weather,
    "get_news": get_news,
}
TOOL_SCHEMAS=[  # 工具定义列表，提供给模型使用,包含工具的名称、描述和参数信息,以 JSON Schema 格式描述参数结构
    {
        "type":"function",
        "function":{
            "name":"get_weather",
            "description": "查询某个城市的实时天气",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{"type": "string", "description": "城市名"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type":"function",
        "function":{
            "name":"get_news",
            "description": "获取关于某个话题的最新新闻列表",
            "parameters":{
                "type":"object",
                "properties":{
                    "topic": {"type": "string", "description": "新闻话题关键词"},
                    "top_k": {"type": "integer", "description": "返回条数", "default": 3},
                },
                "required": ["topic"],
            },
        },
    },
]

def call_tool(name:str,args:dict):  # 调用工具,根据工具名称从注册表中找到对应的函数并执行
    func= TOOL_FUNCS.get(name)
    if not func:
        raise ValueError(f"未知工具: {name}")
    return func(**args)

def chat_with_tools(user_input:str,max_iter:int=5): # 与工具进行对话
    messages = [{"role": "user", "content": user_input}]

    for i in range(max_iter):
        resp = client.chat.completions.create(
            model = "deepseek-chat",
            messages = messages,
            tools = TOOL_SCHEMAS, # 提供工具定义
            tool_choice = "auto", # 让模型自动选择是否调用工具
        )
        msg = resp.choices[0].message

        # 没有工具调用 → 模型给了最终回复
        if not msg.tool_calls:
            print(f"\n[Bot] {msg.content}")
            return msg.content
        
        # 把模型的决策也加入历史
        messages.append({
            "role":"assistant",
            "content": msg.content,
            "tool_calls":[tc.model_dump() for tc in msg.tool_calls], # 将工具调用信息转换为可序列化的格式
        })

        # 执行所有工具调用
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments) # 将参数字符串解析为字典
            print(f"  ↳ 调用 {name}({args})")
            result = call_tool(name,args) # 调用工具并获取结果
            print(f"  ↳ 结果: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, ensure_ascii=False),
            })
    return "(达到最大迭代次数)"

#测试
if __name__ == "__main__":
    chat_with_tools("北京今天多少度？")
    print("\n" + "=" * 40)
    chat_with_tools("帮我查 3 条关于『AI 大模型』的新闻")
    print("\n" + "=" * 40)
    chat_with_tools("先告诉我上海天气，再查 2 条关于上海的新闻")
    print("\n" + "=" * 40)