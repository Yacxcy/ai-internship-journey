import requests

#1.GET请求
r = requests.get("https://api.github.com")
print(r.status_code) # 状态码
print(r.headers["content-type"]) # 响应头
print(r.json) # 响应体
print("-"*50)

#2.带查询参数
r = requests.get("https://api.github.com/search/repositories", params={"q": "langchain", "per_page": 3})
for repo in r.json()["items"]: # 遍历返回的仓库列表
    print(repo["full_name"], repo["stargazers_count"])  # 打印仓库全名和星标数量
print("-"*50)

#3. POST请求+JSON Body
r = requests.post("https://httpbin.org/post",
                  json={"hello": "world"},
                  headers={"User-Agent": "Yaai-Learning/1.0"})
print(r.json)
print("-"*50)

#4.超时与异常
try:
    r = requests.get("https://httpbin.org/delay/5",timeout = 2) # 设置超时时间为2秒
except requests.Timeout: # 捕获超时异常
    print("请求超时了！")
except requests.RequestException as e:
    print(f"请求发生错误：{e}") # 捕获其他请求异常