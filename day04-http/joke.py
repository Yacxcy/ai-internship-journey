import requests

r = requests.get("https://v2.jokeapi.dev/joke/Any?lang=en",timeout = 5)
data = r.json() # 打印笑话内容

if data["type"] == "single": # 如果是单段笑话
    print(data["joke"])
else: # 如果是两段笑话
    print(data["setup"])
    print(data["delivery"]) 
