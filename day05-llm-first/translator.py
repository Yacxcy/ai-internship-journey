from llm_client import LLMClient # 从llm_client模块导入LLMClient类

# 创建一个LLMClient实例，设置默认的系统消息
llm = LLMClient(default_system="你是专业翻译。只输出翻译结果，不要解释。")


def translate(text:str, target:str) -> str: # 定义一个函数，接收待翻译的文本和目标语言，返回翻译结果
    return llm.chat(f"请将以下文本翻译成{target}：\n{text}") # 调用LLMClient的chat方法，传入翻译提示和参数，返回翻译结果


# 测试翻译功能
if __name__ == "__main__":
    print(translate("装饰器是 Python 中一种修改函数行为的语法糖",target = "英文"))
    print(translate("Hello, my name is Yaai. I'm learning AI.", target="中文"))