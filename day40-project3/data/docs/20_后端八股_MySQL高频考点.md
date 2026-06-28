# 后端八股 — MySQL 高频考点

---

## B+树索引（必考）

### 为什么用B+树不用B树？
- B+树非叶子节点只存key，不存数据 → 一个节点可以存更多key → 树更矮 → IO次数更少
- B+树叶节点通过有序链表连接 → 范围查询效率高
- B树非叶子节点也存数据 → 每个节点存的key少 → 树高 → IO次数多

### B+树 vs 哈希表
- B+树支持范围查询和排序
- 哈希表只支持等值查询，O(1)但不支持范围

---

## 索引分类

| 类型 | 说明 |
|------|------|
| 聚簇索引 | 数据按索引顺序物理存储，InnoDB主键索引就是聚簇索引 |
| 非聚簇索引 | 叶子节点存的是主键值，需要回表查数据 |
| 联合索引 | 多列组合索引，遵循最左前缀原则 |
| 覆盖索引 | 查询的列都在索引中，不需要回表（Using index） |

---

## 最左前缀原则
- 联合索引(a,b,c)，where a=1 and b=2 可以用索引
- where b=2 and c=3 不能用索引（跳过了a）
- where a=1 and c=3 只能用到a列
- 范围查询后面的列索引失效：where a=1 and b>2 and c=3 只能用到a和b

---

## 索引失效场景
- 函数操作：`WHERE DATE(create_time) = '2025-01-01'`
- 类型转换：`WHERE phone = 13800138000`（phone是varchar）
- LIKE前缀通配：`LIKE '%abc'`
- OR条件中有一列没有索引
- !=、NOT IN、IS NULL在部分情况
- 联合索引跳过最左列

---

## 事务与隔离级别

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|----------|------|-----------|------|
| READ UNCOMMITTED | ✓ | ✓ | ✓ |
| READ COMMITTED | ✗ | ✓ | ✓ |
| REPEATABLE READ (InnoDB默认) | ✗ | ✗ | 部分解决（Next-Key Lock） |
| SERIALIZABLE | ✗ | ✗ | ✗ |

---

## MVCC 机制

- **Read View**：存储事务快照时活跃的事务列表
- **undo log 版本链**：每次修改都生成undo log，通过DB_ROLL_PTR链接
- **RC**：每次SELECT都生成新的Read View
- **RR**：只在第一次SELECT时生成Read View，后续复用

---

## InnoDB 锁类型

| 锁 | 说明 |
|-----|------|
| 行锁（Record Lock） | 锁住索引记录 |
| 间隙锁（Gap Lock） | 锁住索引之间的间隙 |
| 临键锁（Next-Key Lock） | 行锁 + 间隙锁，InnoDB RR下默认使用 |

---

## 日志体系

| 日志 | 作用 |
|------|------|
| redo log | 保证持久性，crash后恢复已提交的事务 |
| undo log | 保证原子性，回滚未提交的事务，MVCC依赖 |
| binlog | MySQL Server层日志，主从复制、数据恢复 |

### 两阶段提交（redo log + binlog）
1. prepare阶段：写redo log（prepare状态）
2. commit阶段：写binlog → 修改redo log为commit状态
- 保证redo log和binlog的一致性
