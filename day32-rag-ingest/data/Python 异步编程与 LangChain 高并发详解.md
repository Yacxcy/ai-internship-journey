# Python 异步编程与 LangChain 高并发详解

这十个知识点其实是一条完整的学习路线，它们之间是层层递进的关系：

```text
Coroutine（协程）
       ↓
Event Loop（事件循环）
       ↓
Task 对象
       ↓
create_task()
       ↓
asyncio.gather()
       ↓
as_completed()
       ↓
Semaphore
       ↓
invoke() 和 ainvoke()
       ↓
abatch()
       ↓
LangGraph / Agent 高并发
```

------

# 1. invoke() 和 ainvoke() 的区别

这是 LangChain 中最常用的一对方法。

## invoke()

同步调用。

```python
result = llm.invoke("你好")
```

执行流程：

```text
发送请求
↓
等待模型返回
↓
得到结果
↓
继续执行后面的代码
```

一次只能处理一个请求。

例如：

```python
for q in questions:
    llm.invoke(q)
```

实际上：

```text
问题1
↓
等待
↓
问题2
↓
等待
↓
问题3
```

------

## ainvoke()

异步调用。

```python
result = await llm.ainvoke("你好")
```

返回的是协程。

可以多个同时运行：

```python
await asyncio.gather(
    llm.ainvoke("问题1"),
    llm.ainvoke("问题2"),
    llm.ainvoke("问题3")
)
```

执行：

```text
问题1 ─────┐
问题2 ─────├─ 同时进行
问题3 ─────┘
```

------

# 2. 协程（Coroutine）

协程就是：

> 可以暂停、恢复执行的函数。

普通函数：

```python
def foo():
    print("hello")
```

调用：

```python
foo()
```

立即执行。

------

协程：

```python
async def foo():
    print("hello")
```

调用：

```python
foo()
```

得到：

```python
<coroutine object foo>
```

不会运行。

必须：

```python
await foo()
```

才会真正执行。

------

协程类似：

```text
一张待办事项卡片
```

而不是已经开始工作的工人。

------

# 3. Event Loop（事件循环）

事件循环是整个异步程序的大脑。

负责：

- 调度协程
- 管理 Task
- 处理 IO
- 切换任务

例如：

```python
task1
task2
task3
```

事件循环会：

```text
运行 task1 一会
↓
切换 task2
↓
切换 task3
↓
继续 task1
↓
继续 task2
```

不断切换。

------

可以想象成：

- CPU 调度器
- 导演

安排每个演员什么时候出场。

------

启动：

```python
asyncio.run(main())
```

内部：

```text
创建 Event Loop
↓
运行 main()
↓
关闭 Event Loop
```

------

# 4. Task 对象

Task 是：

> 正在被事件循环管理的协程。

协程：

```python
coro = llm.ainvoke("你好")
```

只是：

```text
待办事项
```

Task：

```python
task = asyncio.create_task(coro)
```

变成：

```text
已经交给事件循环处理
```

------

查看类型：

```python
print(type(task))
```

输出：

```python
<class '_asyncio.Task'>
```

------

# 5. create_task()

作用：

> 立即提交任务

例如：

```python
task1 = asyncio.create_task(llm.ainvoke(q1))
task2 = asyncio.create_task(llm.ainvoke(q2))
```

创建后：

任务已经开始执行。

即使：

```python
await task1
```

还没写，

后台已经跑起来了。

------

例如：

```python
async def work():
    await asyncio.sleep(3)
    print("完成")
task = asyncio.create_task(work())

print("继续执行其它代码")
```

不会等待。

3 秒后自动打印：

```text
完成
```

------

# 6. asyncio.gather()

最常见的并发工具。

```python
results = await asyncio.gather(
    task1,
    task2,
    task3
)
```

底层：

### 自动创建 Task

类似：

```python
task1 = create_task(...)
task2 = create_task(...)
task3 = create_task(...)

await task1
await task2
await task3
```

------

特点：

等待全部结束。

返回：

```python
[
    result1,
    result2,
    result3
]
```

按输入顺序排列。

------

# 7. as_completed()

与 gather 不同。

### gather

```text
必须等全部完成
```

------

### as_completed

谁先完成先处理谁。

例如：

```python
tasks = [
    llm.ainvoke(q1),
    llm.ainvoke(q2),
    llm.ainvoke(q3)
]

for task in asyncio.as_completed(tasks):
    result = await task
    print(result.content)
```

假设：

```text
q2 2秒
q1 5秒
q3 7秒
```

输出顺序：

```text
q2
q1
q3
```

而不是：

```text
q1
q2
q3
```

------

适合：

- 流式处理
- 爬虫
- Agent

------

# 8. Semaphore 控制并发数

如果：

```python
1000 个请求
```

同时发：

```python
gather(*tasks)
```

可能：

- API 限流
- 内存爆炸
- 连接池耗尽

所以：

```python
sem = asyncio.Semaphore(5)
```

表示：

### 最多允许 5 个任务同时运行。

```python
async def ask(q):

    async with sem:

        return await llm.ainvoke(q)
```

执行：

```text
5个运行
↓
完成1个
↓
再放进1个
```

类似：

```text
银行只有5个柜台
```

------

# 9. LangChain 的 abatch()

批量异步调用。

不用自己：

```python
gather()
```

直接：

```python
results = await llm.abatch(
    questions
)
```

内部大致：

```python
await asyncio.gather(
    *[
        llm.ainvoke(q)
        for q in questions
    ]
)
```

返回：

```python
[
    AIMessage,
    AIMessage,
    AIMessage
]
```

还能：

```python
await llm.abatch(
    questions,
    config={
        "max_concurrency":3
    }
)
```

自动控制并发。

------

# 10. LangGraph / Agent 高并发

普通：

```text
用户
↓
LLM
↓
结果
```

------

Agent：

```text
用户
↓
LLM
↓
工具调用
↓
LLM
↓
工具调用
↓
结果
```

很多节点。

------

LangGraph：

节点之间可以同时执行。

例如：

```text
          搜索天气
        ↗
用户
        ↘
          搜索新闻
```

两个工具：

同时运行。

然后：

```text
搜索天气
      ↘
        LLM总结
      ↗
搜索新闻
```

------

代码：

```python
StateGraph
```

节点：

```python
weather_node
news_node
stock_node
```

可以：

```text
weather_node ─┐
news_node ────┼── merge
stock_node ───┘
```

真正实现：

### DAG 并行计算

类似：

- Airflow
- Spark
- Ray

------

# 整体关系图

```text
Coroutine
↓
Event Loop
↓
Task
↓
create_task
↓
gather
↓
as_completed
↓
Semaphore
↓
ainvoke
↓
abatch
↓
LangGraph
```

------

# 推荐学习路线

```text
Future
↓
await 底层机制
↓
yield from
↓
async generator
↓
astream()
↓
astream_events()
↓
RunnableParallel
↓
RunnableBranch
↓
LangGraph StateGraph
↓
多 Agent 并行架构
↓
MCP 并发工具调用
↓
生产级异步架构
```

掌握这条路线之后，就能从 Python 异步编程逐步过渡到 LangChain、LangGraph 和生产级 AI Agent 高并发系统开发。