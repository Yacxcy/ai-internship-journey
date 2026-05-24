import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---- 页面配置 ----
st.set_page_config(page_title="My AI Chat", page_icon="🤖", layout="centered")
st.title("🤖 我的 AI 助手")
st.caption("Day 7 · 基于 DeepSeek API · Powered by Streamlit")

# ---- 侧边栏 ----
with st.sidebar:
    st.header("⚙️ 设置")
    system_prompt = st.text_area(
        "System Prompt",
        value="你是一个友好的 AI 助手，回答简洁有用。",
        height=100,
    )
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        st.rerun()

# ---- 初始化历史 ----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# ---- 渲染历史 ----
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- 输入框 ----
if user_input := st.chat_input("说点什么..."):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
    )

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full = ""
        # 注意：每次请求要把 system 用最新的 sidebar 内容
        msgs_to_send = [{"role": "system", "content": system_prompt}] + [
            m for m in st.session_state.messages if m["role"] != "system"
        ]
        try:
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=msgs_to_send,
                temperature=temperature,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    full += delta
                    placeholder.markdown(full + "▌")
            placeholder.markdown(full)
        except Exception as e:
            full = f"出错了: {e}"
            placeholder.error(full)

    st.session_state.messages.append({"role": "assistant", "content": full})