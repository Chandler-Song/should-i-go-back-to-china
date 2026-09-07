import http.server
import socketserver
import os

os.chdir(r"C:\Users\Administrator\IDEProjects\gotochina")
PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass

httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.allow_reuse_address = True
print(f"READY http://localhost:{PORT}/")
httpd.serve_forever()
