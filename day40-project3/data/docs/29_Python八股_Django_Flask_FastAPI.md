# Python 八股 — Django / Flask / FastAPI 框架高频题

---

## Django 高频八股

| 考点 | 具体问题 |
|------|----------|
| **MVC/MTV** | MVC和MTV模式的区别（Model-View-Controller vs Model-Template-View） |
| **请求生命周期** | wsgi → 中间件(process_request) → 路由 → 视图 → 中间件(process_response) → 响应 |
| **中间件** | 5个方法：process_request / view / response / exception / template_response |
| **CSRF** | 实现机制、ajax POST 如何携带 csrf token |
| **FBV vs CBV** | 函数视图 vs 类视图，CBV如何加装饰器（method_decorator） |
| **ORM** | select_related vs prefetch_related、F对象和Q对象、only vs defer |
| **Form** | Form和ModelForm的作用 |
| **Session/Cookie** | 区别、Django中如何读写session |
| **路由name** | name参数的作用（反向解析URL） |
| **Cache** | Django 缓存配置，如何使用 Redis 做缓存 |
| **Signal** | Django信号机制（pre_save/post_save等） |
| **REST Framework** | 认证流程、组件（序列化/视图/路由/认证/权限/频率/分页）、视图继承关系 |

---

## Flask 高频八股

| 考点 | 具体问题 |
|------|----------|
| **框架对比** | Flask vs Django：轻量微框架 vs 全栈框架 |
| **蓝图** | Blueprint 的作用（模块化、URL前缀） |
| **上下文管理** | 请求上下文、应用上下文的流程 |
| **g 对象** | 请求级别的全局变量，存储单次请求的临时数据 |
| **Session** | 默认session加密后存cookie |
| **Local 对象** | Local/LocalStack/LocalProxy，实现线程/协程隔离 |
| **WTF** | Flask-WTF表单处理，CSRF保护 |
| **WebSocket** | Flask-SocketIO |
| **JWT** | 如何在 Flask 中实现 JWT 认证 |

---

## 三框架对比

| 维度 | Django | Flask | FastAPI |
|------|--------|-------|---------|
| **定位** | 全栈框架 | 轻量级微框架 | 异步API框架 |
| **特点** | 自带ORM/Admin/模板/Form | 灵活、可扩展 | 基于Pydantic、类型提示、自动文档 |
| **适用场景** | 大型企业级应用、CMS | 小型项目、API、微服务 | 高并发API、异步任务 |
| **学习曲线** | 较陡峭 | 较平缓 | 中等 |
| **异步支持** | 3.1+ 开始支持 | 有限 | 原生 async/await |

---

## Python 基础高频八股

1. **装饰器**：原理、应用场景（日志、权限、缓存、计时）
2. **生成器 vs 迭代器**：`yield` 产生生成器，惰性求值
3. **上下文管理器**：`__enter__`/`__exit__`，with语句
4. **`*args` vs `**kwargs`**：位置参数 vs 关键字参数
5. **深拷贝 vs 浅拷贝**：copy()复制引用，deepcopy()递归复制
6. **GIL**：全局解释器锁，同一时刻只有一个线程执行Python字节码
7. **垃圾回收**：引用计数为主 + 标记清除 + 分代回收
8. **`__new__` vs `__init__`**：new创建实例，init初始化实例
