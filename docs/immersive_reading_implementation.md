# 沉浸式阅读模式实施记录（immersive_reading_implementation.md）

> 版本：v1.0  
> 日期：2026-09-08  
> 关联设计：`docs/reading_experience_design.md` §4（沉浸式阅读）、§6（侧边目录栏）  
> 改动文件：`assets/js/app.js`、`assets/css/book.css`、`index.html`  
> 资源版本号：`?v=20260908-2`

---

## 一、需求

1. 增加**沉浸式阅读模式**：隐藏左侧导航栏与顶栏，聚焦正文
2. 修复左侧导航中**章节 title 的左对齐**问题
3. 过程记录成文档存入 `docs/`

---

## 二、三个文件的现状分析

### 2.1 `assets/js/chapters.js`（数据层）

- 纯元数据：`PARTS`（9 篇）+ `CHAPTERS`（40 章，含 id/part/file/title），挂载到 `window`
- `title` 字段被目录按钮渲染，**数据本身无对齐问题**——对齐问题出在渲染层（见 2.3）
- 结论：本功能**无需改动**，仅作为目录渲染的数据源

### 2.2 `assets/js/app.js`（状态层）

- Alpine 组件，已有状态：`view / currentChapter / chapterCache / theme / fontSize / sidebarOpen / progress`
- 已有交互：hash 路由、按需加载 + 缓存 + 预加载、主题/字号持久化、键盘 ←/→/Esc
- **缺失**：无 `immersive` 沉浸状态，无对应持久化与快捷键
- 结论：需新增状态机 + `toggleImmersive()` + 键盘支持

### 2.3 `assets/css/book.css`（样式层）——左对齐根因

```css
/* 修改前 */
.sidebar-link {
  display: block;
  padding: .4rem .75rem;
  font-size: .875rem;
  ...
}
```

**根因**：章节项用 `<button>` 渲染，浏览器 UA 样式表对 button 默认 `text-align: center`。`.sidebar-link` 未显式设置 `text-align`，所以目录里的章节标题**实际是居中的**，且标题过长时整行撑开无截断。

**结论**：需显式 `text-align: left` + flex 布局 + 两行截断。

---

## 三、实现过程

### 3.1 左对齐修复（book.css + index.html）

**CSS**：`.sidebar-link` 改 flex 布局、显式左对齐、标题两行截断：

```css
.sidebar-link {
  display: flex;
  align-items: baseline;
  gap: .45rem;
  width: 100%;
  font-size: .84rem;
  line-height: 1.5;
  text-align: left;          /* ← 根因修复：覆盖 button UA 居中 */
}
.sidebar-link .chapter-title {
  display: -webkit-box;
  -webkit-line-clamp: 2;     /* 标题最多两行，超出省略 */
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

**顺带优化当前章指示**：废弃原"整块 navy 底白字"（视觉过重），改为设计文档 §6.2 的**金色竖条**方案：

```css
.sidebar-link.active {
  background: rgba(184,134,11,.08);
  color: #1e3a5f;
  font-weight: 600;
  box-shadow: inset 3px 0 0 #b8860b;   /* 左侧 3px 金竖条 */
}
```

**HTML**：目录按钮内的标题 `<span>` 加 `class="chapter-title"`（桌面侧栏 + 移动抽屉两处），序号 span 加 `flex-shrink-0`。

### 3.2 沉浸式阅读模式

#### 状态机（app.js）

| 项 | 实现 |
|----|------|
| 状态 | `immersive: false`、`barVisible: false` |
| 持久化 | `localStorage['book-immersive']`，`init()` 时恢复 |
| 切换 | `toggleImmersive()`：翻转状态 + 收起顶栏 + 写入存储 |
| 快捷键 | `I` 进入/退出；`Esc` 退出沉浸（原有关抽屉职责保留） |
| 作用域 | `onKeydown` 开头已有 `view !== 'read'` 守卫，首页不响应 |

#### HTML 结构（index.html）

```
阅读视图容器  :class="immersive ? 'immersive' : ''"     ← 沉浸类挂载点
├─ .top-zone（fixed 44px 顶部条带，@mouseenter/leave 控制 barVisible）
│   └─ header.read-header  :class="immersive && !barVisible ? 'bar-hidden' : ''"
├─ aside.read-sidebar（桌面常驻目录）
├─ main.read-main > article.read-article（阅读区）
│   └─ nav.chapter-nav（翻页）
└─ button.fab-toc（沉浸+移动端的悬浮目录圆钮）
```

顶栏新增沉浸按钮（全屏四角图标，tooltip "沉浸阅读 (I)"）。

#### CSS 行为（book.css）

| 元素 | 沉浸模式下 | 实现 |
|------|-----------|------|
| 顶栏 | `translateY(-100%)` 滑出 | `.bar-hidden` |
| 顶部唤出 | 鼠标移入顶部 44px 滑入顶栏，移出滑出 | `.top-zone` pointer-events 按需开启 |
| 桌面侧栏 | `translateX(-105%)` 滑出 | `.immersive .read-sidebar` |
| 阅读区左边距 | 取消 `lg:ml-64` 留白 | `.immersive .read-main`（`!important` 覆盖 Tailwind） |
| 阅读宽度 | 720px → **680px** | `.immersive .read-article` |
| 翻页卡片 | 透明度 0.15，hover 恢复 | `.immersive .chapter-nav` |
| 进度条 | 3px → 2px | `.immersive .reading-progress` |

**顶栏唤出防闪烁设计**：不用 CSS 兄弟选择器 hover 方案（隐藏的 header 与 zone 会互相争抢 hover 造成循环闪烁），改用 **Alpine `@mouseenter/@mouseleave` 显式状态 `barVisible`**，header 显隐由 `immersive && !barVisible` 单一表达式驱动，行为确定。

**移动端保底**：顶栏隐藏后汉堡按钮不可达，右下角新增悬浮目录圆钮 `.fab-toc`（仅 `immersive` 且 `<lg` 显示），点击唤出抽屉目录。

#### 缓存破坏

三个本地资源引用统一升版：`book.css / chapters.js / app.js?v=20260908-2`（python http.server 无 Cache-Control，沿用既有破缓存约定）。

---

## 四、改动清单

| 文件 | 改动 | 行为 |
|------|------|------|
| `assets/js/app.js` | +`immersive/barVisible` 状态；init 恢复；`toggleImmersive()`；onKeydown 支持 `I`/`Esc` | ~20 行 |
| `assets/css/book.css` | sidebar-link 左对齐 + 截断 + 金竖条；沉浸模式 8 条规则 + fab-toc | ~60 行 |
| `index.html` | 阅读容器沉浸类；top-zone 包裹顶栏；沉浸按钮；read-sidebar/read-main/read-article/chapter-nav 类名；chapter-title span；fab-toc；版本号 | ~15 处 |
| `assets/js/chapters.js` | **未改动**（数据层无对齐职责） | 0 |

---

## 五、验收标准

| # | 验收项 | 通过标准 |
|---|--------|----------|
| 1 | 左对齐 | 目录章节标题靠左对齐，长标题两行截断 |
| 2 | 当前章指示 | 左侧金色竖条 + 浅金底，深浅两态可读 |
| 3 | 进入沉浸 | 顶栏按钮或 `I` 键：顶栏/侧栏滑出，阅读区 680px 居中 |
| 4 | 唤出顶栏 | 沉浸中鼠标移到屏幕顶部 44px 内，顶栏滑入；移出滑出 |
| 5 | 退出沉浸 | `Esc` 或再次点击 `I`，全部恢复 |
| 6 | 持久化 | 沉浸状态刷新保持；仅在阅读视图生效 |
| 7 | 移动端 | 沉浸中右下角悬浮目录圆钮可唤出抽屉 |
| 8 | 回归 | 翻页、字号、主题、进度条、缓存加载、hash 路由不受影响 |

---

## 六、注意事项

1. **验证需强制刷新一次（Ctrl+F5）**：即使有 `?v=` 版本号，首次访问仍在旧页面的标签页不会自动更新
2. 沉浸模式在首页不生效（类挂在阅读视图容器上），符合"阅读体验"定位
3. `read-main` 的 `margin-left: 0 !important` 用于覆盖 Tailwind `lg:ml-64`，若后续调整侧栏宽度需同步检查