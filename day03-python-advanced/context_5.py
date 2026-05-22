from contextlib import contextmanager
import time

# 1. 定义一个上下文管理器
@contextmanager
def time_block(name :str ):
    """一个上下文管理器，用来记录代码块的执行时间"""
    start = time.time() # 记录开始时间
    yield # 暂停执行，等待代码块执行完成
    print(f"[{name}]耗时{time.time() - start:.3f}")

# 2.测试
with time_block("数据加载"): # 使用 time_block 上下文管理器来记录数据加载的时间
    time.sleep(1) # 模拟数据加载的操作，暂停 1 秒钟
    print("loading.......")