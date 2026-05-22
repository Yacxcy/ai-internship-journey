import time
import functools

# 1.定义一个记时装饰器，用来记录时间
def timer(func):
    # 1.1函数的元信息
    @functools.wraps(func) # 
    # 1.2 定义一个内部函数
    def wrapper(*args,**kwargs):
        # 1.3 记录开始时
        start = time.time()
        #1.4 计算使用时间
        elapsed = time.time() - start
        # 1.5 打印结果
        print(f"{func.__name__} 耗时: {elapsed:.3f}s")
        # 1.6 返回结果,引用原函数
        return func(*args,**kwargs)
    return wrapper

# 2.定义一个函数，模拟失败重试操作
def retry(times: int = 3):
    # 2.1 定义一个装饰器函数
    def decorator(func):
        
        @functools.wraps(func)
        # 2.2 定义一个内部函数
        def wrapper(*args,**kwargs):
            # 2.3 循环尝试执行原函数，直到成功或者达到最大尝试次数
            for i in range(times):
                # 2.4 如果成功执行原函数，返回结果；如果失败，捕获异常并打印错误信息
                try:
                    return func(*args,**kwargs) # 调用原函数
                except Exception as e:
                    print(f"第 {i+1} 次尝试失败: {e}")
            raise Exception(f"经过 {times} 次尝试，仍然失败") # 如果达到最大尝试次数仍然失败，抛出异常
        return wrapper
    return decorator

#3.测试
if __name__ == "__main__":
    # 3.1 定义一个函数，模拟从网络获取数据的操作，可能会失败
    @timer
    # 使用 timer 装饰器来记录 fetch_data 函数的执行时间
    @retry(times=3)
    # 使用 retry 装饰器来实现 fetch_data 函数的失败重试机制，最多尝试 3 次
    def fetch_data(url :str):
        import random
        if random.random() < 0.7:
            raise ConnectionError("网络抖动")
        return f"data from {url}"
print(fetch_data("https://example.com"))