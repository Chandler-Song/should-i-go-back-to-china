import subprocess
import time
import urllib.request
import sys
import os

ROOT = r"C:\Users\Administrator\IDEProjects\gotochina"
PORT = 8234

proc = subprocess.Popen(
    [sys.executable, "-m", "http.server", str(PORT)],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

try:
    time.sleep(2)
    base = f"http://localhost:{PORT}"
    results = []
    failures = []

    def check(url, label):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 't'})
            with urllib.request.urlopen(req, timeout=8) as r:
                data = r.read()
                results.append((label, r.status, len(data)))
                return True
        except Exception as e:
            failures.append((label, str(e)[:100]))
            return False

    check(f"{base}/", "index.html")
    check(f"{base}/assets/css/book.css", "book.css")
    check(f"{base}/assets/js/chapters.js", "chapters.js")
    check(f"{base}/assets/js/app.js", "app.js")
    check(f"{base}/assets/images/cover.png", "cover.png")

    import glob
    ch_files = sorted(glob.glob(os.path.join(ROOT, "gobackchina", "ch*.md")))
    ch_ok = 0
    for p in ch_files:
        fn = os.path.basename(p)
        if check(f"{base}/gobackchina/{fn}", fn):
            ch_ok += 1

    print("=" * 60)
    print("HTTP 服务器 fetch 验证")
    print("=" * 60)
    for label, status, length in results:
        print(f"  [OK] {label} -> {status} {length}B")
    if failures:
        print("\n失败:")
        for label, err in failures:
            print(f"  [FAIL] {label} -> {err}")
    print(f"\n章节 fetch: {ch_ok}/{len(ch_files)}")
    print(f"总计: 成功 {len(results)}, 失败 {len(failures)}")
    print("=" * 60)
    ok = (len(failures) == 0 and ch_ok == len(ch_files))
    print("ALL PASS" if ok else "HAS FAILURES")
finally:
    proc.terminate()
    proc.wait(timeout=5)

sys.exit(0 if ok else 1)