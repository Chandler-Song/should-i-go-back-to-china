# 《我应该回国吗？》网页书 — 任务分解文档（tasks.md）

> 版本：v1.0  
> 创建日期：2026-09-07  
> 依据：`design.md` + `spec.md`  
> 执行顺序：T1 → T2 → ... → T10，每步完成后进入下一步

---

## 任务总览

| 任务 | 内容 | 产物 | 预计复杂度 |
|------|------|------|-----------|
| T1 | 项目骨架与目录 | `index.html` 空壳 + `assets/` 目录 | 低 |
| T2 | 章节元数据 | `assets/js/chapters.js` | 低 |
| T3 | 封面 SVG | `assets/images/cover.svg` | 低 |
| T4 | 排版样式 | `assets/css/book.css` | 中 |
| T5 | 首页 HTML 结构 | `index.html` 首页七区块 | 中 |
| T6 | 阅读视图 HTML 结构 | `index.html` 阅读视图 | 中 |
| T7 | Alpine 交互逻辑 | `assets/js/app.js` | 高 |
| T8 | 深色模式样式补全 | `book.css` 深色覆盖 | 中 |
| T9 | 本地测试验证 | 启动服务器 + 逐项验收 | 中 |
| T10 | 修复与打磨 | 修复测试发现的问题 | 低 |

---

## T1 项目骨架与目录

**目标**：建立文件结构，引入 CDN，配置 Tailwind。

**步骤**：
1. 创建 `assets/css/`、`assets/js/`、`assets/images/` 目录
2. 创建 `index.html`，在 `<head>` 引入：
   - Tailwind Play CDN + 内联 `tailwind.config`（navy/gold/ink 色阶 + serif/sans 字体）
   - Alpine.js 3.14.1（defer）
   - marked.js 12.0.2（defer）
   - Google Fonts：Noto Serif SC + Noto Sans SC
   - `assets/css/book.css`
   - `assets/js/chapters.js`（defer）
   - `assets/js/app.js`（defer）
3. `<body>` 加 `<div x-data="bookApp()">` 根容器，留待 T5/T6 填充

**验收**：浏览器打开 `index.html`（经 HTTP 服务器），无控制台错误，Tailwind 生效（可用 `class="text-navy-600"` 验证）。

---

## T2 章节元数据

**目标**：建立 40 章 + 9 篇元数据。

**步骤**：
1. 创建 `assets/js/chapters.js`
2. 定义 `PARTS` 数组（9 篇，含 id/name/range）
3. 定义 `CHAPTERS` 数组（40 条，含 id/part/file/title），file 与 `gobackchina/` 下实际文件名一一对应

**file 字段映射**（从 `gobackchina/` 实际文件名提取）：
```
01 ch01_overview_and_era_context.md
02 ch02_tier1_tech_giants.md
03 ch03_tier2_tech_giants.md
04 ch04_tier3_vertical_leaders.md
05 ch05_ai_unicorns_and_startups.md
06 ch06_chip_semiconductor.md
07 ch07_foreign_companies_in_china.md
08 ch08_academia_talent_programs.md
09 ch09_compensation_system_deep_dive.md
10 ch10_level_mapping_overseas_domestic.md
11 ch11_salary_negotiation.md
12 ch12_equity_long_term_return.md
13 ch13_tier1_cities_compare.md
14 ch14_new_tier1_cities.md
15 ch15_housing_purchase_model.md
16 ch16_living_cost_full_calculate.md
17 ch17_livability_personal_weighting.md
18 ch18_children_education_international_schools.md
19 ch19_marriage_social_rebuild.md
20 ch20_hukou_social_security_legal.md
21 ch21_online_info_collection.md
22 ch22_network_referral_strategy.md
23 ch23_interview_research_method.md
24 ch24_headhunter_guide.md
25 ch25_psychology_decision_models.md
26 ch26_motivation_deep_analysis.md
27 ch27_overcome_resistance.md
28 ch28_culture_shock_reverse.md
29 ch29_timing_multi_factor.md
30 ch30_success_cases.md
31 ch31_failure_cases.md
32 ch32_llm_impact_on_engineers.md
33 ch33_coder_unemployment_wave.md
34 ch34_market_severity_analysis.md
35 ch35_core_competency_reshape.md
36 ch36_checklist_90_days.md
37 ch37_resume_localization.md
38 ch38_interview_preparation.md
39 ch39_visa_archive_legal.md
40 ch40_financial_tax_cross_border.md
```

**title 字段**：从 README "全书目录" 提取各章标题（去掉"第 XX 章"前缀）。

**验收**：`console.log(CHAPTERS.length)` 为 40，`PARTS.length` 为 9，每条 file 对应文件存在。

---

## T3 封面 SVG

**目标**：生成 `assets/images/cover.svg`。

**参数**（遵循 design §8）：
- 画布 600×840
- 背景 Navy 渐变 `#15293f → #0a1521`（纵向）
- 双线边框：外框 3px gold `#b8860b`，内框 1px gold，间距 12px
- 书名"我应该回国吗？"居中，130px，金色渐变 `#d4a843 → #b8860b`
- 副标题"Should I Go Back to China?"，24px，navy-200 `#adc2d9`
- 作者"宋秀强"，18px，navy-300 `#84a3c7`
- 装饰语"硅谷工程师回国决策手册"，13px，navy-400 `#5b84b5` 70% 透明

**验收**：浏览器打开 SVG 显示完整封面，文字不溢出边框。

---

## T4 排版样式

**目标**：创建 `assets/css/book.css`，实现 markdown 排版 + 深色覆盖。

**步骤**：
1. 按 design §9 写 `.markdown` 系列样式（h1-h3、p、blockquote、table、code、ul/ol、hr）
2. 写 `.dark .markdown` 深色覆盖（blockquote 背景、表头、斑马纹、code 背景）
3. 写阅读区容器、进度条、抽屉等辅助样式
4. 写响应式微调（移动端字号、间距）

**验收**：一段含表格/引用/列表的 markdown 渲染后，浅色与深色均清晰可读。

---

## T5 首页 HTML 结构

**目标**：在 `index.html` 写首页七区块（`x-show="view==='home'"`）。

**区块**：
1. **英雄区**：`grid md:grid-cols-2`，左侧封面 `<img>`，右侧书名 + 副标题 + 两个 CTA 按钮
2. **核心理念**：`max-w-3xl mx-auto` 卡片，一段话
3. **五因子模型**：`grid md:grid-cols-2 lg:grid-cols-3 gap-6`，5 张卡片
4. **金句墙**：同上布局，6-9 张金句卡片
5. **目录导航**：9 篇分组，每篇卡片含篇名 + 章节列表（`@click="openChapter(id)"`）
6. **作者介绍**：`flex md:flex-row`，左侧头像占位 + 右侧信息
7. **页脚**：居中文字

**数据**：
- 五因子、金句、作者信息硬编码在 HTML（内容固定）
- 目录导航用 `template x-for` 遍历 `PARTS` 和 `CHAPTERS`

**验收**：首页七区块完整显示，配色字体符合设计风格，目录章节可点击触发跳转。

---

## T6 阅读视图 HTML 结构

**目标**：在 `index.html` 写阅读视图（`x-show="view==='read'"`）。

**结构**：
1. **顶部固定栏**：`fixed top-0`，左返回按钮、中章节标题、右字号 + 主题按钮
2. **进度条**：`fixed top-0 h-1`，`:style="width: progress+'%'"`
3. **侧边目录**：
   - `lg:` 常驻 `fixed left-0 w-60`
   - `<lg` 抽屉 `:class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"` + 遮罩层
   - 汉堡按钮（`<lg` 显示）触发 `sidebarOpen=true`
4. **阅读区**：`max-w-[720px] mx-auto`，`x-html="currentHtml"` 渲染章节
5. **底部翻页**：上一章 / 下一章按钮

**验收**：切换到阅读视图，结构完整，侧边目录列出 40 章。

---

## T7 Alpine 交互逻辑

**目标**：在 `assets/js/app.js` 实现 `bookApp()` 组件。

**方法**：
1. 定义 `bookApp()` 返回状态 + 方法（按 design §7.1）
2. `init()`：从 localStorage 恢复 fontSize/theme；应用主题 class；监听 hashchange；解析初始 hash
3. `goHome()`：`location.hash = ''`
4. `openChapter(id)`：`location.hash = '#/ch/' + id`
5. `handleHash()`：解析 hash，切换 view，调用 loadChapter
6. `loadChapter(id)`：
   - 设 currentChapter、view='read'
   - 查缓存命中则直接渲染，否则 fetch `gobackchina/{file}` → 等待 marked 就绪 → `marked.parse(text)` → 缓存 → 渲染
   - 渲染后 `setTimeout(preloadNext, 500)`
   - 存 localStorage `lastChapter`
   - 滚动到顶
7. `preloadNext(id)`：若未缓存则 fetch + parse + 缓存（不渲染）
8. `toggleTheme()`：切换 dark class + 存 localStorage
9. `setFont(delta)`：clamp 16-22 + 存 localStorage + 应用到阅读区
10. `onScroll()`：rAF 节流，计算 progress
11. `prevChapter()` / `nextChapter()`：边界检查后 openChapter
12. `randomChapter()`：随机 openChapter

**错误处理**：
- fetch 失败：阅读区显示错误提示 + 返回首页链接
- marked 未就绪：轮询 50ms 直到 `window.marked` 存在

**验收**：
- 点击章节加载并渲染
- 缓存章节秒切
- 主题/字号切换 + 刷新保持
- 进度条随滚动更新
- 翻页正确，首末章边界
- 直接访问 `#/ch/25` 打开第 25 章

---

## T8 深色模式样式补全

**目标**：确保深色模式下所有区块可读。

**步骤**：
1. 检查首页七区块在 `.dark` 下的配色（卡片底、文字、边框）
2. 检查阅读视图在 `.dark` 下的配色（顶栏、侧栏、阅读区）
3. 在 `book.css` 补充必要的 `.dark` 覆盖
4. 确保表格、引用、code 在深色下对比度足够

**验收**：深色模式下全站可读，无黑底黑字或白底白字。

---

## T9 本地测试验证

**目标**：启动本地服务器，逐项验证 spec §7 验收标准。

**步骤**：
1. 在项目根目录启动 `python -m http.server 8000`
2. 浏览器访问 `http://localhost:8000`
3. 逐项检查：
   - [ ] 首页七区块完整渲染
   - [ ] 配色字体符合设计风格（navy/gold/serif）
   - [ ] 点击第 01 章加载并渲染
   - [ ] markdown 表格/引用/列表正确显示
   - [ ] 深色切换正常，刷新保持
   - [ ] 字号 16-22 可调，刷新保持
   - [ ] 进度条随滚动更新
   - [ ] 上一章/下一章正确
   - [ ] 第 40 章无下一章
   - [ ] 移动端抽屉目录（浏览器 DevTools 模拟）
   - [ ] 直接访问 `#/ch/25` 打开第 25 章
   - [ ] 控制台无错误
4. 用脚本批量验证 40 章全部可 fetch（`curl` 或浏览器循环）

**验收**：全部检查项通过。

---

## T10 修复与打磨

**目标**：修复 T9 发现的问题，最终打磨。

**步骤**：
1. 修复测试中发现的问题
2. 检查移动端体验（字号、间距、抽屉）
3. 检查深色模式细节
4. 确认 40 章全部可加载
5. 清理控制台 warning

**验收**：全站无错误，体验流畅，交付完成。

---

## 依赖关系

```
T1 ─┬─ T2 ─┐
    │       ├─ T5 ─┐
    ├─ T3 ─┤       │
    └─ T4 ─┴─ T6 ─┴─ T7 ── T8 ── T9 ── T10
```

T1 是基础；T2/T3/T4 可并行；T5/T6 依赖 T1-T4；T7 依赖 T2/T5/T6；T8 依赖 T7；T9 依赖 T8；T10 依赖 T9。