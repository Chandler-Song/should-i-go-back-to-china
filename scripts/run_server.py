import http.server
import socketserver
import os
import webbrowser
import time

os.chdir(r"C:\Users\Administrator\IDEProjects\gotochina")
PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass

print(f"启动服务器 http://localhost:{PORT}/")
print(f"工作目录: {os.getcwd()}")

httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.allow_reuse_address = True

time.sleep(1)
webbrowser.open(f"http://localhost:{PORT}/")
print("浏览器已打开")

httpd.serve_forever()