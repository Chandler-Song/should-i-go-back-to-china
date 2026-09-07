# 《我应该回国吗？》网页书 — 技术设计文档（design.md）

> 版本：v1.0  
> 创建日期：2026-09-07  
> 关联技能：`book_design_style`（商务沉稳型社科图书网页风格）  
> 方案类型：纯前端，零构建，CDN 引入

---

## 1. 设计目标

把 `gobackchina/` 下 40 章 markdown 原稿做成一本**可在线阅读的网页书**，满足：

- 还原书籍气质：封面、目录、章节、作者介绍一应俱全
- 长文阅读体验优：衬线正文、1.85 行高、720px 阅读宽、两端对齐
- 交互完整：目录跳转、阅读进度、字号/主题切换、阅读记忆、预加载
- 零构建部署：推到 GitHub Pages 即用，无需 Node/Vite/Webpack
- 双主题：深色/浅色一键切换，localStorage 持久化

---

## 2. 总体架构

### 2.1 文件结构

```
gotochina/
├── index.html                  # 单页入口（首页 + 阅读器双视图）
├── assets/
│   ├── css/
│   │   └── book.css            # 自定义排版样式（覆盖 Tailwind 不足的部分）
│   ├── js/
│   │   ├── app.js              # Alpine.js 主组件 + 章节数据 + 交互逻辑
│   │   └── chapters.js         # 40 章元数据（file/title/part/subtitle）
│   └── images/
│       └── cover.png           # 封面图片（PNG）
├── gobackchina/                # 40 章 markdown 原稿（已存在，按需 fetch）
│   ├── ch01_overview_and_era_context.md
│   └── ... ch40_financial_tax_cross_border.md
└── docs/
    ├── design.md               # 本文档
    ├── spec.md                # 需求规格
    ├── tasks.md               # 任务分解
    ├── review.md              # 设计评审
    └── book_design_style.md   # 设计风格技能文档（已存在）
```

### 2.2 运行时数据流

```
用户打开 index.html
   │
   ├─ 首页视图（view='home'）
   │    └─ 静态渲染：英雄区 / 核心理念 / 模型卡片 / 金句墙 / 目录 / 作者 / 页脚
   │
   └─ 点击章节 → view='read'
        ├─ 查 chapterCache[index] 是否已加载
        │    ├─ 命中：直接渲染
        │    └─ 未命中：fetch('gobackchina/chXX_xxx.md') → marked.parse() → 缓存 → 渲染
        ├─ 渲染后 preloadChapter(index+1)（预载下一章）
        └─ @scroll 更新顶部进度条
```

### 2.3 路由方案

单页 + hash 路由，无后端：

| URL | 视图 | 说明 |
|-----|------|------|
| `index.html` 或 `#/` | home | 首页 |
| `#/ch/01` | read | 第 01 章 |
| `#/ch/25` | read | 第 25 章 |

监听 `hashchange`，解析 `#/ch/{id}` 切换视图并加载章节。

---

## 3. 技术选型

| 依赖 | 版本 | 用途 | 引入方式 |
|------|------|------|----------|
| Tailwind CSS | Play CDN | 原子化样式 + 双主题 | `<script src="https://cdn.tailwindcss.com">` |
| Alpine.js | 3.14.1 | 声明式交互（视图切换、抽屉、主题） | `<script defer src="...alpinejs...">` |
| marked.js | 12.0.2 | markdown → HTML | `<script defer src="...marked...">` |
| Google Fonts | - | Noto Serif SC（正文）+ Noto Sans SC（界面） | `<link>` |

**为何不用 Vue/React**：本书是静态内容站，Alpine.js 3KB 够用，且零构建。  
**为何不用 VitePress/Docsify**：它们偏技术文档，缺书籍特有元素（封面、金句墙、作者介绍、核心模型卡片）。

---

## 4. 配色与字体（遵循 book_design_style §2.1 / §2.2）

### 4.1 Tailwind Config（内联在 index.html）

```javascript
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        navy: { 50:'#ebf0f5', 100:'#d6e0eb', 200:'#adc2d9', 300:'#84a3c7',
                400:'#5b84b5', 500:'#3b5b7f', 600:'#1e3a5f', 700:'#15293f',
                800:'#0f1f30', 900:'#0a1521' },
        gold: { DEFAULT:'#b8860b', light:'#d4a843', dark:'#8b6508' },
        ink:  { DEFAULT:'#111827', light:'#4b5563', muted:'#6b7280' }
      },
      fontFamily: {
        serif: ['"Noto Serif SC"', '"Source Han Serif SC"', '"Songti SC"', 'serif'],
        sans:  ['-apple-system', '"PingFang SC"', '"Microsoft YaHei"', 'sans-serif']
      }
    }
  }
}
```

### 4.2 字体角色

- **正文 / 章节标题 / 金句**：`font-serif`（Noto Serif SC，传递书籍质感）
- **界面 / 按钮 / 目录侧栏 / 元信息**：`font-sans`（无衬线，清晰利落）

---

## 5. 页面结构

### 5.1 首页（view='home'）— 七区块叙事流

遵循 `book_design_style §2.5`，自上而下：

| # | 区块 | 内容 | 布局 |
|---|------|------|------|
| 1 | 英雄区 | SVG 封面 + 书名《我应该回国吗？》+ 副标题 + "开始阅读"CTA + "随机一章" | `grid md:grid-cols-2`，`py-16 md:py-24` |
| 2 | 核心理念 | 一段话讲清"回国 = 七子决策耦合序列 + 五因子模型" | `max-w-3xl` 卡片 |
| 3 | 五因子模型卡片 | 动机/可迁移性/机会成本/家庭/时机，每张卡片含因子名+一句话 | `grid md:grid-cols-2 lg:grid-cols-3 gap-6` |
| 4 | 金句墙 | 从原稿精选 6-9 句金句 | `grid md:grid-cols-2 lg:grid-cols-3 gap-6` |
| 5 | 目录导航 | 9 篇分组，每篇下展开各章，点击跳转 | 篇卡片 `grid md:grid-cols-2 gap-3`，章列表 |
| 6 | 作者介绍 | 头像 + 姓名 + 标签 + 统计 + 著作链接 | `flex md:flex-row gap-8` |
| 7 | 页脚 | 书名 + 作者 + 一句金句 + 免责声明摘要 | 居中文字 |

**卡片统一样式**：
```
bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm
border border-slate-200 dark:border-slate-700
hover:shadow-md transition-all hover:-translate-y-1
```

### 5.2 阅读视图（view='read'）

```
┌─────────────────────────────────────────────────┐
│ 顶部固定栏：←返回 | 第XX章 标题 | 字号A- A+ | 🌓主题 │  ← 进度条贴顶
├──────────┬──────────────────────────────────────┤
│ 侧边目录  │  阅读区（max-w-[720px]）              │
│ （lg常驻  │   ## 章节标题                          │
│  md抽屉） │   正文段落...                          │
│           │   表格 / 引用 / 列表...                │
│ 40章列表  │                                       │
│ 当前章高亮│   ← 上一章        下一章 →             │
└──────────┴──────────────────────────────────────┘
```

- **顶部固定栏**：返回首页 / 章节标题 / 字号调节 / 主题切换
- **进度条**：贴顶 2px，宽度随滚动百分比
- **侧边目录**：`lg:` 常驻左栏 240px；`<lg` 抽屉式（汉堡按钮触发 + 遮罩层）
- **阅读区**：`max-w-[720px] mx-auto`，`px-6 py-10`
- **翻页**：底部"上一章 / 下一章"按钮，到第 40 章时"下一章"禁用

---

## 6. 章节数据结构（assets/js/chapters.js）

```javascript
const CHAPTERS = [
  { id:'01', part:1, file:'ch01_overview_and_era_context.md',
    title:'回国决策总论与 2026 时代背景' },
  { id:'02', part:1, file:'ch02_tier1_tech_giants.md',
    title:'第一梯队大厂全景：华为 / 字节 / 腾讯 / 阿里' },
  // ... 共 40 条
];

const PARTS = [
  { id:1, name:'市场环境与机会调研', range:'01-08' },
  { id:2, name:'薪酬与级别',         range:'09-12' },
  { id:3, name:'城市与生活',         range:'13-17' },
  { id:4, name:'家庭与社会',         range:'18-20' },
  { id:5, name:'信息收集与方法论',   range:'21-24' },
  { id:6, name:'心理学与决策',       range:'25-28' },
  { id:7, name:'时机与案例',         range:'29-31' },
  { id:8, name:'时代挑战',           range:'32-35' },
  { id:9, name:'实操手册',           range:'36-40' },
];
```

`part` 字段用于侧边目录分组与首页目录导航分组。

---

## 7. 交互逻辑（assets/js/app.js）

### 7.1 Alpine 主组件状态

```javascript
{
  view: 'home',              // 'home' | 'read'
  currentChapter: null,      // 当前章 id
  chapterCache: {},          // { '01': '<html>', '02': '<html>' }
  fontSize: 18,              // 16-22
  theme: 'light',            // 'light' | 'dark'
  sidebarOpen: false,        // 移动端抽屉
  progress: 0,               // 0-100 阅读进度
  loading: false,            // 章节加载中

  init() { /* 从 localStorage 恢复 fontSize/theme；监听 hashchange */ },
  goHome() { /* location.hash = '' */ },
  openChapter(id) { /* location.hash = '#/ch/' + id */ },
  async loadChapter(id) { /* fetch + marked + cache + preload next */ },
  toggleTheme() { /* classList.toggle('dark') + persist */ },
  setFont(delta) { /* fontSize clamp 16-22 + persist */ },
  onScroll() { /* rAF 更新 progress */ },
}
```

### 7.2 关键交互

| 功能 | 实现 |
|------|------|
| 视图切换 | `view` 状态 + `x-show` 切换，hash 路由同步 |
| 章节加载 | `fetch('gobackchina/' + file).then(r=>r.text()).then(marked.parse)` |
| 章节缓存 | `chapterCache[id]`，命中直接渲染 |
| 预加载 | 当前章渲染后 `setTimeout(()=>loadChapter(id+1), 500)`，仅缓存不渲染 |
| 阅读进度 | `@scroll.window` + `requestAnimationFrame`，`progress = scrollTop / (scrollHeight - clientHeight) * 100` |
| 阅读记忆 | `localStorage` 存 `fontSize` / `theme` / `lastChapter` |
| 主题切换 | `document.documentElement.classList.toggle('dark')` |
| 移动端目录 | `sidebarOpen` + 抽屉 `translate-x` + 遮罩层 |

### 7.3 错降级

- `fetch` 失败：阅读区显示"章节加载失败，请检查网络或[返回首页]"。
- `marked` 未加载完：等待 `window.marked` 就绪再解析（轮询 50ms）。
- CDN 不可达：Tailwind 降级为浏览器默认样式（可读但无设计），Alpine 降级为静态首页（章节点击用 `window.location` 跳转兜底）。

---

## 8. 封面（assets/images/cover.png）

遵循 `book_design_style §2.4`，自动生成：

- 画布 600×840，Navy 渐变背景 `#15293f → #0a1521`
- Gold 双线边框（外 3px + 内 1px，间距 12px）
- 书名"我应该回国吗？"居中，130px，金色渐变 `#d4a843 → #b8860b`
- 副标题"Should I Go Back to China?"，24px，navy-200
- 底部作者署名"宋秀强"，18px，navy-300
- 装饰语"硅谷工程师回国决策手册"，13px，navy-400 70% 透明度

`<img src="cover.png">` 直接引用 PNG 封面。

---

## 9. Markdown 排版样式（assets/css/book.css）

遵循 `book_design_style §4.4`，关键样式：

```css
.markdown { font-family: var(--font-serif); font-size: 18px; line-height: 1.85; }
.markdown h1 { font-size: 1.75em; border-bottom: 2px solid #b8860b; padding-bottom: .5em; }
.markdown h2 { font-size: 1.3em; color: #1e3a5f; margin-top: 1.5em; }
.markdown h3 { font-size: 1.1em; color: #3b5b7f; }
.markdown p  { text-align: justify; text-justify: inter-ideograph; margin: 1em 0; }
.markdown blockquote {
  border-left: 4px solid #b8860b; background: #f8f6f0;
  padding: 1em 1.5em; margin: 1.5em 0; color: #4b5563; border-radius: 0 8px 8px 0;
}
.markdown table { width: 100%; border-collapse: collapse; margin: 1.5em 0; font-size: .95em; }
.markdown th { background: #1e3a5f; color: #fff; padding: .75em; text-align: left; }
.markdown td { border-bottom: 1px solid #e2e8f0; padding: .75em; }
.markdown tr:nth-child(even) td { background: #f8fafc; }
.markdown code { background: #f1f5f9; padding: .15em .4em; border-radius: 4px; font-size: .9em; }
.markdown ul, .markdown ol { padding-left: 1.5em; margin: 1em 0; }
.markdown li { margin: .5em 0; }
.markdown hr { border: none; border-top: 1px solid #b8860b; margin: 2em 0; opacity: .5; }
```

深色模式用 `.dark .markdown xxx` 覆盖颜色（blockquote 背景、表头、斑马纹等）。

---

## 10. 响应式（遵循 book_design_style §4.3）

| 断点 | 行为 |
|------|------|
| `lg` ≥1024px | 侧边目录常驻左栏，阅读区居中 720px |
| `md` ≥768px | 首页卡片 2 列，英雄区双栏，目录抽屉触发 |
| 默认 <768px | 全单列，抽屉目录，卡片堆叠，字号自动缩 1px |

---

## 11. 性能与可访问性

- **按需加载**：40 章非首屏，仅点击时 fetch，已加载章节缓存秒切
- **预加载**：当前章渲染后静默预载下一章
- **字体 fallback**：Noto Serif SC 加载前用 Songti SC / serif 兜底
- **语义化**：`<main>` `<article>` `<nav>` `<header>` `<footer>`
- **键盘**：Esc 关抽屉，← → 翻章
- **对比度**：navy/gold/ink 组合满足 WCAG AA

---

## 12. 部署

纯静态，任一静态托管可用：

- **GitHub Pages**：推到 `gh-pages` 分支或主分支 `/docs`，开启 Pages 即可
- **本地预览**：`python -m http.server 8000` 后访问 `localhost:8000`

> 注意：因使用 `fetch` 加载 markdown，**不能直接 file:// 打开**，必须经 HTTP 服务器。

---

## 13. 与设计风格文档的对应关系

| 本设计 | book_design_style 章节 |
|--------|------------------------|
| §4 配色字体 | §2.1 §2.2 §4.1 |
| §5 页面结构 | §2.5 |
| §7 交互逻辑 | §2.6 |
| §8 封面 | §2.4 |
| §9 排版 | §4.4 |
| §10 响应式 | §4.3 |
| §3 技术选型 | §4.2 |

---

## 14. 不做（明确排除）

- 不做全文搜索（40 章目录跳转够用，后续可加 Lunr.js）
- 不做评论/批注（纯阅读）
- 不做 SSR/SEO（社科书 SEO 需求低）
- 不做后端（纯前端方案，用户偏好）
- 不做构建工具（零构建，CDN 即用）
- 不做 PWA/离线（CDN 依赖，离线本就降级）

---

## 15. 验收标准

1. `index.html` 经 HTTP 服务器打开，首页七区块完整渲染
2. 点击任一章节，2 秒内加载并渲染 markdown（首次），缓存后秒切
3. 深色/浅色切换正常，刷新后保持
4. 字号 16-22 可调，刷新后保持
5. 阅读进度条随滚动实时更新
6. 移动端（<768px）抽屉目录正常开关
7. 上一章/下一章翻页正确，第 40 章无下一章
8. 40 章全部可加载无报错