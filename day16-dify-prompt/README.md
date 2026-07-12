# Day 16: Dify Prompt 工程实战

## Bot 列表

### 1. 智能翻译助手
- 链接：[Bot 1 翻译助手 - Dify](http://localhost/completion/i2U4MPJljZJyzJ1A)
- 特点：自动识别原文语言、保留格式、不输出多余内容
- 截图：![image-20260602113722328](C:\Users\Ya\Desktop\练习\ai-internship-journey\day16-dify-prompt\assets\image-20260602113722328.png)

### 2. 周报生成器 v2
- 链接：[Bot 2 周报生成器 v2 - Dify](http://localhost/completion/XXTGT3ttwWeD4tVK)

- 特点：3 种情绪基调、自动评级工作量、检测需协助项

  ![image-20260602114217604](C:\Users\Ya\Desktop\练习\ai-internship-journey\day16-dify-prompt\assets\image-20260602114217604.png)

### 3. 文案润色助手
- 链接：[Bot 3 文案润色 - Dify](http://localhost/completion/lDqAvcqnwWKTT8st)

- 特点：Few-shot 实现 3 种风格输出

  ![image-20260602114441791](C:\Users\Ya\Desktop\练习\ai-internship-journey\day16-dify-prompt\assets\image-20260602114441791.png)

## 学到的 Dify 技巧
- 变量注入 `{{x}}`
- 下拉选项控制 prompt 分支
- 段落变量适合长文本
- temperature 调度：翻译 0.2 / 周报 0.5 / 文案 0.8