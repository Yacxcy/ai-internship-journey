# Day 19: Dify 工作流 - Text2SQL

## 工作流图
开始 → 生成 SQL (LLM) → 安全检查 (代码) → 执行 SQL (代码) → 总结 (LLM) → 结束

## 测试结果
- 5 个测试用例，4 个正确，1 个被安全检查拦截
- 详见 test_cases.md

## 链接
[Text2SQL 工作流 - Dify](http://localhost/workflow/PzwyM9z82Atdljwg)

## 学到
- Dify 工作流 = 节点连接图，节点间通过变量传值
- 代码节点用于把结构化数据转格式
- LLM 节点 + 条件分支 = 可控的多步推理
- Cloud 版无法访问本地 SQLite，需 hardcode 或包成 HTTP API