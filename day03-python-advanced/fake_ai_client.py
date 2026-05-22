import time 
import random
import functools
from typing import Iterator

# ------装饰器------
#1.定义一个装饰器函数，用来记录函数的执行时间
def timer(func):
    @functools.wraps(func)
    #1.1 定义一个内部函数
    def wrapper(*args,**kwargs):
        #1.2 记录开始时间
        start = time.time()
        #1.3 运行原函数
        result = func(*args,**kwargs)
        #1.4 计算使用时间
        print(f"\n[耗时{time.time() - start:.3f}s]")
        #1.5 返回结果
        return result
    return wrapper

#2.定义一个装饰器函数，用来重复失败的函数
def retry(times:int = 3,delay : float = 0.5):
    #2.1 定义一个装饰器函数
    def decorator(func):
        @functools.wraps(func)
        #2.2 定义一个内部函数
        def wrapper(*args,**kwargs):
            #2.3 循环尝试执行原函数，直到成功或者达到最大尝试次数
            for i in range(times):
                try:
                    #2.4 如果成功执行原函数，返回结果；如果失败，捕获异常并打印错误信息
                    return func(*args,**kwargs) # 调用原函数
                except Exception as e:
                    print(f"第 {i+1}/{times} 次尝试失败: {e}")
                    time.sleep(delay) # 等待一段时间后重试
            raise RuntimeError (f"经过 {times} 次尝试，仍然失败") # 如果达到最大尝试次数仍然失败，抛出异常
        return wrapper
    return decorator

# ---- 假 AI 客户端 ----
# 1. 定义一个假 AI 客户端类，模拟 LLM 的流式输出
class FakeAIClient:
    # 1.1 初始化方法，接受一个可选的 name 参数，默认为 "FakeAI"
    def __init__(self,name :str = "FakeAI"):
        self.name = name
    
    # 1.2 定义一个方法，模拟 LLM 的流式输出
    def stream(self,prompt:str)->Iterator[str]:
        """流式生成回复（生成器）"""
        if random.random() < 0.3: # 模拟 30% 的失败率
            raise ConnectionError("API超时")
        response = f"我是{self.name},关于[{prompt}]的回答是：…………假装这是一段很长的回复…………"
        for char in response:
            time.sleep(0.02) # 模拟生成每个字符的时间间隔
            yield char # 使用 yield 关键字返回每个字符，实现流式输出
    
    @timer # 使用 timer 装饰器来记录 chat 方法的执行时间
    @retry(times=3,delay=0.3) # 使用 retry 装饰器来实现 chat 方法的失败重试机制，最多尝试 3 次，每次失败后等待 1 秒钟
    def chat(self,prompt:str)->str:
        """生成回复"""
        chunks=[]
        for c in self.stream(prompt): # 遍历生成器对象，获取每个字符
            chunks.append(c) # 将每个字符添加到 chunks 列表中
            print(c,end="",flush=True) # 打印每个字符，使用 end="" 参数避免换行，使用 flush=True 参数立即刷新输出缓冲区
        return "".join(chunks) # 将 chunks 列表中的字符连接成一个字符串并返回

# 2.测试
if __name__ == "__main__":
    client = FakeAIClient() # 创建一个 FakeAIClient 对象
    client.chat("Python是什么？") # 调用 chat 方法，传入一个提示字符串，获取并打印 AI 的回复
        