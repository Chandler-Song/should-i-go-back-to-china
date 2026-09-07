import http.server
import socketserver
import threading
import time
import urllib.request
import os

os.chdir(r"C:\Users\Administrator\IDEProjects\gotochina")
PORT = 8090

class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

h = socketserver.TCPServer(("", PORT), H)
t = threading.Thread(target=h.serve_forever, daemon=True)
t.start()
time.sleep(1)
r = urllib.request.urlopen(f"http://localhost:{PORT}/", timeout=5)
print("服务器测试:", r.status, len(r.read()), "B")
h.shutdown()
print("服务器已关闭")