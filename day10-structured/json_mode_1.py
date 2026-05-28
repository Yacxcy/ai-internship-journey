import os # 导入os模块，用于获取环境变量
import json # 导入json模块，用于处理JSON数据
from openai import OpenAI # 导入OpenAI模块，用于访问OpenAI API
from dotenv import load_dotenv # 导入dotenv模块，用于加载环境变量

load_dotenv() # 加载环境变量
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL")) # 创建OpenAI客户端实例

resp = client.chat.completions.create(
    model = "deepseek-v4-pro", # 模型名称
    messages =[
        {"role":"system","content":"你是信息抽取助手。必须输出 JSON 格式，包含 name (string), age (int), skills (string[]) 三个字段。"},
        {"role": "user","content": "我叫张三，今年 25 岁，会 Python 和 SQL。"},
    ],
    response_format = {"type":"json_object"}, # 指定响应格式为JSON对象
    temperature = 0, # 温度参数，控制生成文本的随机程度，0表示最确定的输出
)

raw = resp.choices[0].message.content # 获取模型生成的内容
print(raw)
data = json.loads(raw)
print(type(data), data["name"]) # 输出数据类型和内容