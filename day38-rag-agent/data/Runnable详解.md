# Runnable、RunnablePassthrough、RunnableLambda、RunnableParallel 详解

这是 LangChain 初学者最容易迷惑的问题之一。

其实只要理解 **Runnable 的本质**，另外三个类：

- `RunnablePassthrough`
- `RunnableLambda`
- `RunnableParallel`

就非常容易理解。

------

# 一、什么是 Runnable？

先不要看 LangChain。

看普通 Python：

```python
x = 10

y = x + 1

z = y * 2
```

执行流程：

```text
10
↓
+1
↓
11
↓
×2
↓
22
```

这里：

```python
+1
×2
```

其实都是“处理输入得到输出”的过程。

LangChain 把这种：

> 输入 → 处理 → 输出

统一抽象成：

# Runnable

即：

```text
Input
↓
Runnable
↓
Output
```

------

例如：

### Prompt

```python
prompt = ChatPromptTemplate.from_template(
    "解释 {term}"
)
```

输入：

```python
{
    "term":"RAG"
}
```

输出：

```python
HumanMessage(...)
```

因此：

```python
prompt
```

就是 Runnable。

------

### LLM

```python
llm
```

输入：

```python
HumanMessage
```

输出：

```python
AIMessage
```

所以：

```python
llm
```

也是 Runnable。

------

### Parser

```python
StrOutputParser()
```

输入：

```python
AIMessage
```

输出：

```python
str
```

因此：

```python
StrOutputParser()
```

也是 Runnable。

------

所以：

```python
prompt | llm | parser
```

实际上：

```text
dict
↓
Runnable
↓
HumanMessage

↓
Runnable
↓
AIMessage

↓
Runnable
↓
str
```

因此：

> Runnable = 一个能够接受输入并产生输出的节点。

------

# Runnable 的统一接口

所有 Runnable 都支持：

```python
invoke()
batch()
stream()
ainvoke()
abatch()
```

例如：

### Prompt

```python
prompt.invoke()
```

### LLM

```python
llm.invoke()
```

### Parser

```python
parser.invoke()
```

### 整个 Chain

```python
chain.invoke()
```

都能调用。

因为它们本质上都是 Runnable。

------

# 二、RunnablePassthrough 是什么？

名字：

```python
Passthrough
```

意思：

> 原样通过

相当于：

```python
lambda x:x
```

------

例如：

```python
RunnablePassthrough().invoke("hello")
```

输出：

```python
"hello"
```

什么都不做。

------

流程：

```text
hello
 ↓
Passthrough
 ↓
hello
```

------

最常见用途：

保存原始输入。

例如：

```python
{
    "text": RunnablePassthrough()
}
```

输入：

```python
"hello"
```

输出：

```python
{
    "text":"hello"
}
```

相当于：

```python
lambda x:{
    "text":x
}
```

------

### assign()

更常用：

```python
RunnablePassthrough.assign(
    chinese=translate_chain
)
```

原来：

```python
{
"text":"hello"
}
```

新增：

```python
"chinese":"你好"
```

得到：

```python
{
"text":"hello",
"chinese":"你好"
}
```

类似：

```python
dict.update()
```

------

# 三、RunnableLambda 是什么？

作用：

> 把普通 Python 函数包装成 Runnable。

例如：

普通函数：

```python
lambda x:{
    "text":x
}
```

不能：

```python
lambda x:{
"text":x
} | llm
```

会报错。

因为：

```python
lambda
```

不是 Runnable。

------

包装：

```python
RunnableLambda(
    lambda x:{
        "text":x
    }
)
```

以后：

```python
RunnableLambda(...)
| llm
```

就可以了。

------

流程：

```text
输入
 ↓

普通函数

 ↓

输出
```

变成：

```text
输入
 ↓

RunnableLambda

 ↓

输出
```

------

例如：

```python
chain = (
    translate
    |
    RunnableLambda(
        lambda x:{
            "text":x
        }
    )
    |
    summarize
)
```

翻译得到：

```python
"你好"
```

经过：

```python
RunnableLambda
```

变成：

```python
{
"text":"你好"
}
```

再给：

```python
summarize
```

使用。

------

所以：

### RunnableLambda = Runnable 化的 Python 函数。

------

# 四、RunnableParallel 是什么？

作用：

> 多条链同时执行。

例如：

有三个任务：

### 翻译

```python
translate_chain
```

### 总结

```python
summarize_chain
```

### 情感分析

```python
sentiment_chain
```

它们都需要：

```python
{text}
```

作为输入。

------

串行：

```text
翻译
↓
总结
↓
情感分析
```

耗时：

```text
T1+T2+T3
```

------

并行：

```text
          输入
            │
      ┌─────┼─────┐
      ▼     ▼     ▼

   翻译   总结   情感分析

      ▼     ▼     ▼

      └─────┼─────┘
            ▼

         合并结果
```

耗时：

```text
max(T1,T2,T3)
```

------

例如：

```python
parallel = RunnableParallel(
    translation=translate_chain,
    summary=summarize_chain,
    sentiment=sentiment_chain
)
```

输出：

```python
{
"translation":"...",
"summary":"...",
"sentiment":"positive"
}
```

------

# 五、三者关系

### RunnablePassthrough

#### 什么都不做

```text
x
↓
x
```

相当于：

```python
lambda x:x
```

主要用途：

- 保存输入
- assign 增加字段

------

### RunnableLambda

#### 自定义处理

```text
x
↓
自定义函数
↓
y
```

相当于：

```python
def func(x):
    ...
```

但可以参与 LCEL。

------

### RunnableParallel

#### 一分多路

```text
        x
        │
 ┌──────┼──────┐
 ▼      ▼      ▼

A      B      C

 └──────┼──────┘
        ▼

     dict
```

负责：

多任务并发。

------

# 六、最形象的理解

把整个 LangChain 看成工厂流水线。

### Runnable

就是：

> 一个加工站。

------

### RunnablePassthrough

像：

```text
传送带
```

什么也不加工。

只是运送。

------

### RunnableLambda

像：

```text
人工加工站
```

你自己写规则。

------

### RunnableParallel

像：

```text
分拣中心
```

同时送到：

- A车间
- B车间
- C车间

最后汇总。

------

# 七、总结

| 类                  | 本质             | 类比       |
| ------------------- | ---------------- | ---------- |
| Runnable            | 输入→输出节点    | 工位       |
| RunnablePassthrough | 原样返回         | 传送带     |
| RunnableLambda      | 包装 Python 函数 | 人工加工站 |
| RunnableParallel    | 多路并发执行     | 分拣中心   |
| Prompt              | Runnable         | 工位       |
| LLM                 | Runnable         | 工位       |
| Parser              | Runnable         | 工位       |
| Chain               | Runnable         | 整条流水线 |

------

所以：

```python
prompt | llm | parser
```

其实就是：

```text
工位
↓
工位
↓
工位
```

而：

```python
RunnableParallel
```

是：

```text
           工位
             │
      ┌──────┼──────┐
      ▼      ▼      ▼
    工位    工位    工位
      └──────┼──────┘
             ▼
```

------

# 最终一句话

> Runnable 是 LangChain 中最核心的抽象，表示一个“输入 → 输出”的处理节点；RunnablePassthrough 用于原样传递数据，RunnableLambda 用于包装自定义 Python 函数，RunnableParallel 用于多任务并发执行，它们共同构成了 LCEL（LangChain Expression Language）流水线，也是 LangGraph StateGraph 的基础。