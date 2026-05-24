import streamlit as st 

# 设置页面标题
st.title("我的第一个 Streamlit 应用")
# 显示文本
st.write("Hello, AI World!")

# 获取用户输入
name = st.text_input("你叫什么名字？")

if name:
    st.success(f"你好{name}!")

if st.button("点我"):
    st.balloons() # 显示气球动画