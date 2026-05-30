import os 
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import get_weather, web_search

load_dotenv() # 加载环境变量
client = OpenAI(api_key = os.getenv("DEEPSEEK_API_KEY"), base_url = os.getenv("DEEPSEEK_BASE_URL")) # 初始化 OpenAI 客户端，使用环境变量中的 API key 和 base URL

# 工具映射表
TOOL_FUNCS = {
    "get_weather": get_weather,
    "web_search": web_search
}

# 定义工具 Schema
TOOL_SCHEMAS = [
    {
        "type":"function",
        "function":{
            "name":"get_weather",
            "description": "查询中国主要城市的实时天气，包括温度、天气状况、风向风力",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{"type":"string", "description":"城市名（中文），例如 北京"}, # city 参数是一个字符串类型，描述为城市名（中文），例如 北京
                },
                "required":["city"], # city 参数是必需的
            },
        },
    },
    {
        "type":"function",
        "function":{
            "name" : "web_search",
            "description" : "搜索互联网获取最新信息、新闻、资料。当用户问到实时/新近/不确定的内容时使用",
            "parameters":{
                "type":"object",
                "properties":{
                    "query":{"type":"string","description":"搜索关键词"},
                    "top_k": {"type": "integer", "description": "返回条数 1-5", "default": 3},
                },
                "required":["query"],
            },
        },
    },
]

# 处理工具调用的函数
def call_tool(name:str,args:dict):
    func = TOOL_FUNCS.get(name) # 从工具映射表中获取对应的函数
    if not func: # 如果函数不存在，则返回错误信息
        return {"error": f"未知工具 {name}"}
    try:
        return func(**args) # 调用函数，传入参数
    except Exception as e:
        return {"error": f"工具执行失败: {e}"}


# chat函数,接收用户输入，调用模型生成响应，处理工具调用，并返回最终结果
def chat(user_input:str,history:list = None,max_iter:int = 5):
    history = history or [] # 如果没有提供历史记录，则初始化为空列表
    messages = history + [{"role":"user","content":user_input}] # 将用户输入和历史记录组合成消息列表

    for i in range(max_iter):
        resp = client.chat.completions.create(
            model = "deepseek-chat", # 使用深度搜索模型
            messages = messages, # 传入消息列表
            tools = TOOL_SCHEMAS, # 提供工具的 Schema 供模型选择调用
            tool_choice = "auto", # 让模型自动选择是否调用工具
            temperature = 0, # 设置生成文本的随机程度，较低的值会使输出更确定
        )

        msg = resp.choices[0].message # 获取模型生成的消息

        if not msg.tool_calls:
            messages.append({"role":"assistant","content":msg.content}) # 如果没有工具调用，则直接将模型的回复添加到消息列表中
            return msg.content, messages # 返回模型的回复和更新后的消息列表
        
        messages.append({
            "role":"assistant",
            "content":msg.content,
            "tool_calls": [tc.model_dump() for tc in msg.tool_calls], # 将工具调用信息添加到消息列表中，供后续处理,如果有多个工具调用，则将它们都添加到消息列表中
            # 上述model_dump()方法将工具调用信息转换为可序列化的格式，就是将模型的输出转换为字典形式，以便后续处理。
        })

        for tc in msg.tool_calls:
            name = tc.function.name # 获取工具调用的名称
            args = json.loads(tc.function.arguments) # 获取工具调用的参数，并解析成字典,json.loads()方法将参数字符串转换为字典
            print(f"  ↳ {name}({args})")
            result = call_tool(name,args) # 调用工具函数，获取结果
            print(f"  ↳ {(str(result))[:120]}") # 打印工具调用的结果，截取前120个字符以避免输出过长

            messages.append({
                "role":"tool",
                "tool_call_id": tc.id, # 将工具调用的 ID 添加到消息列表中，以便模型知道这是哪个工具调用的结果
                "content": json.dumps(result,ensure_ascii=False), # 将工具调用的结果转换为 JSON 字符串，并添加到消息列表中
            })
    return "(达到最大迭代次数)", messages# 如果超过最大迭代次数，返回提示信息和消息列表


# 测试
if __name__ == "__main__":
    test_questions =[
        "北京今天多少度？",
        "上海天气怎么样？是不是要下雨？",
        "搜一下 2026 年 AI Agent 的最新进展",
        "你好你叫什么",  # 不该用工具
        "比较一下北京和深圳今天的温度",  # 多工具
    ]
    for q in test_questions:
        print(f"\n========== Q: {q} ==========")
        ans,_ = chat(q) # 调用 chat 函数，传入用户输入，并获取回复
        print(f"A: {ans}") # 打印模型的回复