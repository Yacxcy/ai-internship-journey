import os # 导入os模块，用于访问环境变量
from typing import List,Dict,Optional # 类型提示,用于指定函数参数和返回值的类型
from openai import OpenAI # 导入OpenAI模块，用于访问OpenAI API
from dotenv import load_dotenv # 导入load_dotenv函数，用于加载环境变量

load_dotenv() # 加载环境变量

# 创建一个LLMClient类，封装对OpenAI API的调用,提供更简洁的接口
class LLMClient:
    """LLMClient是一个封装了OpenAI API调用的客户端类，提供了更简洁的接口来与语言模型进行交互。"""
    # 初始化方法，创建一个OpenAI客户端实例
    def __init__(
            self,
            api_key:Optional[str] = None, # API key参数，默认为None，如果没有传入，则从环境变量中获取
            base_url:Optional[str] = None, # base_url参数，默认为None，如果没有传入，则从环境变量中获取
            model:str = "deepseek-v4-pro", # 模型参数，默认为"deepseek-v4-pro
            default_system : str = "你是一个有用的 AI 助手", # 默认的系统消息，设置模型的角色和行为
        ):
        self.client = OpenAI( # 创建一个OpenAI客户端实例
            api_key = api_key or os.getenv("DEEPSEEK_API_KEY"), # 从参数或环境变量中获取API key
            base_url = base_url or os.getenv("DEEPSEEK_BASE_URL"),  # 从参数或环境变量中获取base_url
        )
        self.model = model # 设置默认的模型
        self.default_system = default_system # 设置默认的系统消息

    def chat(
            self,
            prompt :str, # prompt参数，用户输入的文本
            system :Optional[str] = None, # system参数，系统消息，默认为None，如果没有传入，则使用默认的系统消息
            temperature :float = 0.7, # temperature参数，控制生成文本的随机程度，默认为0.7
            max_tokens :int = 1024, # max_tokens参数，控制生成文本的长度，默认为1024
        ) ->str:
        """单轮对话，返回字符串。""" 
        messages:List[Dict[str,str]]=[ # 创建一个消息列表，包含系统消息和用户输入的文本
            {"role":"system","content":system or self.default_system}, # 系统消息，使用传入的system参数或默认的系统消息
            {"role":"user","content":prompt},
        ]
        resp = self.client.chat.completions.create( # 调用OpenAI API创建一个聊天完成请求
            model = self.model, # 使用默认的模型
            messages = messages, # 传入消息列表
            temperature = temperature, # 传入temperature参数
            max_tokens = max_tokens, # 传入max_tokens参数
        )
        return resp.choices[0].message.content # 返回模型生成的文本内容

# 测试LLMClient类
if __name__=="__main__":
    # 创建一个LLMClient实例
    llm = LLMClient(default_system="你是 Python 老师，回答简洁不超过 50 字")
    # 调用chat方法，获取模型的回复  
    print(llm.chat("什么是 Python 装饰器？"))
    print("---")
    print(llm.chat("用一句话夸我学得快", temperature=1.2))