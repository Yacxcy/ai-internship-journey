#LLM 流式输出本质就是生成器

#1. 创建一个生成器函数
def fake_llm_stream(prompt:str):
    """模拟 LLM 的流式输出"""
    response = f"对你的问题[{prompt}]，我的回答是：这是一个分块返回的服务"
    #循环遍历响应字符串中的每个字符，并使用 yield 关键字返回它们
    for char in response:
        yield char # 返回一个字符

#2.测试
for chunk in fake_llm_stream("python是什么"):
    print(chunk,end="",flush= True)
print()