class DivisionByZeroError(Exception):
    pass

class Calculator:
    def __init__(self,value):
        self._value = value

    ## 加法
    def add(self,value):
        self._value += value
        return self

    ## 减法
    def subtract(self,value):
        self._value -= value
        return self

    ## 乘法
    def multiply(self,value):
        self._value *= value
        return self

    ## 除法
    def divide(self,value):
        if value == 0:
            raise DivisionByZeroError("除数不能为零")
        self._value /= value
        return self
    
    ## 获取结果
    def __str__(self):
        return f"计算结果是：{self._value}"

if __name__ == "__main__":
    c = Calculator(10).add(5).subtract(3).multiply(2).divide(2)
    print(c)
