# 前端设计优化规格（frontdesign_spec）

> 依据：`docs/frontdesign_review.md`
> 范围：**P0 全部（8 项）+ P1 全部（10 项）+ 低成本 P2（3 项）**；明确列出本期不做项
> 涉及文件：`index.html`、`assets/css/book.css`、`assets/js/app.js`
> 约束：纯原生单文件 + Alpine.js，不引入构建工具与图标库依赖；品牌基线 Navy(#1e3a5f) + Gold(#b8860b) 不变；改 JS/CSS 需升级 `?v=` 破缓存
> 日期：2026-09-09

---

## 0. 目标

1. 建立**统一的线性图标系统**与**动效令牌**，消除拼贴感
2. 补齐**可访问性硬约束**（aria 语义、prefers-reduced-motion）
3. 修正首页**视觉失衡**（英雄区、五因子警示卡）与**响应式隐患**（移动端顶栏、奇数目录）
4. 让动效承担叙事：章节切换过渡、滚动 reveal、沉浸三段编排

---

## 1. 设计令牌（写入 `book.css :root`）

```css
:root {
  /* 动效时长 */
  --motion-fast: 0.15s;   /* hover / active 反馈 */
  --motion-base: 0.25s;   /* 视图切换 / 抽屉 / 顶栏 */
  --motion-slow: 0.4s;    /* 章节 / 沉浸编排 / reveal */
  /* 缓动 */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
}
```

**规则**：全部 transition / animation 引用令牌，禁止裸写 `0.2s` `300ms` 等散乱值。

---

## 2. 图标系统规范

统一基线：`viewBox="0 0 24 24"`、`fill="none"`、`stroke="currentColor"`、`stroke-width="1.75"`、`stroke-linecap="round"`、`stroke-linejoin="round"`、`aria-hidden="true" focusable="false"`。渲染尺寸统一 **20×20**（阅读顶栏沉浸图标从 18 改 20）。SVG 一律加 `aria-hidden`，语义由按钮的 `aria-label` 承担。

| 名称 | 语义 | 使用位置 | SVG 核心路径 |
|---|---|---|---|
| `icon-moon` | 切换到深色 | 顶栏（theme==='light' 时显示） | `M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z` |
| `icon-sun` | 切换到浅色 | 顶栏（theme==='dark' 时显示） | `circle r=4` + 8 条光线 |
| `icon-warn` | 警示/最短板 | 五因子 banner | 三角 + 感叹号（Lucide triangle-alert） |
| `icon-more` | 更多菜单 | 阅读顶栏移动端 | 三个实心圆点（fill） |
| `icon-back` | 返回 | 沿用现有箭头 | `M19 12H5M12 19l-7-7 7-7` |
| `icon-menu` | 目录 | 沿用现有三横线 | `M3 12h18M3 6h18M3 18h18` |
| `icon-close` | 关闭 | 沿用现有 X | `M18 6L6 18M6 6l12 12` |
| `icon-immersive` | 沉浸 | 沿用现有四角 | 现有 path 不变，尺寸 20 |
| `icon-prev/next` | 翻页 | 沿用现有箭头 | 不变 |
| `icon-github` | 外链 | 品牌例外，保留实心 fill | 不变 |

**替代的 emoji**：`🌙` `☀️`（主题）、`⚠`（五因子）——全部改为上表 SVG。

---

## 3. 变更清单

### 3.1 图标统一（P0）

| # | 位置 | 改法 |
|---|---|---|
| I-1 | 首页/阅读顶栏主题按钮 | emoji → `icon-moon` / `icon-sun` 二态（`x-show` 切换） |
| I-2 | 五因子警示 | `⚠` → `icon-warn`，`text-gold`，置于 Navy 全宽 banner 内 |
| I-3 | 沉浸图标 | 18×20 → 20×20 |

### 3.2 可访问性（P0）

| # | 位置 | 改法 |
|---|---|---|
| A-1 | 全部 `icon-btn` | 补 `aria-label`（返回首页/打开目录/缩小字号/放大字号/沉浸阅读/切换主题/关闭目录/更多设置） |
| A-2 | 沉浸按钮 | `:aria-pressed="immersive"` |
| A-3 | 目录按钮 | `:aria-expanded="sidebarOpen"` `aria-controls="mobile-toc"`；抽屉 aside 加 `id="mobile-toc"` |
| A-4 | 所有内联 SVG | `aria-hidden="true" focusable="false"` |

### 3.3 动效（P0 + P1）

| # | 名称 | 改法 |
|---|---|---|
| M-1 | reduced-motion 兜底 | `book.css` 末尾加 `@media (prefers-reduced-motion: reduce)` 全局禁用动画/过渡/smooth 滚动 |
| M-2 | 章节切换过渡 | 新增 `@keyframes fadeUp` + `.chapter-enter`；`app.js` 在 `loadChapter` 设置内容后对 `.markdown` 容器 remove/reflow/add 重播动画 |
| M-3 | 卡片 hover 分层 | `.card` 仅阴影微调不上浮；新增 `.card-interactive`（translateY(-2px)）仅用于可点击卡片（首页目录卡）；金句卡 hover 只加左边框粗细变化 |
| M-4 | 按钮 active | `.btn-primary:active` `scale(0.98)`；`.icon-btn:active` `scale(0.92)`，时长 `--motion-fast` |
| M-5 | 滚动 reveal | 新增 `.reveal` / `.reveal-group`（`@keyframes fadeUp` + `animation-delay` 错峰 60ms×n，cap 300ms）；`app.js` init 后用 `IntersectionObserver`（threshold 0.08）加 `.reveal-visible`，不支持则直接显示 |
| M-6 | 沉浸三段编排 | 进入：顶栏 0ms → 侧栏 delay 100ms → 文章 delay 200ms；退出同步恢复（顶栏唤出不受延迟影响） |
| M-7 | 沉浸阅读宽度 | 非沉浸 720px 不变，沉浸 680→**620px**；`.immersive .markdown { line-height:1.9 !important; letter-spacing:.01em }` |
| M-8 | 进度条跟手 | `transition: width .1s linear` → `transition: none`（rAF 已节流） |
| M-9 | 令牌统一 | 卡片/按钮/icon/链接/抽屉等全部 transition 引用令牌 |
| M-10 | 品牌 spinner | 通用 border spinner → `.brand-spinner`：Gold 弧 + 25% Gold 轨道 |

### 3.4 布局（P0 + P1）

| # | 名称 | 改法 |
|---|---|---|
| L-1 | 英雄区封面 | `max-w-sm` → `max-w-xs md:max-w-md`；`shadow-2xl` → `shadow-md ring-1 ring-gold/20` |
| L-2 | 五因子警示卡 | 与因子卡同格 → `md:col-span-2 lg:col-span-3` 全宽 Navy banner + Gold `icon-warn` |
| L-3 | 目录 9 部分 | `md:grid-cols-2` → `md:grid-cols-2 lg:grid-cols-3`；章节行距 `space-y-1/py-1.5` → `space-y-1.5/py-2` |
| L-4 | 阅读顶栏移动端 | 字号组/沉浸/GitHub/百分比在 `<md` 折叠进"更多"菜单（`moreOpen` 状态 + `@click.outside`）；主题按钮常驻；桌面不变 |
| L-5 | 移动抽屉 | `w-72` → `w-[85%] max-w-xs`；遮罩 `bg-black/50` → `bg-black/60` |
| L-6 | 翻页间距 | `mt-16 pt-8` → `mt-12 pt-6` |
| L-7 | 作者头像 | 渐变 → `bg-navy-600 ring-2 ring-gold/40`；统计数字 `text-2xl` → `text-xl md:text-2xl` |
| L-8 | backdrop-blur 抖动 | `.read-header` 加 `will-change: transform` |

### 3.5 低成本 P2

| # | 名称 | 改法 |
|---|---|---|
| X-1 | 进度百分比 | 桌面阅读顶栏 GitHub 前显示 `Math.round(progress)%`（`hidden md:inline`）；更多菜单顶部也显示 |
| X-2 | 页脚反馈入口 | 补 GitHub Issues 链接一行 |
| X-3 | favicon / og | `<link rel="icon" type="image/svg+xml" href="assets/images/cover.svg">`；og:title/description/image（指向 GitHub Pages 绝对地址 cover.png）+ `twitter:card` |

---

## 4. 本期不做项（范围外）

- 章节内小节迷你目录（P2，涉及标题锚点扫描）
- 移动端沉浸顶栏下拉手势唤出（P2，手势状态机较重）
- 首屏骨架屏 / 全局加载进度条（P2，需评估 CDN 预加载策略）
- 阅读位置恢复平滑过渡（P2）
- 翻页"读完本章"庆祝动效（P2）
- Tailwind CDN 本地化、字体子集化（性能专项，另行立项）

---

## 5. 涉及文件与缓存版本

| 文件 | 变更类型 | 缓存版本 |
|---|---|---|
| `index.html` | 图标/布局/aria/meta | — |
| `assets/css/book.css` | 令牌/动画/reveal/沉浸编排 | `?v=20260909-3` |
| `assets/js/app.js` | reveal 观察器/章节动画/moreOpen | `?v=20260909-3` |

---

## 6. 验收标准

1. **语法**：`node --check assets/js/app.js` 通过
2. **功能**：本地 `python -m http.server` 启动后——首页→阅读→沉浸→切章→返回全链路正常；更多菜单开合正常
3. **图标**：页面无 emoji 图标（🌙☀️⚠ 全部消失）；所有图标按钮有 aria-label
4. **动效**：系统开启"减弱动态效果"后无任何过渡/动画；关闭后 reveal、章节 fadeUp、沉浸三段编排正常
5. **布局**：375px 宽度下阅读顶栏不溢出、不换行；目录 3 列整齐；沉浸宽度明显收窄
6. **缓存**：css/js 引用均为 `?v=20260909-3`