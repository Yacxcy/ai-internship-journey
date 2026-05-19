nums = [1,2,3,4,5]
print([n * 2 for n in nums if n % 2 == 0]) ## 如果n是偶数，则返回n的2倍

scores = {"Alice": 90, "Bob": 85}
for name ,score in scores.items():
    print(f"{name}: {score}") ## 打印名字和分数