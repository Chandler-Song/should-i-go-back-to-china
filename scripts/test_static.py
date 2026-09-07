import os
import re
import sys

ROOT = r"C:\Users\Administrator\IDEProjects\gotochina"
errors = []
ok_count = 0

def ok(msg):
    global ok_count
    ok_count += 1
    print(f"  [OK] {msg}")

def fail(msg):
    errors.append(msg)
    print(f"  [FAIL] {msg}")

print("=" * 60)
print("静态资源完整性验证（文件系统）")
print("=" * 60)

# 1. 核心文件存在
print("\n[1] 核心文件存在性")
for f in ["index.html", "assets/css/book.css", "assets/js/chapters.js",
          "assets/js/app.js", "assets/images/cover.png"]:
    p = os.path.join(ROOT, f)
    if os.path.isfile(p) and os.path.getsize(p) > 0:
        ok(f"{f} ({os.path.getsize(p)}B)")
    else:
        fail(f"{f} 缺失或为空")

# 2. 40章markdown存在
print("\n[2] 40章原稿存在性")
import glob
ch_files = sorted(glob.glob(os.path.join(ROOT, "gobackchina", "ch*.md")))
if len(ch_files) == 40:
    ok(f"共 {len(ch_files)} 个章节文件")
else:
    fail(f"章节文件数 {len(ch_files)}，预期 40")
for p in ch_files:
    if os.path.getsize(p) < 100:
        fail(f"{os.path.basename(p)} 过小")

# 3. chapters.js 中的 file 字段与实际文件匹配
print("\n[3] chapters.js file 字段与实际文件匹配")
with open(os.path.join(ROOT, "assets/js/chapters.js"), encoding="utf-8") as f:
    js = f.read()
file_matches = re.findall(r"file:\s*'([^']+)'", js)
id_matches = re.findall(r"id:\s*'(\d{2})'", js)
part_matches = re.findall(r"part:\s*(\d+)", js)
if len(file_matches) == 40:
    ok(f"chapters.js 含 {len(file_matches)} 条章节")
else:
    fail(f"chapters.js 章节条数 {len(file_matches)}，预期 40")

actual_basenames = set(os.path.basename(p) for p in ch_files)
for fm in file_matches:
    if fm in actual_basenames:
        pass
    else:
        fail(f"chapters.js 引用 {fm} 但文件不存在")
if all(fm in actual_basenames for fm in file_matches):
    ok("所有 file 字段对应文件均存在")

if len(id_matches) == 40:
    ok(f"40 个 id: {id_matches[0]}..{id_matches[-1]}")
else:
    fail(f"id 数 {len(id_matches)}")

if len(part_matches) == 40:
    ok(f"40 个 part 字段")
else:
    fail(f"part 数 {len(part_matches)}")

# 4. index.html 引用资源正确
print("\n[4] index.html 资源引用")
with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
    html = f.read()
for ref in ["assets/css/book.css", "assets/js/chapters.js", "assets/js/app.js",
            "assets/images/cover.png"]:
    if ref in html:
        ok(f"引用 {ref}")
    else:
        fail(f"未引用 {ref}")

# CDN 引用
for cdn in ["cdn.tailwindcss.com", "alpinejs", "marked", "Noto+Serif+SC"]:
    if cdn in html:
        ok(f"CDN: {cdn}")
    else:
        fail(f"缺少 CDN: {cdn}")

# Alpine 组件
if "x-data=\"bookApp()\"" in html:
    ok("Alpine x-data=bookApp()")
else:
    fail("缺少 Alpine x-data")

# 视图切换
if "view==='home'" in html and "view==='read'" in html:
    ok("双视图 home/read")
else:
    fail("缺少双视图")

# 5. app.js 关键方法
print("\n[5] app.js 关键方法")
with open(os.path.join(ROOT, "assets/js/app.js"), encoding="utf-8") as f:
    appjs = f.read()
for method in ["init()", "loadChapter(", "preloadChapter(", "toggleTheme(",
               "setFont(", "onScroll(", "handleHash(", "openChapter(",
               "prevChapter()", "nextChapter()", "randomChapter()", "goHome()",
               "chapterCache", "localStorage"]:
    if method in appjs:
        ok(f"方法/字段: {method}")
    else:
        fail(f"缺少: {method}")

# 6. book.css 关键样式
print("\n[6] book.css 关键样式")
with open(os.path.join(ROOT, "assets/css/book.css"), encoding="utf-8") as f:
    css = f.read()
for sel in [".markdown", ".markdown h1", ".markdown blockquote", ".markdown table",
            ".dark .markdown", ".reading-progress", ".sidebar-link", ".card",
            ".btn-primary", "@media"]:
    if sel in css:
        ok(f"样式: {sel}")
    else:
        fail(f"缺少样式: {sel}")

# 7. cover.png 存在性
print("\n[7] cover.png 存在性")
cover_png = os.path.join(ROOT, "assets/images/cover.png")
if os.path.isfile(cover_png) and os.path.getsize(cover_png) > 0:
    ok(f"cover.png ({os.path.getsize(cover_png)}B)")
else:
    fail("cover.png 缺失或为空")

# 8. PARTS 9篇
print("\n[8] PARTS 9篇")
parts_in_js = re.findall(r"name:\s*'([^']+)'", js.split('CHAPTERS')[0])
if len(parts_in_js) == 9:
    ok(f"9 篇: {', '.join(parts_in_js)}")
else:
    fail(f"篇数 {len(parts_in_js)}，预期 9")

# 9. 深色模式
print("\n[9] 深色模式")
if "darkMode: 'class'" in html:
    ok("Tailwind darkMode class")
else:
    fail("缺少 darkMode config")
if "classList.add('dark')" in appjs and "classList.remove('dark')" in appjs:
    ok("主题切换 classList")
else:
    fail("缺少主题切换逻辑")

# 10. 路由
print("\n[10] hash 路由")
if "#/ch/" in appjs and "hashchange" in appjs:
    ok("hash 路由 #/ch/{id}")
else:
    fail("缺少 hash 路由")

print("\n" + "=" * 60)
print(f"通过: {ok_count}, 失败: {len(errors)}")
print("=" * 60)
if errors:
    print("\n失败详情:")
    for e in errors:
        print(f"  - {e}")
print("\nALL PASS" if not errors else "HAS FAILURES")
sys.exit(0 if not errors else 1)