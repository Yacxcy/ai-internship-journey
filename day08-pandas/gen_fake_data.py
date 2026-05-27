import pandas as pd  # pandas 导入模块
import random # 导入随机数模块
from datetime import datetime, timedelta # 导入日期时间模块

random.seed(42) # 设置随机数种子，保证每次生成的数据相同
rows = [] # 创建一个空列表，用于存储生成的数据行
users=  ["u001", "u002", "u003", "u004", "u005", None] # 用户ID列表，包含一个None值表示缺失数据
actions = ["login", "view", "click", "buy", "logout"]   # 用户行为列表

start = datetime(2026,1,1) # 定义起始日期
for i in range(200): # 生成200行数据
    rows.append({
        "ts" : (start+timedelta(minutes = random.randint(0,30*24*60))).isoformat(),
        "user_id": random.choice(users), # 随机选择一个用户ID
        "action": random.choice(actions) ,# 随机选择一个用户行为
        "duration":random.choice([random.randint(1,300),None]), # 随机生成一个持续时间，或者None表示缺失数据
        "value": random.choice([round(random.uniform(0,1000),2),None]) # 随机生成一个数值，或者None表示缺失数据
    })

pd.DataFrame(rows).to_csv("user_log.csv",index = False,encoding = "utf-8") # 将生成的数据写出到CSV文件，使用UTF-8编码，不写出索引
print("数据生成完毕")