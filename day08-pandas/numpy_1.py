import numpy as np # 导入numpy库，并使用别名np

# 1. 创建
a = np.array([1, 2, 3, 4, 5]) # 创建一维数组
print(a.shape,a.dtype) # 输出数组的形状和数据类型

print("-"*20)

# 2. 创建二维
b = np.zeros((2,3)) # 创建一个2行3列的全零数组
print(b)

print("-"*20)

# 3. 广播
a = np.array([1, 2, 3]) # 创建一维数组
b = np.array([[10], [20], [30]]) # 创建一个3行1列的二维数组
print(a+b) # 使用广播规则，将a和b相加

print("-"*20)

# 4. 索引切片
arr = np.arange(20).reshape(4,5) # 创建一个4行5列的数组
print(arr[1:3, 2:4]) # 切片获取第2-3行，第3-4列的子数组

print("-"*20)
# 5. 聚合
print(arr.sum(), arr.mean(), arr.max(axis=0)) # 计算数组的总和、平均值和每列的最大值