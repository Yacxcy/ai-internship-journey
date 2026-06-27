import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import uuid
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from app.agent.graph import app_graph

st.set_page_config(page_title = "面试 Coach（AI 模拟面试官）",page_icon = "🤖",layout = "wide")
st.title("🤖 面试 Coach（AI 模拟面试官）")
st.caption("基于 LangGraph + RAG + 多工具调度")

#Session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]
if "messages" not in st.session_state:
    st.session_state.messages = []

#Sidebar
with st.sidebar:
    st.header("⚙️ 设置")
    st.text(f"Thread :{st.session_state.thread_id}")
    if st.button("🔄 新对话"):
        st.session_state.thread_id = str(uuid.uuid4())[:8]
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**示例问题**")
    examples = [
        "我们公司报销流程？",
        "2026 年最新 LLM 排行榜",
        "年终奖按 1.5 个月算，月薪 18000 共多少",
    ]
    for ex in examples:
        if st.button(ex,key = ex):
            st.session_state._pending_input = ex
            st.rerun()

#主区域
col_chat,col_refs = st.columns([3,2])

with col_chat:
    st.subheader("💬 对话")
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

#输入
user_input = st.chat_input("说点什么...")
if not user_input and st.session_state.get("_pending_input"):
    user_input = st.session_state._pending_input
    st.session_state._pending_input = None

if user_input:
    with col_chat:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role":"user","content":user_input})

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""
            with st.spinner("思考中..."):
                config = {"configurable":{"thread_id":st.session_state.thread_id}}
                tool_calls_in_run = []
                tool_results = []
                for chunk in app_graph.stream(
                    {"messages":[HumanMessage(content = user_input)]},
                    config = config,
                    stream_mode = "values",
                ):
                    last_msg = chunk["messages"][-1]
                    # 收集 tool_calls（可能在 AIMessage 上）
                    if hasattr(last_msg,"tool_calls") and last_msg.tool_calls:
                        tool_calls_in_run.extend(last_msg.tool_calls)
                    # 收集 tool_results（可能在 ToolMessage 上）
                    if isinstance(last_msg,ToolMessage):
                        tool_results.append(
                            {
                                "name":"tool_result",
                                "content":last_msg.content,
                            }
                        )
                    # 流式更新最终回答
                    if hasattr(last_msg,"content") and last_msg.content:
                        full = last_msg.content
                        placeholder.markdown(full+"▌")
                # 最终输出
                placeholder.markdown(full)

                # 保存本轮对话和工具调用结果到 session_state
                st.session_state.last_tool_calls = tool_calls_in_run
                st.session_state.last_tool_results = tool_results
        st.session_state.messages.append({"role":"assistant","content":full})
    st.rerun()

with col_refs:
    st.subheader("🔍 工具调用 / 引用")
    if "last_tool_calls" in st.session_state and st.session_state.last_tool_calls:
        for tc in st.session_state.last_tool_calls:
            with st.expander(f"🔧 {tc['name']}"):
                st.json(tc.get("args",{}))
        for tr in st.session_state.last_tool_results:
            with st.expander(f"📄 {tr['name']}"):
                st.markdown(tr["content"][:1500]) # 长文本截断
    else:
        st.info("提问后这里会显示工具调用过程")