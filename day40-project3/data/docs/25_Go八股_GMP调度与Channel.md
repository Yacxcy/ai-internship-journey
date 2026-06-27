# Go 八股 — GMP调度、Channel、defer、并发安全

---

## GMP 调度模型（必考 ⭐⭐⭐⭐⭐）

- **G**（Goroutine）：协程，初始栈仅 2KB
- **M**（Machine）：操作系统线程，实际执行G
- **P**（Processor）：逻辑处理器，默认=CPU核数，控制并发度

### 调度核心机制
- 每个P维护本地G队列（runq）
- 全局G队列（runqhead）作为补充
- **工作窃取（Work Stealing）**：P的本地队列空了，从全局队列或其他P偷取G
- 系统调用时M与P分离，P继续调度其他G

---

## Channel

### 底层结构（hchan）
```
环形队列 + mutex + sendq(发送等待队列) + recvq(接收等待队列)
```

### panic 场景
- 关闭 nil channel
- 重复 close channel
- 向已关闭的 channel 发送数据

### 无缓冲 vs 有缓冲
- **无缓冲**：发送和接收必须同时就绪（同步）
- **有缓冲**：缓冲未满时发送不阻塞，缓冲不空时接收不阻塞

### select
- 随机选择就绪的case
- default分支实现非阻塞操作
- 用于超时控制：`case <-time.After(timeout):`

### goroutine 泄漏防止
- 用 `context` 控制退出
- 发送方负责 close channel
- 设置超时/截止时间

---

## Slice 底层结构

```go
type slice struct {
    ptr *array  // 指向底层数组
    len int     // 当前长度
    cap int     // 容量
}
```

### 扩容策略
- `len < 1024`：容量翻倍
- `len ≥ 1024`：增长约25%（1.25倍）

### 注意事项
- 传参是值拷贝，但共享底层数组
- append后可能因扩容导致底层数组变化
- 子切片修改可能影响原切片

---

## defer / panic / recover

### defer
- 执行顺序：**后进先出（LIFO）**
- 参数在声明时就确定（值拷贝）
- 命名返回值会被defer修改

### panic
- 程序崩溃前会执行所有defer
- panic只能被defer中的recover捕获

### recover
- 只能在defer函数中生效
- 捕获后程序继续执行

---

## Map 并发安全

### 问题
Go原生map不是并发安全的，并发写入会panic

### 解决方案
1. **sync.RWMutex** 包装：适合读多写少
2. **sync.Map**：读写分离，适合读多写少
3. **分片加锁（Sharded Map）**：适合高并发写入

---

## sync 包

| 类型 | 用途 |
|------|------|
| sync.Mutex | 互斥锁，正常模式+饥饿模式 |
| sync.RWMutex | 读写锁 |
| sync.WaitGroup | 等待一组goroutine完成 |
| sync.Once | 单例模式，确保只执行一次 |
| sync.Pool | 对象复用池，减少GC |

---

## Context

### 四种创建方式
- `WithCancel`：手动取消
- `WithTimeout`：超时自动取消
- `WithDeadline`：截止时间取消
- `WithValue`：传递元数据

### 使用原则
- 不要将context存到struct中
- context是线程安全的
- 上游context取消，下游全部取消
