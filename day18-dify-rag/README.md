# Day 18: Dify 知识库实战 (PDF 问答助手)

## 配置
- 知识库：3 份 PDF（XXX）
- Embedding: text-embedding-v3 (通义)
- Rerank: gte-rerank (通义)
- 分段：800 / 100 overlap
- 检索：混合检索 + Top 5 + Rerank

## 测试
- 10 个测试用例，准确率 8/10
- 详细见 test_cases.md

## 链接
- 发布链接：[我的问答助手 - Dify](http://localhost/chat/pXPPfTLs6faxL2gi)
- 演示 png：![image-20260603141743524](C:\Users\Ya\Desktop\练习\ai-internship-journey\day18-dify-rag\assets\image-20260603141743524.png)

## 学到
- chunk_size 800 对中文长文档比较合适
- 混合检索（向量+关键词）比纯向量准确率高 ~15%
- Rerank 把 Top 5 重排后能把"刚好相关"的 chunk 提前

## 待优化
- 文档 2 引用经常错位，怀疑分段切坏了
- 跨文档推理类问题召回不全