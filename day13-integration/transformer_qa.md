# Transformer 八股 5 题

## Q1: Transformer 比 RNN 强在哪？
- 并行计算（RNN 必须按时间步串行）
- 长距离依赖捕捉（Attention 一步到位）
- 训练效率高，能堆参数堆出 GPT
答：RNN 需要按顺序处理数据，训练慢，而且难以学习长距离依赖；Transformer 通过 Self-Attention 让每个词直接关注所有词，实现并行计算，更容易捕获长距离关系，因此训练更快、效果更好，成为 GPT、BERT 等大模型的基础架构。

## Q2: Self-Attention 直观理解？
每个词都和句子里所有词算"相关度"，再按相关度加权聚合信息。
比如"苹果掉到牛顿头上"，"它"和"苹果"的相关度高，所以"它"更多吸收"苹果"的语义。
答：Self-Attention 是 Transformer 的核心机制，它允许序列中的每个词直接与其他所有词建立联系，通过计算注意力权重来衡量各词的重要性，从而获得包含全局上下文信息的表示，解决了传统 RNN 难以捕获长距离依赖的问题。

## Q3: 多头注意力是干嘛的？
多个 Self-Attention 并行，每个头关注不同模式（语法/语义/位置等），
最后拼接，类似 CNN 多个卷积核。
答：多头注意力（Multi-Head Attention）是在多个不同的表示子空间中并行执行 Attention 计算。每个注意力头可以关注输入序列中的不同关系和特征，例如语法关系、语义关系、位置关系等，最后将多个头的结果拼接融合，从而获得更丰富、更全面的特征表示，提高模型的表达能力。

## Q4: Encoder-Decoder vs Decoder-only？
- Encoder-Decoder：BERT、T5，理解+生成两阶段
- Decoder-only：GPT、LLaMA、DeepSeek，自回归生成
- 当前 LLM 主流是 Decoder-only


## Q5: 为什么需要位置编码？
Attention 本身没有位置概念（打乱顺序结果一样），
位置编码给每个 token 加上"位置信息"，让模型知道词序。
