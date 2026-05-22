from dataclasses import dataclass, field # 导入 dataclass 和 field 函数
from typing import List # 导入 List 类型提示

# 定义一个 Message 类,它包含 role、content、tokens 和 metadata 四个字段,其中 tokens 的默认值为 0,metadata 的默认值为一个空字典
@dataclass  # 使用 dataclass 装饰器定义一个数据类,它会自动生成 __init__、__repr__ 等方法
class Message:
    role:str
    content:str
    tokens:int = 0
    metadata:dict = field(default_factory=dict) # 使用 field 函数为 metadata 字段设置默认值为一个空字典

# 定义一个 Conversion 类,它包含一个 user 字段和一个 message 字段,其中 message 是一个 Message 对象的列表
@dataclass  # 使用 dataclass 装饰器定义一个数据类,它会自动生成 __init__、__repr__ 等方法
class Conversion:
    user :str
    message : List[Message]= field(default_factory=list) # 使用 field 函数为 message 字段设置默认值为一个空列表
    # 添加消息的方法,它接受角色和内容作为参数，并将它们封装成一个 Message 对象添加到 message 列表中
    def add(self,role:str,content:str):
        self.message.append(Message(role,content)) # 向 message 列表中添加一个新的 Message 对象 

#测试
if __name__ == "__main__":
    c = Conversion(user = "Ya") # 创建一个 Conversion 对象,并指定 user 字段的值为 "Ya"
    c.add("user","你好") # 调用 add 方法添加一条消息,角色为 "user",内容为 "你好"
    c.add("assistant","你好！有什么可以帮助你的吗？") # 调用 add 方法添加一条消息,角色为 "assistant",内容为 "你好！有什么可以帮助你的吗？"
    print(c) # 打印 Conversion 对象,它会自动调用 __repr__ 方法显示对象的内容