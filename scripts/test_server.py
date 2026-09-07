import http.server
import socketserver
import threading
import urllib.request
import os
import time
import sys

PORT = 8124
ROOT = r"C:\Users\Administrator\IDEProjects\gotochina"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)
    def log_message(self, *args):
        pass

httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.allow_reuse_address = True
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
time.sleep(0.5)

results = []
failures = []

def check(url, label):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'test'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = r.read()
            results.append((label, r.status, len(data)))
            return True
    except Exception as e:
        failures.append((label, str(e)[:80]))
        return False

base = f"http://localhost:{PORT}"

check(f"{base}/", "index.html")
check(f"{base}/assets/css/book.css", "book.css")
check(f"{base}/assets/js/chapters.js", "chapters.js")
check(f"{base}/assets/js/app.js", "app.js")
check(f"{base}/assets/images/cover.png", "cover.png")

import glob
ch_files = sorted(glob.glob(os.path.join(ROOT, "gobackchina", "ch*.md")))
ch_ok = 0
ch_fail = 0
for path in ch_files:
    fname = os.path.basename(path)
    if check(f"{base}/gobackchina/{fname}", fname):
        ch_ok += 1
    else:
        ch_fail += 1

httpd.shutdown()

print("=" * 60)
print("资源加载测试结果")
print("=" * 60)
for label, status, length in results:
    print(f"  [OK] {label} -> {status} {length}B")

if failures:
    print("\n失败项:")
    for label, err in failures:
        print(f"  [FAIL] {label} -> {err}")

print(f"\n章节: 成功 {ch_ok}/{len(ch_files)}, 失败 {ch_fail}")
print(f"总计: 成功 {len(results)}, 失败 {len(failures)}")
print("=" * 60)
ok = (len(failures) == 0 and ch_ok == len(ch_files))
print("ALL PASS" if ok else "HAS FAILURES")
sys.exit(0 if ok else 1)
