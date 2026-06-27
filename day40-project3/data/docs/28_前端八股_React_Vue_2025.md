# 前端八股 — React & Vue 核心考点

---

## React 8题必背

### 1. Fiber 架构
- **设计目标**：可中断的异步渲染，提高响应性
- **核心**：将渲染工作拆分成小单元（Fiber节点），可根据优先级中断
- **调度**：requestIdleCallback / Scheduler

### 2. Hooks 规则
为什么不能在条件/循环中调用？
- React依赖调用顺序来识别Hook
- 条件调用会打乱顺序，导致状态错乱

### 3. useMemo vs useCallback
- **useMemo**：缓存计算结果
- **useCallback**：缓存函数引用

### 4. setState 同步/异步
- React 18之前：合成事件和生命周期中是异步，setTimeout中是同步
- React 18自动批处理：所有场景都是批处理（异步）

### 5. 虚拟DOM和Diff算法
- **虚拟DOM**：JS对象模拟DOM，减少真实DOM操作
- **Diff**：同层比较、key标识、类型不同则重建

### 6. React合成事件
React自己封装的事件系统，统一了不同浏览器的差异，采用事件委托机制

### 7. useEffect vs useLayoutEffect
- **useEffect**：异步执行，不阻塞渲染
- **useLayoutEffect**：同步执行，在浏览器绘制前运行

### 8. 受控组件 vs 非受控组件
- **受控**：表单值由React状态控制
- **非受控**：表单值由DOM自身管理（ref获取）

---

## Vue 8题必背

### 1. Vue3 响应式原理
Proxy vs Vue2的Object.defineProperty：
- **优势**：可监听数组变化、对象属性添加/删除、Map/Set
- V2只能劫持已存在的属性，V3全面代理

### 2. Composition API vs Options API
- **Composition API**：逻辑聚合，可复用，TypeScript友好
- **Options API**：按选项分类，简单场景直观

### 3. Vue Diff算法
- 同层比较，双端对比
- 从两端向中间收拢

### 4. computed vs watch
- **computed**：有缓存，依赖不变时不重新计算
- **watch**：无缓存，监听数据变化执行副作用

### 5. v-if vs v-for
为什么不能同时使用？
- v-for优先级高于v-if（Vue2）
- 同时使用会导致性能浪费（先循环再判断）
- 建议用computed过滤或在template外层用v-if

### 6. Vue Router hash vs history
- **hash**：#后面的内容变化不发送请求，兼容性好
- **history**：利用HTML5 History API，需要服务端配置

### 7. $nextTick
DOM更新是异步的，$nextTick在DOM更新后执行回调

### 8. keep-alive
缓存组件实例，避免重复创建和销毁，通过LRU算法管理缓存
