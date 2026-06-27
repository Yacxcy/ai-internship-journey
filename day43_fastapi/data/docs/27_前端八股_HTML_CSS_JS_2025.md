# 前端八股 — HTML/CSS/JavaScript 核心考点

---

## HTML 5题必背

### 1. 从输入 URL 到页面展示的完整过程
DNS解析→TCP连接→TLS握手→HTTP请求→服务器处理→HTTP响应→浏览器解析HTML→构建DOM树→CSS解析→构建渲染树→布局→绘制→合成

### 2. script 标签 defer 和 async 的区别
- **defer**：异步下载，HTML解析完成后、DOMContentLoaded前按顺序执行
- **async**：异步下载，下载完立即执行，不保证顺序
- **普通script**：下载和执行都阻塞HTML解析

### 3. HTML5 语义化标签
header、nav、main、article、section、aside、footer
重要性：SEO友好、可访问性、代码可读性

### 4. DOM 和 BOM
- **DOM**：文档对象模型，操作HTML文档
- **BOM**：浏览器对象模型，操作浏览器（window、navigator、location、history）

### 5. SPA 应用如何做 SEO？
- SSR（服务端渲染）
- 预渲染（Prerender）
- 使用语义化标签
- 合理的title和meta描述

---

## CSS 5题必背

### 1. BFC（块级格式化上下文）
- **触发条件**：float非none、position absolute/fixed、overflow非visible、display flex/grid
- **应用**：清除浮动、防止margin合并、自适应两栏布局

### 2. Flex vs Grid
- **Flex**：一维布局（行或列）
- **Grid**：二维布局（行和列）

### 3. 垂直居中方法
- Flexbox：`display:flex; align-items:center; justify-content:center`
- Grid：`place-items:center`
- 绝对定位 + transform：`top:50%; left:50%; transform:translate(-50%, -50%)`
- 绝对定位 + margin:auto（需定宽高）

### 4. 回流（reflow）和重绘（repaint）
- **回流**：布局改变（width/height/position等）→ 重新计算布局
- **重绘**：样式改变（color/background等）→ 重新绘制但不改变布局

### 5. CSS3 动画
- **transition**：过渡动画，需要触发条件
- **animation**：关键帧动画，可自动播放
- **transform**：2D/3D变换，GPU加速

---

## JavaScript 10题必背

### 1. 闭包
函数可以访问其外部作用域的变量，即使外部函数已执行完。
应用：数据私有化、函数工厂、模块化。

### 2. 原型链
`obj → obj.__proto__ → Constructor.prototype → Object.prototype → null`

### 3. Event Loop
同步代码 → 微任务队列（Promise.then、MutationObserver）→ 宏任务队列（setTimeout、setInterval、IO）

### 4. Promise
三种状态：pending → fulfilled / rejected

### 5. 防抖与节流
- **防抖**：连续触发只执行最后一次（搜索框输入）
- **节流**：固定时间间隔执行一次（滚动事件）

### 6. this 指向四种绑定
1. new 绑定（构造函数）
2. 显式绑定（call/apply/bind）
3. 隐式绑定（对象方法）
4. 默认绑定（严格模式undefined，非严格window）
优先级：new > 显式 > 隐式 > 默认
