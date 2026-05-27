import pandas as pd # pandas 导入模块

df = pd.read_csv("user_log.csv") # 读取CSV文件到DataFrame
print("原始数据shape：", df.shape) # 输出原始数据的行数和列数
print(df.head())    # 输出原始数据的前5行，查看数据的结构和内容
print(df.isna().sum()) # 输出每列缺失值的数量，查看数据的完整性


# 1. 删除 user_id 缺失的行
df = df.dropna(subset = ["user_id"]) # 删除 user_id 列中缺失值所在的行

# 2. duration 缺失填 
df["duration"] = df["duration"].fillna(0) # 将 duration 列中的缺失值填充为0

# 3. value 缺失填该列均值
df["value"] = df["value"].fillna(df["value"].mean())    # 将 value 列中的缺失值填充为该列的均值

# 4. ts 转成 datetime 类型
df["ts"] = pd.to_datetime(df["ts"]) # 将 ts 列转换为 datetime 类型，方便后续的时间处理

# 5. 加一列：日期
df["date"] = df["ts"].dt.date # 从 ts 列中提取日期部分，创建一个新的 date 列

#分析
print("\n=== 每日各操作次数 ===")
print(df.groupby(["date","action"]).size().unstack(fill_value = 0).head(10)) # 按照日期和操作类型分组，计算每组的大小，并使用 unstack 将结果转换为宽格式，缺失值填充为0，输出前10行

print("\n=== 每个用户总价值 ===")
print(df.groupby("user_id")["value"].sum().sort_values(ascending = False)) # 按照 user_id 分组，计算 value 列的总和，并按照总和降序排序，输出结果

print("\n=== buy 行为最多的 3 个用户 ===")
print(df[df["action"]=="buy"]["user_id"].value_counts().head(3)) # 筛选出 action 列为 "buy" 的行，统计 user_id 列的值出现的次数，并输出出现次数最多的前3个用户

# 写出干净版
df.to_csv("clean_log.csv", index = False,encoding = "utf-8")
print("\n清洗后 shape:", df.shape)