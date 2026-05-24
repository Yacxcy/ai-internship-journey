import os # 导入os模块，用于访问环境变量
import streamlit as st # 导入streamlit模块，用于创建Web应用
from openai import OpenAI # 导入OpenAI模块，用于访问OpenAI API
from dotenv import load_dotenv # 导入dotenv模块，用于加载环境变量
import tiktoken # 导入tiktoken模块，用于计算消息的token数量
import json # 导入json模块，用于处理JSON数据

load_dotenv() # 加载环境变量

 #加 Token 用量显示
enc = tiktoken.get_encoding("cl100k_base") # 获取模型对应的编码器
def count_tokens(messages): # 定义一个函数来计算消息的token数量
    return sum(len(enc.encode(m["content"])) + 4 for m in messages) + 2 # 计算所有消息内容的token数量总和

# 增加角色预设
PRESETS = {
    "默认助手": "你是一个友好的 AI 助手，回答简洁有用。",
    "Python 老师": "你是 Python 老师，用初学者能懂的方式回答，多举例子。",
    "面试官": "你是技术面试官，用追问的方式让对方深入思考。",
    "翻译": "你是专业翻译，只输出翻译结果，不解释。",
}

# ---- 页面配置 ----
st.set_page_config(page_title  ="My AI Chat",page_icon = "🤖",layout = "centered")  # 页面配置
st.title("🤖 我的 AI 助手")
st.caption("Day 7 · 基于 DeepSeek API · Powered by Streamlit")

# ---- 侧边栏 ----
with st.sidebar:
    st.header("⚙️ 设置") # 侧边栏标题
    system_prompt = st.text_area(
        "System Prompt", # 系统提示语
        value = "你是一个友好的 AI 助手，回答简洁有用。", # 默认值
        height = 100, # 输入框高度
    )
    temperature = st.slider("Temperature",0.0,2.0,0.7,0.1) #随机程度,滑动条
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = [{"role":"system","content":system_prompt}] # 重置对话上下文
        st.rerun() # 重新运行应用

    # ---- 计算消息的token数量 ----
    if  "messages" in st.session_state:#只有 messages 已经存在，才统计 token。此时messages还没初始化，需要先判断一下
        st.metric("当前对话 Token", count_tokens(st.session_state.messages)) #只有 messages 已经存在，才统计 token。此时messages
    
    #加导出对话功能
    if st.button("💾 导出对话"):
         data = json.dumps(st.session_state.messages, ensure_ascii=False, indent=2) # 将对话历史转换为JSON格式字符串
         st.download_button(
             "下载 JSON", # 按钮文本
            data = data, # 下载数据
            file_name="chat_history.json", # 下载文件名
             mime="application/json", # MIME类型
         )
    
    # 增加角色预设功能
    preset = st.selectbox("选择角色预设", options=list(PRESETS.keys())) # 角色预设选择框
    if st.button("应用预设"):
        st.session_state.messages = [{"role":"system","content":PRESETS[preset]}] # 应用选定的角色预设
        st.rerun() # 重新运行应用

# ---- 初始化历史 ----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"system","content":system_prompt}] # 初始化对话上下文

# ---- 渲染历史 ----
for msg in st.session_state.messages:  #根据历史记录里的角色，自动决定放进用户框还是 AI 框
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]): # 根据消息角色创建聊天消息组件
        st.write(msg["content"]) # 显示消息内容

# ---- 输入框 ----
if user_input:= st.chat_input("说点什么..."):
    # 显示用户消息
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):  # 这段是在用户刚输入内容后，立刻把用户消息显示到页面上。
        st.write(user_input) 

    # 调用 LLM 流式输出
    client = OpenAI(
        api_key = os.getenv("DEEPSEEK_API_KEY"), # 从环境变量中获取API key
        base_url = os.getenv("DEEPSEEK_BASE_URL"), # 从环境变量中
    )

    with st.chat_message("assistant"): # 创建一个助手消息组件
        placeholder = st.empty() # 创建一个占位符，用于显示模型回复
        full = ""  # 初始化回复内容
        # 注意：每次请求要把 system 用最新的 sidebar 内容
        msg_to_send =[{"role":"system","content":system_prompt}]+[
            m for m in st.session_state.messages if m["role"] != "system"] # 构建消息列表，包含最新的系统提示和历史消息
        try:
            stream = client.chat.completions.create(
                model = "deepseek-v4-pro", # 模型名称
                messages = msg_to_send, # 消息列表作为参数传递给模型
                temperature = temperature, # 随机程度参数
                stream = True, # 启用流式输出
            )
            for chunk in stream: # 迭代处理流式输出的每个块
                delta = chunk.choices[0].delta.content # 获取当前块的内容增量
                if delta:
                    full += delta # 将增量添加到完整回复中
                    placeholder.markdown(full+"▌")   # 在占位符中显示当前回复内容，并添加光标
                placeholder.markdown(full) # 最后在占位符中显示完整回复
        except Exception as e:
            full = f"出错了: {e}"
            placeholder.markdown(full) # 显示错误信息
    # 将助手回复添加到对话历史中
    st.session_state.messages.append({"role":"assistant","content":full}) 
