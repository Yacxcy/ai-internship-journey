import streamlit as st
from agent import run

st.set_page_config(page_title = "RAG-Agent 助手",page_icon = "🤖",layout = "centered")
st.title("🤖 RAG-Agent 综合助手")
st.caption("能查私有知识库、搜索互联网、做数学")

if "history" not in st.session_state:
    st.session_state.history = []

#渲染
for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])


#输入
if user_input := st.chat_input("说点什么..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.history.append({"role":"user","content":user_input})

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            result = run(user_input)
        answer = result["output"]
        st.markdown(answer)
        st.session_state.history.append({"role":"assistant","content":answer})