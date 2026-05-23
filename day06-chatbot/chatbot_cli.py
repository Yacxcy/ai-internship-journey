import os # 导入os模块，用于访问环境变量
import json # 导入json模块，用于处理JSON数据
from datetime import datetime # 导入datetime模块，用于处理日期和时间
from typing import List, Dict # 导入typing模块中的List和Dict类型提示
from openai import OpenAI # 导入OpenAI模块，用于访问OpenAI API
from dotenv import load_dotenv

load_dotenv() # 加载环境变量

#支持多轮对话、流式输出、清空历史、保存历史、查看历史的命令行聊天机器人。

class Chatbot:
    # 初始化方法
    def __init__(
            self,
            system:str = "你是一个有用的 AI 助手，回答简洁明了。",
            model:str = "deepseek-v4-pro",
            max_pairs : int = 10,
    ):
        self.client = OpenAI(
            api_key = os.getenv("DEEPSEEK_API_KEY"),
            base_url = os.getenv("DEEPSEEK_BASE_URL"),
        )
        self.model = model # 模型名称 
        self.system = system # 系统消息
        self.max_pairs = max_pairs # 最大对话对数
        self.messages:List[dict[str,str]] =[{"role":"system","content":system}] # 消息列表，初始包含系统消息

    # 限制对话数量
    def _truncate(self):
        system = [m for m in self.messages if m["role"] == "system"] # 提取系统消息
        others = [m for m in self.messages if m["role"] != "system"] # 提取非系统消息
        self.messages = system + others[-self.max_pairs*2:] # 保留系统消息
    
    # 发送消息并获取回复,流式输出
    def chat(self, user_input:str)->str:
        self.messages.append({"role":"user","content":user_input})
        self._truncate() # 限制对话数量

        # 创建流式输出的聊天完成对象
        stream = self.client.chat.completions.create(
            model = self.model,
            messages = self.messages,
            stream = True,
        )
        print("Bot:",end = "",flush = True)
        replay = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta,end = "",flush = True)
                replay += delta
        print() # 换行
        self.messages.append({"role":"assistant","content":replay}) # 添加回复到消息列表
        return replay
    # 清空历史
    def clear(self):
        self.messages = [{"role":"system","content":self.system}]
        print("历史已清空。")
    
    # 保存历史
    def save(self,path:str = None):
        path = path or f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(path,"w",encoding="utf-8") as f:
            json.dump(self.messages,f,ensure_ascii=False,indent=2)  # 保存为JSON文件
        print(f"[已保存到{path}]")

    # 查看历史
    def show_history(self):
        print(f"---共{len(self.messages)}条消息---")
        for m in self.messages:
            print(f"[{m['role']}]{m['content'][:60]}...") # 只显示前60个字符

def main():
    bot = Chatbot()
    print("欢迎使用 AI 助手！")
    print("可用指令: /clear 清空 | /save 保存 | /history 看历史 | /quit 退出")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input == "/quit":
                break
            elif user_input == "/clear":
                bot.clear()
            elif user_input == "/save":
                bot.save()
            elif user_input == "/history":
                bot.show_history()
            else:
                bot.chat(user_input)
        except KeyboardInterrupt:
            print("\n[Ctrl+C 退出]")
            break
        except Exception as e:
            print(f"\n[出错了] {e}")


#测试
if __name__ == "__main__":
    main()

        