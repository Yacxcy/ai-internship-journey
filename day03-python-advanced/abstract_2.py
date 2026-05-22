from abc import ABC, abstractmethod

#抽象类：不能被实例化的类，通常用来定义接口和规范，子类必须实现抽象类中的抽象方法
class LLMProvider(ABC):
    @abstractmethod #抽象方法
    #抽象方法没有具体的实现，子类必须重写这个方法，否则子类也会成为抽象类，无法实例化
    def chat(self,prompt:str):
        pass

class DeepSeekProvider(LLMProvider):
    #重写抽象方法，提供具体的实现
    def chat(self, prompt: str):
        return f"[Deepseek 回复]: {prompt}"

class QwenProvider(LLMProvider):
    def chat(self,prompt:str):
        return f"[Qwen 回复]: {prompt}"

#测试
if __name__ == "__main__":
    for p in [DeepSeekProvider(),QwenProvider()]: #创建 DeepSeekProvider 和 QwenProvider 的实例，并将它们放在一个列表中进行迭代
        print(p.chat("你好，世界！"))