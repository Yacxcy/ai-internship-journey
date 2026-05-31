import streamlit as st
import tiktoken
from agent import chat
from presets import PRESETS

st.set_page_config(page_title="AI 助手 v2", page_icon="🚀", layout="wide")
st.title("🚀 AI 助手 v2 (Day 13)")
st.caption("Streamlit + Function Calling + 结构化输出 + 多角色")

enc = tiktoken.get_encoding("cl100k_base")
def count_tokens(messages):
    return sum(len(enc.encode(str(m.get("content") or "")))+4 for m in messages) + 2

# 侧边栏
with st.sidebar:
    st.header("⚙️ 配置")
    role = st.selectbox("角色",list(PRESETS.keys()))
    if "current_role" not in st.session_state or st.session_state.current_role != role:
        st.session_state.current_role = role
        st.session_state.history = [{"role":"system","content": PRESETS[role]}] # 切换角色时重置历史记录

    st.divider()
    st.metric("Token",count_tokens(st.session_state.get("history", []))) # 显示当前对话的 Token 数量

    if st.button("🗑️ 清空"):
        st.session_state.history = [{"role":"system","content": PRESETS[role]}] # 清空历史记录，但保留当前角色的系统提示

# 初始化历史
if "history" not in st.session_state:
    st.session_state.history = [{"role":"system","content": PRESETS[role]}] # 初始化历史记录，包含系统提示

for m in st.session_state.history:
    if m["role"] in ("user","assistant") and m.get("content"):
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

#输入
if user_input := st.chat_input("说点什么..."):
    with st.chat_message("user"):
        st.markdown(user_input)
        with st.chat_message("assistant"):
            st.spinner("思考中...")
            answer,new_history = chat(user_input,st.session_state.history)
            st.session_state.history = new_history
        st.markdown(answer)
    