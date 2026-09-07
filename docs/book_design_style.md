# 技能模块：社科商业图书网页设计风格

> 技能ID：`book_design_style`  
> 版本：v1.0  
> 来源项目：《权力：普通人的人生跃迁法则》网页图书  
> 创建日期：2026-08-27  
> 适用范围：社科、商业认知、职场成长类书籍的网页化呈现

---

## 1. 风格定义

**本风格定位为"商务沉稳型社科图书网页风格"**，核心诉求是在线长文阅读体验与书籍气质的视觉传达之间的平衡。

一句话概括：**深蓝灰为底、古铜金为饰、衬线为骨、卡片为形**——以商务书籍的沉稳质感承载社科内容的思想深度，以现代网页的交互方式提升阅读体验。

---

## 2. 设计维度与核心特征

本风格涵盖六个设计维度，每个维度有明确的参数规范。

### 2.1 配色体系

| 角色 | 名称 | 浅色值 | 深色值 | 用途 |
|------|------|--------|--------|------|
| 主色 | Navy（深蓝灰） | `#1e3a5f` | `#adc2d9` | 标题、按钮、强调 |
| 点缀 | Gold（古铜金） | `#b8860b` | `#d4a843` | 分隔线、标签、装饰 |
| 正文 | Ink（墨色） | `#111827` | `#e2e8f0` | 段落正文 |
| 辅助 | Ink-muted | `#6b7280` | `#9a9a9a` | 次要文字 |
| 背景 | 白/灰 | `#ffffff` | `#0f172a` | 页面底色 |
| 卡片底 | 浅灰 | `#f8fafc` | `#1e293b` | 卡片、引用块 |

**核心特征**：
- 低饱和度配色，避免刺眼，适合长时间阅读
- 主色与点缀色对比适度，金色仅用于装饰不用于大面积
- 深/浅双主题，通过 `class="dark"` 切换

**色阶扩展（Tailwind config）**：
```javascript
navy: { 50:'#ebf0f5', 100:'#d6e0eb', 200:'#adc2d9', 300:'#84a3c7',
        400:'#5b84b5', 500:'#3b5b7f', 600:'#1e3a5f', 700:'#15293f',
        800:'#0f1f30', 900:'#0a1521' }
gold: { DEFAULT:'#b8860b', light:'#d4a843', dark:'#8b6508' }
ink:  { DEFAULT:'#111827', light:'#4b5563', muted:'#6b7280' }
```

### 2.2 字体系统

| 用途 | 字体栈 | CSS 变量 |
|------|--------|----------|
| 正文（衬线） | `"Noto Serif SC", "Source Han Serif SC", "Songti SC", serif` | `--font-serif` |
| 界面（无衬线） | `-apple-system, "PingFang SC", "Microsoft YaHei", sans-serif` | `--font-sans` |

**核心特征**：
- 中文正文用衬线字体，笔画有起收，传递书籍质感
- 界面元素用无衬线，清晰利落
- 通过 Google Fonts 引入 Noto Serif SC + Noto Sans SC

**字号规范**：
| 元素 | 桌面 | 移动端 |
|------|------|--------|
| 章节标题 h1 | 1.75em | 1.5em |
| 小节标题 h2 | 1.3em | 1.2em |
| 正文 | 18px（可调 16–22px） | 17px |
| 界面文字 | 14–16px | 13–15px |

### 2.3 版式与阅读区

| 参数 | 值 | 说明 |
|------|-----|------|
| 行高 | 1.85 | 中文长文最佳行高 |
| 段间距 | 1em | 段落呼吸感 |
| 阅读区最大宽度 | 720px（首页 768px） | 黄金阅读宽度 |
| 对齐方式 | justify + inter-ideograph | 两端对齐，中文友好 |
| 阅读区内边距 | 40px 24px（桌面）/ 24px 18px（移动） | |

### 2.4 封面构图

**自动生成 SVG 封面**，后续可用 PNG 替换。

| 参数 | 值 |
|------|-----|
| 画布尺寸 | 600 × 840（3:4.2 竖版） |
| 背景 | Navy 渐变 `#15293f → #0a1521` |
| 装饰边框 | Gold 双线边框，外粗内细 |
| 书名 | 居中，Noto Serif SC，130px，金色渐变 |
| 副标题 | 居中，24px，navy-200 |
| 作者署名 | 底部，18px，navy-300 |
| 装饰语 | 底部，13px，navy-400，70% 透明度 |

**替换方式**：将 `cover.png` 放入 `assets/images/` 同目录即可，`<img>` 标签的 `onerror` 自动降级。

### 2.5 视觉层级与组件

首页采用**自上而下的叙事流**，每个区块有明确的视觉角色：

| 序号 | 区块 | 视觉角色 | 布局参数 |
|------|------|----------|----------|
| 1 | 英雄区 | 第一印象：封面 + 书名 + CTA | `grid md:grid-cols-2`，`py-16 md:py-24` |
| 2 | 核心理念 | 深度引导：一段话讲清书的核心主张 | `max-w-3xl`，卡片 `rounded-2xl p-8 md:p-12` |
| 3 | 模型卡片 | 结构化呈现：核心模型可视化 | `grid md:grid-cols-2 lg:grid-cols-3 gap-6` |
| 4 | 金句墙 | 情感共鸣：精选金句卡片网格 | `grid md:grid-cols-2 lg:grid-cols-3 gap-6` |
| 5 | 目录导航 | 导览入口：按篇分组的卡片目录 | `grid md:grid-cols-2 gap-3` |
| 6 | 作者介绍 | 信任建立：头像 + 标签 + 统计 + 著作 | `flex md:flex-row gap-8` |
| 7 | 页脚 | 收尾：书名 + 作者 + 金句 | 居中文字 |

**卡片统一样式**：
```
bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm
border border-slate-200 dark:border-slate-700
hover:shadow-md transition-all hover:-translate-y-1
```

### 2.6 交互模式

| 功能 | 实现方式 | 说明 |
|------|----------|------|
| 视图切换 | Alpine.js `view: 'home' \| 'read'` | 单页双视图，hash 路由 |
| 章节加载 | `fetch` + `marked.parse()` | 按需加载，非首屏不加载 |
| 章节缓存 | `chapterCache{}` 对象 | 已加载章节秒切 |
| 预加载 | `preloadChapter(index+1)` | 当前章加载完自动预载下一章 |
| 阅读进度 | `@scroll` + rAF | 顶部进度条实时更新 |
| 阅读记忆 | `localStorage` | 字号/主题/章节位置持久化 |
| 主题切换 | `classList.toggle('dark')` | Tailwind `darkMode: 'class'` |
| 移动端目录 | 抽屉式 + 遮罩层 | `<768px` 汉堡按钮触发 |

---

## 3. 适用场景

| 场景 | 适用度 | 说明 |
|------|--------|------|
| 社科/商业认知类书籍 | ★★★★★ | 完全匹配，本风格即为此设计 |
| 职场成长/自我提升类 | ★★★★★ | 气质契合，沉稳不轻浮 |
| 学术著作（通俗版） | ★★★★☆ | 衬线正文显学术感，卡片降严肃感 |
| 文学作品集 | ★★★☆☆ | 可用但偏理性，文学可考虑更感性配色 |
| 技术文档/手册 | ★★☆☆☆ | 过于书籍化，技术文档宜用 Docsify/VitePress |
| 儿童读物 | ★☆☆☆☆ | 配色过于沉稳，不适合 |

---

## 4. 设计规范与参数速查

### 4.1 Tailwind Config 完整定义

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
      }
    }
  }
}
```

### 4.2 CDN 引入清单

```html
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>
<!-- Alpine.js -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.1/dist/cdn.min.js"></script>
<!-- marked.js -->
<script defer src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 4.3 响应式断点

| 断点 | 宽度 | 行为变化 |
|------|------|----------|
| `lg` | ≥1024px | 侧边目录常驻，双栏布局 |
| `md` | ≥768px | 卡片网格 2 列，英雄区双栏 |
| 默认 | <768px | 单列，抽屉目录，卡片堆叠 |

### 4.4 Markdown 排版关键 CSS

```css
.markdown { font-family: var(--font-serif); font-size: 18px; line-height: 1.85; }
.markdown h1 { font-size: 1.75em; border-bottom: 2px solid #b8860b; }
.markdown blockquote { border-left: 4px solid #b8860b; background: #f8f6f0; }
.markdown p { text-align: justify; text-justify: inter-ideograph; }
```

---

## 5. 复用示例

### 5.1 最小化复用步骤

1. **复制配色**：将 §4.1 的 `tailwind.config` 粘贴到项目
2. **复制 CDN**：将 §4.2 的引入清单粘贴到 `<head>`
3. **复制排版 CSS**：将 §4.4 的样式粘贴到自定义 CSS 文件
4. **定义章节数据**：在 JS 中定义 `chapters` 数组（file + title + part）
5. **搭建首页骨架**：按 §2.5 的七个区块顺序搭建
6. **实现阅读器**：侧边目录 + 阅读区 + 进度条 + 翻页

### 5.2 适配另一本书的改动点

| 改动项 | 位置 | 示例 |
|--------|------|------|
| 书名/副标题 | `BOOK` 对象 | `name: '搜商', subtitle: '面对未知的能力'` |
| 配色主色 | `tailwind.config` | 改 navy 为墨绿即可换气质 |
| 金句 | `QUOTES` 数组 | 从新书提取 6–9 句 |
| 核心模型 | `POWER_LEVELS` 数组 | 替换为新书的核心框架 |
| 作者信息 | `AUTHOR` 对象 | 姓名、头衔、统计、著作 |
| 封面 | `cover.svg` | 改书名文字和配色 |
| 章节分组 | `chapters` 的 `part` 字段 | 按新书的篇划分 |

### 5.3 配色变体示例

保持结构不变，仅改配色即可适配不同气质：

| 变体 | 主色 | 点缀色 | 气质 |
|------|------|--------|------|
| 商务蓝（默认） | Navy `#1e3a5f` | Gold `#b8860b` | 沉稳、权威 |
| 学院绿 | `#1e3a2f` | `#b8860b` | 学术、严谨 |
| 文艺紫 | `#3b1e5f` | `#d4a843` | 优雅、思辨 |
| 科技青 | `#0f4f5f` | `#43b8a8` | 现代、理性 |

---

## 6. 优势与局限性

### 6.1 优势

| 优势 | 说明 |
|------|------|
| 零构建部署 | 全部 CDN 引入，推到 GitHub Pages 即用 |
| 阅读体验优 | 衬线正文 + 1.85 行高 + 720px 宽度，中文长文最佳实践 |
| 双主题完备 | 深/浅色一键切换，CSS 变量统一管理 |
| 性能优化 | 章节按需加载 + 缓存 + 预加载，翻页零延迟 |
| 维护成本低 | 新增章节仅需在 chapters 数组追加一条 |
| 首页叙事完整 | 英雄区→理念→模型→金句→目录→作者，转化路径清晰 |
| 封面自动生成 | SVG 封面零依赖，可用 PNG 无缝替换 |

### 6.2 局限性

| 局限 | 说明 | 缓解方案 |
|------|------|----------|
| 依赖 CDN | 离线环境无法加载 Tailwind/Alpine | 可下载到本地引用 |
| 无全文搜索 | 30 章只能通过目录跳转 | 可后续集成 Lunr.js |
| 无 SSR/SEO | 单页应用，搜索引擎只抓到空壳 | 社科书 SEO 需求低，可接受 |
| Tailwind CDN 体积 | ~300KB JS（Play 模式） | 生产环境可用 Tailwind CLI 构建精简 |
| 中文首屏字体 | Noto Serif SC 需从 Google Fonts 加载 | 有 fallback 字体兜底 |
| 无评论/批注 | 纯阅读，无社交功能 | 可后续集成 Giscus |

---

## 7. 与其他风格方案的对比

| 维度 | 本风格（book_design_style） | VitePress | Docsify | Notion-style |
|------|---------------------------|-----------|---------|--------------|
| 定位 | 社科商业图书 | 技术文档 | 轻量文档 | 知识管理 |
| 配色 | Navy + Gold 商务 | Vue 绿 | 极简白 | Notion 灰 |
| 字体 | 衬线正文 | 无衬线 | 无衬线 | 无衬线 |
| 首页 | 英雄区+模型+金句 | 无首页 | 侧边栏 | 无首页 |
| 封面 | SVG 自动生成 | 无 | 无 | 无 |
| 交互 | Alpine.js 声明式 | Vue 组件 | 原生 JS | React |
| 构建 | 零构建 | 需 Vite 构建 | 零构建 | 需 React |
| 主题 | 深/浅双主题 | 深/浅 | 插件 | 深/浅 |
| 适用 | 社科/商业书 | 技术文档 | 简单文档 | 笔记/文档 |
| 复用成本 | 复制配色+CDN | 全新项目 | 全新项目 | 全新项目 |

**结论**：本风格在"社科商业图书网页化"这一细分场景下，比通用文档方案更有针对性——它有书籍封面、金句墙、核心模型卡片、作者介绍等**书籍特有元素**，通用文档工具不提供这些。

---

## 8. 存储路径与命名规范

### 8.1 本文档路径

```
docs/skills/book_design_style.md
```

### 8.2 命名规范

| 规则 | 说明 | 示例 |
|------|------|------|
| 目录 | `docs/skills/` | 所有技能文档统一存放 |
| 文件名 | `{领域}_{设计类型}_{风格名}.md` | `book_design_style.md` |
| 命名风格 | 英文 snake_case | `book_design_style` |
| 版本标识 | 文档头部 `版本：vX.Y` | `版本：v1.0` |
| 来源标识 | 文档头部 `来源项目：` | 便于追溯实际项目 |

### 8.3 后续扩展命名

| 预期技能 | 文件名 |
|----------|--------|
| 技术文档风格 | `tech_doc_design_style.md` |
| 文学作品风格 | `literature_design_style.md` |
| 儿童读物风格 | `kids_book_design_style.md` |
| 通用卡片布局 | `card_layout_pattern.md` |

---

## 9. 检索与调用方式

### 9.1 检索

在项目根目录搜索技能文档：
```bash
# �"社科"或"图书"相关技能
grep -rl "社科\|图书" docs/skills/

# 按配色检索
grep -rl "navy.*gold" docs/skills/
```

### 9.2 调用

新项目复用时，按 §5.1 的最小化复用步骤执行，仅需替换 §5.2 中的改动点。

---

## 10. 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-08-27 | 初始版本，从《权力》项目提炼 |