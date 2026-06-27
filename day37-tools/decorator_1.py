from langchain_core.tools import tool

@tool
def get_word_length(word:str)->int:
    """返回单词的长度。
    参数 word: 任意字符串
    """
    return len(word)

#调用
print(get_word_length.name)  # 输出工具名称
print(get_word_length.description) # 输出工具描述
print(get_word_length.args) # 输出工具参数
print(get_word_length.invoke({"word":"hello"})) # 输出工具调用结果