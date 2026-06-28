# Java 八股 — Spring & MyBatis 高频面试题

---

## Spring Bean 生命周期
```
实例化 → 属性注入 → BeanNameAware → BeanFactoryAware
→ BeanPostProcessor#before → InitializingBean#afterPropertiesSet
→ 自定义init-method → BeanPostProcessor#after → Bean 就绪
→ DisposableBean#destroy → 自定义destroy-method
```

---

## Spring 循环依赖解决

Spring 通过**三级缓存**解决单例 Bean 的循环依赖：

| 缓存级别 | 名称 | 存储内容 |
|----------|------|----------|
| 一级缓存 | `singletonObjects` | 完全初始化好的 Bean |
| 二级缓存 | `earlySingletonObjects` | 提前暴露的 Bean |
| 三级缓存 | `singletonFactories` | Bean 工厂 |

**核心流程**：A 实例化后把工厂放入三级缓存 → 注入 B 时触发 B 实例化 → B 注入 A 时从三级缓存获取 A 的早期引用 → 完成注入。

---

## Spring AOP 实现原理

- **JDK 动态代理**：目标类实现了接口时使用，基于 `InvocationHandler`
- **CGLIB 代理**：目标类无接口时使用，通过字节码增强生成子类
- **AspectJ**：编译期织入，性能优于运行时代理

---

## Spring 事务传播行为

| 传播行为 | 说明 |
|----------|------|
| **REQUIRED**（默认） | 有事务则加入，无则新建 |
| **REQUIRES_NEW** | 始终新建事务，挂起当前事务 |
| **NESTED** | 嵌套事务，内层回滚不影响外层 |
| **SUPPORTS** | 有则加入，无则以非事务执行 |
| **MANDATORY** | 必须存在事务，否则抛异常 |
| **NEVER** | 必须在无事务环境下执行 |
| **NOT_SUPPORTED** | 挂起当前事务，以非事务方式执行 |

---

## MyBatis 高频考点

### `#{}` 和 `${}` 的区别

| | `#{}` | `${}` |
|------|------|------|
| **处理方式** | 预编译占位符 `?` | 直接字符串拼接 |
| **SQL 注入** | 安全 | 存在注入风险 |
| **使用场景** | 传递参数值 | 动态表名/列名 |

### MyBatis 缓存

| 缓存级别 | 作用域 | 说明 |
|----------|--------|------|
| **一级缓存** | SqlSession 级别 | 默认开启，DML操作清除 |
| **二级缓存** | Mapper/Namespace 级别 | 不同 SqlSession 可共享 |

### Dao 接口为什么没有实现类也能执行？
MyBatis 通过 JDK 动态代理 + `MapperProxy` 为 Dao 接口生成代理对象，调用方法时根据"namespace + 方法ID"找到对应的 XML 中的 SQL 并执行。

### MyBatis 分页原理
- **逻辑分页**（RowBounds）：查询全部数据后在内存中截取，性能差
- **物理分页**（PageHelper 插件）：通过拦截器改写 SQL，添加 `LIMIT` 语句

---

## Spring Boot 自动配置原理

`@SpringBootApplication` → `@EnableAutoConfiguration` → `@Import(AutoConfigurationImportSelector.class)` → 读取 `META-INF/spring/...AutoConfiguration.imports` 文件 → 通过 `@Conditional` 系列注解按条件加载配置
