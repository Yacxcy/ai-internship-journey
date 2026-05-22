import json

# 1. Python对象转JSON字符串
data = {"name": "Yaai", "skills": ["python", "ai"], "age": 20}
json_str = json.dumps(data,ensure_ascii=False,indent=2) # ensure_ascii=False 参数可以让中文正常显示
print(json_str)

# 2. JSON字符串转Python对象
parse = json.loads(json_str)
print(parse)