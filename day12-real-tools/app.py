import streamlit as st
from agent import chat

st.set_page_config(page_title="带工具的 AI 助手", page_icon="🛠️")  #设置浏览器标签页
st.title("🛠️ 带工具的 AI 助手")#显示大标题
st.caption("能查天气、能搜索互联网") #显示副标题

# 初始化聊天历史记录
if "history" not in st.session_state: # 判断session_state中是否有history这个键
    st.session_state.history = [] # 如果没有，就初始化为一个空列表

# 渲染历史
for m in st.session_state.history: 
    if m["role"] in ("user","assistant"): # 如果消息角色是用户或助手，就显示消息内容
        with st.chat_message(m["role"]): # 使用st.chat_message组件来显示聊天消息，参数是消息的角色（用户或助手）
            st.markdown(m["content"] or "") # 显示消息内容，如果内容为空，就显示空字符串

# 获取用户输入
if user_input :=st.chat_input("问点啥..."):
    with st.chat_message("user"):
        st.markdown(user_input) # 显示用户输入的消息
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."): # 显示一个加载动画，提示用户等待
            answer, new_history = chat(user_input,st.session_state.history) # 调用chat函数，传入用户输入和历史记录，获取模型的回复和更新后的历史记录
            # 更新 session_state 中的历史记录，只保留用户、助手和系统消息，过滤掉工具调用的消息
            st.session_state.history = new_history
        st.markdown(answer) # 显示模型的回复
