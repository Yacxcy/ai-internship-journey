## 定义一个“余额不足”的异常：
class InsufficientFunds(Exception):
    pass

## 定义一个取款函数
def withdraw(amount,balance):
    if amount > balance:
        raise InsufficientFunds("余额不足，无法取款！")
    else:
        return balance - amount

try:
    new_balance = withdraw(100,200)
except InsufficientFunds as e:
    print(f"操作失败：{e}")
finally:
    print("交易记录已落库")