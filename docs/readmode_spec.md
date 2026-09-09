# 沉浸式阅读模式优化规格（readmode_spec.md）

> 版本：v2.0
> 日期：2026-09-09
> 依据：`docs/readmode_review.md` v2.0（用户反馈：v1.0 的 dock/peek/popover/hint 设计影响阅读）
> 关联设计：`docs/reading_experience_design.md` §4、`docs/frontdesign_spec.md`（动效令牌 / reduced-motion）
> 涉及文件：`index.html`、`assets/css/book.css`、`assets/js/app.js`
> 约束：纯原生单文件 + Alpine.js；品牌基线 Navy(#1e3a5f) + Gold(#b8860b) 不变；纸感护眼配色不变；改 JS/CSS 需升 `?v=` 破缓存；所有动效遵守 `prefers-reduced-motion`

---

## 0. 目标（一句话）

**沉浸但不藏导航**——沉浸模式下顶部栏**固定常驻、不隐藏**，所有功能（目录 / 首页 / 作者 / 字号 / 主题 / 沉浸 / GitHub）都在顶栏里随时可用；删除 v1.0 的底部 Floating Dock、左缘 peek 区、作者浮卡、首次引导提示等「隐形触发区」与「浮层」，避免入口分散影响阅读。字号范围 **10–20**，默认进入 **14**。

---

## 1. 与 v1.0 的差异（为什么重做）

| 项 | v1.0 做法 | v1.0 问题 | v2.0 做法 |
|----|----------|----------|----------|
| 顶栏 | 沉浸时 `translateY(-100%)` 滑出，顶部 44px hover 唤出 | 入口在「隐形触发区」里，不发现就等于没有；新读者找不到导航 | **固定常驻，不隐藏** |
| 底部 Floating Dock | 6 图标胶囊坞常驻 | 入口分散在底部，与顶栏重复；占据底部视觉；移动端 6 图标拥挤 | **删除** |
| 左缘 peek 区 | 12px 隐形条带 hover 唤出侧栏 | 又一个隐形触发区，零视觉提示 | **删除** |
| 作者浮卡 | dock 上方弹出半透明卡片 | 浮层多一层，打断阅读 | **删除**，顶栏新增作者按钮 → `goAuthor()` 回首页作者区 |
| 首次引导提示 | toast 提示「按 Esc / 鼠标移顶部」 | 既然顶栏固定，提示无意义 | **删除** |
| 字号范围 | 16–24，默认 18（移动 17） | 偏大 | **10–20，默认 14** |
| 沉浸聚焦感 | 顶栏隐藏 + 侧栏隐藏 + 宽度 680 | 聚焦靠「藏」 | 侧栏隐藏 + 宽度 680 + 行距 1.9（顶栏保留，聚焦靠宽度与侧栏） |

---

## 2. 范围

### 2.1 本期做

| 编号 | 方案 | 优先级 |
|------|------|--------|
| FR-1 | 顶栏固定常驻（沉浸不隐藏） | P0 |
| FR-2 | 删除 Floating Dock / 左缘 peek / 作者浮卡 / 引导提示 | P0 |
| FR-3 | 顶栏补齐功能：作者按钮 + 沉浸时桌面目录按钮可见 | P0 |
| FR-4 | 沉浸时桌面侧栏点击唤出（`sidebarShow` toggle） | P0 |
| FR-5 | 字号范围 10–20，默认 14 | P0 |
| FR-6 | 沉浸阅读宽度 680px、翻页 opacity .35、进度条 2px、行距 1.9（保留 v1.0 已落地的可读性微调） | P1 |

### 2.2 本期不做

- 沉浸下全文搜索（维持既有排除决策）
- 沉浸下书签 / 笔记（超出阅读器定位）
- 语音朗读 / 自动翻页
- 不改首页作者区块视觉
- 不改非沉浸模式任何行为（顶栏、侧栏、字号边界同步调整除外）

---

## 3. 功能需求（FR 编号）

### FR-1 顶栏固定常驻（沉浸不隐藏）

**来源**：用户反馈「保留顶部栏，虽然是沉浸阅读，但是顶部栏仍然可用，是固定的」

| 编号 | 需求 | 验收 |
|------|------|------|
| FR-1.1 | 沉浸模式下顶栏 `.read-header` 不再添加 `bar-hidden` 类，保持 `position: fixed; top:0` 常驻可见 | 沉浸时顶栏始终可见 |
| FR-1.2 | 删除顶部 44px hover 唤出区 `.top-zone` 的沉浸专属 `pointer-events` 逻辑与 `barVisible` 状态驱动的显隐 | 顶栏不再因 hover 显隐 |
| FR-1.3 | 顶栏视觉与非沉浸一致：`bg-white/95 dark:bg-slate-900/95 backdrop-blur` + 底边分隔线 | 沉浸与非沉浸顶栏外观一致 |
| FR-1.4 | 阅读区顶部 `pt-16` 保留（为固定顶栏留出空间），沉浸时不因顶栏隐藏而调整 | 内容不被顶栏遮挡 |

---

### FR-2 删除 v1.0 的浮层与隐形触发区

| 编号 | 需求 | 验收 |
|------|------|------|
| FR-2.1 | 删除 `.floating-dock` 元素、样式、`dock-tr/dock-from/dock-to` 过渡类 | 页面无 dock 元素与样式 |
| FR-2.2 | 删除 `.left-peek-zone` 元素、样式、`sidebarPeek` 状态 | 页面无 peek 元素与样式 |
| FR-2.3 | 删除 `.author-popover` 元素、样式、`popover-*` 过渡类、`authorOpen` 状态 | 页面无作者浮卡 |
| FR-2.4 | 删除 `.immersive-hint` 元素、样式、`hint-*` 过渡类、`showImmersiveHint` 状态与 `maybeShowImmersiveHint()` 方法、`localStorage['book-immersive-hint']` | 页面无引导提示 |
| FR-2.5 | 删除 JS 中 `dockToc/dockHome/dockAuthor/dockFont` 方法 | 无 dock 相关方法 |
| FR-2.6 | 沉浸下阅读区底部 `padding-bottom` 不再为 dock 预留 72px（改回默认） | 翻页卡片正常贴底 |

---

### FR-3 顶栏补齐功能

**来源**：用户反馈「各个功能都有」

| 编号 | 需求 | 验收 |
|------|------|------|
| FR-3.1 | 顶栏新增「作者」图标按钮，点击调用 `goAuthor()`（退出沉浸 + 回首页作者区） | 顶栏有作者按钮，点击跳到首页作者区 |
| FR-3.2 | 顶栏「目录」按钮：移动端始终可见（打开抽屉）；桌面端**仅沉浸时可见**（唤出侧栏），非沉浸时 `lg:hidden`（有常驻侧栏） | 非沉浸桌面无目录按钮（有常驻侧栏），沉浸桌面有目录按钮 |
| FR-3.3 | 顶栏现有功能在沉浸时全部保留可用：返回首页、字号 A-/A+、沉浸开关、进度、主题、GitHub、更多（移动） | 沉浸时顶栏所有按钮可点 |
| FR-3.4 | 作者按钮位置：放在「主题」与「GitHub」之间，图标用 `icon-user`，`aria-label="作者介绍"` | 位置与无障碍标签符合 |

---

### FR-4 沉浸时桌面侧栏点击唤出

| 编号 | 需求 | 验收 |
|------|------|------|
| FR-4.1 | 新增 Alpine 状态 `sidebarShow: false`，控制沉浸时桌面侧栏显隐 | 状态存在且默认 false |
| FR-4.2 | 顶栏目录按钮点击调用 `openToc()`：桌面端（`innerWidth >= 1024`）toggle `sidebarShow`；移动端 `sidebarOpen = true` | 桌面点击 toggle 侧栏，移动打开抽屉 |
| FR-4.3 | 桌面侧栏沉浸时：`sidebarShow` 为 true 则 `translateX(0)` 显示，否则 `translateX(-105%)` 隐藏；用 `.sidebar-show` 类驱动 | 沉浸时侧栏可显可隐 |
| FR-4.4 | 非沉浸时桌面侧栏保持常驻（`hidden lg:block`），不受 `sidebarShow` 影响 | 非沉浸侧栏常驻不变 |
| FR-4.5 | 切换章节 / 退出沉浸时 `sidebarShow` 重置为 false | 切章/退出后侧栏回到隐藏 |
| FR-4.6 | `Esc` 键优先级：关抽屉 `sidebarOpen` → 关桌面侧栏 `sidebarShow` → 退出沉浸 | Esc 逐级关闭 |

---

### FR-5 字号范围 10–20，默认 14

**来源**：用户反馈「字体是设计范围是10-20，默认进入是14大小」

| 编号 | 需求 | 验收 |
|------|------|------|
| FR-5.1 | `fontSize` 初始值从 18（移动 17）改为 **14**，不再区分移动端 | 首次进入阅读区字号 14px |
| FR-5.2 | `setFont(delta)` 边界从 `16 ≤ next ≤ 24` 改为 **`10 ≤ next ≤ 20`** | 字号不能调出 10–20 |
| FR-5.3 | 顶栏字号按钮 `:disabled` 边界同步：A- 在 `fontSize <= 10` 禁用，A+ 在 `fontSize >= 20` 禁用 | 边界按钮正确禁用 |
| FR-5.4 | 顶栏字号数字显示 `fontSize` 当前值 | 显示 10–20 之间 |
| FR-5.5 | `lineHeight` 计算：`fontSize >= 16 ? 1.8 : 1.85`（小字号行距稍宽） | 行距随字号合理变化 |
| FR-5.6 | 已有用户 `localStorage['book-fontsize']` 若超出 10–20，init 时 clamp 回区间内 | 旧值越界自动收敛 |

---

### FR-6 沉浸可读性微调（保留 v1.0 已落地项）

| 编号 | 需求 | 验收 |
|------|------|------|
| FR-6.1 | `.immersive .read-article { max-width: 680px }` 保留 | 沉浸阅读区 680px |
| FR-6.2 | `.immersive .chapter-nav { opacity: .35 }` + hover 恢复 1 + 上方 Gold 渐变暗示线，保留 | 翻页卡片可见性符合 |
| FR-6.3 | `.immersive .reading-progress { height: 2px }` 保留 | 进度条沉浸时 2px |
| FR-6.4 | `.immersive .markdown { line-height: 1.9 !important; letter-spacing: .01em }` 保留 | 沉浸行距舒展 |
| FR-6.5 | 沉浸时桌面侧栏隐藏（`translateX(-105%)`），由 `sidebarShow` 控制唤出 | 沉浸默认无侧栏，点击唤出 |

---

## 4. 非功能需求（NFR）

| 编号 | 需求 |
|------|------|
| NFR-1 | **品牌守恒**：Navy + Gold 不变，纸感护眼配色不变，不引入新色 |
| NFR-2 | **动效令牌**：保留的过渡引用 `frontdesign_spec.md` 令牌，禁止裸写时长 |
| NFR-3 | **减弱动效兼容**：保留的动效受 `@media (prefers-reduced-motion: reduce)` 兜底 |
| NFR-4 | **可访问性**：顶栏所有图标按钮补 `aria-label`；作者按钮 `aria-label="作者介绍"`；目录按钮 `aria-expanded` |
| NFR-5 | **回归不破坏**：非沉浸模式完全不受影响；首页、主题、字号、进度条、断点续看、hash 路由、章节预加载全部正常 |
| NFR-6 | **缓存破除**：`book.css` 与 `app.js` 引用升 `?v=20260909-8` |

---

## 5. 状态机与交互

### 5.1 Alpine 状态（app.js）

| 状态 | 默认 | 说明 | v1.0 → v2.0 |
|------|------|------|-------------|
| `immersive` | `false` | 沉浸模式 | 保留 |
| `sidebarOpen` | `false` | 移动端抽屉目录 | 保留 |
| `sidebarShow` | `false` | 桌面沉浸时点击唤出侧栏 | **新增** |
| `moreOpen` | `false` | 移动端「更多」菜单 | 保留 |
| `fontSize` | `14` | 当前字号 | **改**（原 18） |

**删除的状态**：`barVisible`、`sidebarPeek`、`authorOpen`、`showImmersiveHint`、`_hintTimer`、`authorMeta`（作者浮卡数据，顶栏作者按钮直接 `goAuthor()` 不需要浮卡数据）。

### 5.2 键盘快捷键

| 键 | 动作 | 说明 |
|----|------|------|
| `Esc` | 关抽屉 → 关桌面侧栏 → 退出沉浸 | 逐级关闭 |
| `I` | 切换沉浸 | 原有，保持 |
| `←/→` | 翻章 | 原有，保持 |

**删除的快捷键**：`T`（目录，改由顶栏按钮）、`H`（首页，顶栏返回箭头）、`A`（作者浮卡，改顶栏作者按钮）。

### 5.3 沉浸模式下可见元素

```
┌─────────────────────────────────────────────────────┐
│ ← ☰  第 03 章 …    A- 14 A+  ⤢  ☀  👤  GitHub  │ ← 顶栏固定常驻
├─────────────────────────────────────────────────────┤
│                                                      │
│            沉浸正文区（680px 居中）                  │
│            纸感护眼配色 · 行高 1.9                   │
│                                                      │
│                                                      │
│            ─── 上一章 / 下一章 ───                  │
│  ──────────── Gold 渐变进度条 (2px) ────────────    │
└─────────────────────────────────────────────────────┘
```

顶栏就是导航，不再有任何浮层 / 隐形触发区 / 底部 dock。

---

## 6. 视觉规格

### 6.1 顶栏（沉浸与非沉浸一致）

| 项 | 值 |
|----|----|
| 定位 | `position: fixed; top: 0; left: 0; right: 0; z-index: 50` |
| 背景 | `bg-white/95 dark:bg-slate-900/95` + `backdrop-blur` |
| 底边 | `border-b border-slate-200 dark:border-slate-700` |
| 高度 | 约 56px（`py-3` + 内容） |

### 6.2 顶栏按钮清单（沉浸时全部可见可用）

| 按钮 | 桌面 | 移动 | 行为 |
|------|------|------|------|
| 返回首页 `←` | ✅ | ✅ | `goHome()` |
| 目录 `☰` | ✅（沉浸）/ ❌（非沉浸，有常驻侧栏） | ✅ | `openToc()` |
| 章节标题 | ✅ | ✅ | 显示当前章节 |
| A- / 字号 / A+ | ✅ | ❌（收进「更多」） | `setFont(±1)`，边界 10–20 |
| 沉浸开关 `⤢` | ✅ | ❌（收进「更多」） | `toggleImmersive()` |
| 进度 `%` | ✅ | ❌（收进「更多」） | 显示 |
| 主题 `☀/☾` | ✅ | ✅ | `toggleTheme()` |
| 作者 `👤` | ✅ | ✅ | `goAuthor()`（**新增**） |
| GitHub | ✅ | ❌（收进「更多」） | 外链 |
| 更多 `⋮` | ❌ | ✅ | 展开移动端菜单 |

### 6.3 配色（沿用品牌令牌，无新增）

顶栏沿用既有纸感护眼配色，无新增色。翻页 Gold 渐变暗示线、进度条 Gold 沿用。

### 6.4 动效（沿用 `frontdesign_spec.md` 令牌）

| 动作 | 时长 | 缓动 |
|------|------|------|
| 侧栏滑入/滑出 | `--motion-base` (0.25s) | `--ease-out` |
| 翻页卡片 opacity | `--motion-base` | `--ease-out` |
| 阅读区宽度过渡 | `--motion-slow` (0.4s) | `--ease-in-out` |

全部受 `@media (prefers-reduced-motion: reduce)` 兜底禁用。

---

## 7. 实施清单

| 文件 | 改动 | 关联 FR |
|------|------|---------|
| `index.html` | ① 删除 `.floating-dock` 整块 ② 删除 `.left-peek-zone` ③ 删除 `.author-popover` 整块 ④ 删除 `.immersive-hint` ⑤ 顶栏去掉 `bar-hidden` 绑定与 `.top-zone` hover ⑥ 顶栏目录按钮 `:class` 沉浸时桌面显示 ⑦ 顶栏新增作者按钮 ⑧ 顶栏字号 `:disabled` 边界改 10/20 ⑨ 桌面侧栏 `:class` 加 `sidebar-show` ⑩ 版本号升 `?v=20260909-8` | FR-1/2/3/4/5 |
| `assets/css/book.css` | ① 删除 `.top-zone` 沉浸规则 ② 删除 `.bar-hidden` ③ 删除 `.floating-dock/.dock-*/.dock-tr/.dock-from/.dock-to` ④ 删除 `.left-peek-zone` 与 `.sidebar-peek-show` ⑤ 删除 `.author-popover/.popover-*` ⑥ 删除 `.immersive-hint/.hint-*` ⑦ `.immersive .read-main` 去掉 `padding-bottom:72px` ⑧ 新增 `.immersive .read-sidebar.sidebar-show { transform: translateX(0) }` ⑨ 保留 680px / opacity .35 / 进度条 2px / 行距 1.9 | FR-1/2/4/6 |
| `assets/js/app.js` | ① 删除 `barVisible/sidebarPeek/authorOpen/showImmersiveHint/_hintTimer/authorMeta` 状态 ② 新增 `sidebarShow: false` ③ `fontSize` 默认 14 ④ `setFont` 边界 10–20 ⑤ `lineHeight` 调整 ⑥ init 时 clamp 旧字号到 10–20 ⑦ 删除 `dockToc/dockHome/dockAuthor/dockFont/maybeShowImmersiveHint` ⑧ 新增 `openToc()` ⑨ `toggleImmersive` 清理 `sidebarShow` ⑩ `loadChapter` 重置 `sidebarShow` ⑪ `onKeydown` 删除 T/H/A，Esc 加 `sidebarShow` ⑫ 删除 `book-immersive-hint` localStorage | FR-1/2/4/5 |

---

## 8. 验收标准

| # | 项 | 通过标准 |
|---|----|---------|
| 1 | 顶栏固定 | 沉浸模式下顶栏始终可见，不因鼠标位置变化 |
| 2 | 无浮层 | 页面无 dock / peek 区 / 作者浮卡 / 引导提示 |
| 3 | 顶栏功能齐全 | 沉浸时顶栏：返回首页 / 目录 / 字号 / 沉浸 / 主题 / 作者 / GitHub 全部可用 |
| 4 | 作者入口 | 顶栏点作者按钮 → 跳到首页作者区 |
| 5 | 桌面目录 | 沉浸时顶栏目录按钮可见，点击 toggle 侧栏；非沉浸时桌面无目录按钮（有常驻侧栏） |
| 6 | 移动目录 | 移动端顶栏目录按钮打开抽屉 |
| 7 | 字号范围 | A- 到 10 禁用，A+ 到 20 禁用；默认进入 14 |
| 8 | 字号持久化 | 刷新后字号保持；旧值越界自动 clamp |
| 9 | 沉浸宽度 | 阅读区 680px |
| 10 | 翻页可见 | 沉浸下翻页卡片 opacity .35，hover 恢复 1，上方 Gold 渐变线 |
| 11 | Esc | Esc 逐级关：抽屉 → 桌面侧栏 → 退出沉浸 |
| 12 | 回归 | 非沉浸模式完全不受影响；首页、主题、进度条、断点续看、hash 路由正常 |
| 13 | 品牌守恒 | Navy + Gold 不变，纸感护眼配色不变，无新色 |
| 14 | 语法 | `node --check assets/js/app.js` 通过 |
| 15 | 缓存 | css/js 引用均为 `?v=20260909-8` |

---

## 9. 一句话总结

> 沉浸的聚焦不该靠「把导航藏起来」，而应靠阅读宽度与侧栏收起。顶栏固定常驻、所有功能随手可用，删掉底部 dock、左缘 peek、作者浮卡、引导提示这些「隐形触发区」与「浮层」，阅读反而更专注——因为读者不再需要「找入口」。
