import pandas as pd # pandas 导入模块

# 1. 创建
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "David"],
    "age": [25, 30, 35, 28],
    "city": ["Beijing", "Shanghai", "Beijing", "Hangzhou"],
    "salary": [15000, 25000, 30000, 18000],
})
print(df) # 输出DataFrame
print("-"*20)

# 2. 筛选
print(df[df["age"]>28]) # 筛选年龄大于28岁的行
print(df[df["city"].isin(["Beijing", "Shanghai"])]) # 筛选城市在北京和上海的行
print("-"*20)

# 3. 排序
print(df.sort_values("salary", ascending = False)) # 按照薪水降序排序 ascending = True 升序
print("-"*20)

# 4. 分组聚合
print(df.groupby("city")["salary"].agg(["mean", "max", "count"])) # 按照城市分组，计算薪水的均值和总和
print("-"*20)

# 5. 新增列
df["tax"] = df["salary"] *0.1 # 计算税金，假设税率为10%
print(df) # 输出更新后的DataFrame

# 6. 写出
df.to_csv("output.csv",index = False,encoding = "utf-8") # 将DataFrame写出到CSV文件,使用UTF-8编码,index = False 不写出索引
print("-"*20)

