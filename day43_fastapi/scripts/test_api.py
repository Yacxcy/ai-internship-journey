import httpx
import json

BASE = "http://127.0.0.1:8000"

#健康检查
print(httpx.get(f"{BASE}/api/health").json())


# 普通对话
r = httpx.post(f"{BASE}/api/chat",json = {"message":"你是谁？","thread_id":"test"},timeout = 60)
print(r.json())

#流式对话
with httpx.stream("POST",f"{BASE}/api/chat/stream",json = {"message":"你是谁？","thread_id":"test"},timeout = 60) as r:
    for line in r.iter_lines():
        if line.startswith("data: "):
            print(line[6:])