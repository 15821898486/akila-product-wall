# server.py - 完整的数据库网站服务器
import http.server
import socketserver
import sqlite3
import urllib.parse

# 1. 连接数据库（自动创建data.db）
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()

# 2. 创建数据表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

class DatabaseHandler(http.server.SimpleHTTPRequestHandler):
    # 3. 处理首页请求
    def do_GET(self):
        if self.path == '/':
            # 显示你的AI_workshop.html
            try:
                with open('AI_workshop.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            except:
                self.send_error(404, "找不到AI_workshop.html文件")
        
        elif self.path == '/view':
            # 显示数据库所有数据
            cursor.execute('SELECT * FROM posts ORDER BY id DESC')
            all_posts = cursor.fetchall()
            
            html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>查看数据</title>
                <style>
                    body { font-family: Arial; margin: 30px; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
                    th { background-color: #4CAF50; color: white; }
                    tr:nth-child(even) { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
                <h1>📊 数据库中的所有数据</h1>
                <p><a href="/">返回首页</a></p>
            '''
            
            if all_posts:
                html += '<table>'
                html += '<tr><th>ID</th><th>姓名</th><th>内容</th><th>提交时间</th></tr>'
                for post in all_posts:
                    html += f'<tr><td>{post[0]}</td><td>{post[1]}</td><td>{post[2]}</td><td>{post[3]}</td></tr>'
                html += '</table>'
                html += f'<p>共 {len(all_posts)} 条记录</p>'
            else:
                html += '<p>暂无数据</p>'
            
            html += '</body></html>'
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        
        else:
            # 其他请求（如图片、CSS文件）
            super().do_GET()
    
    # 4. 处理表单提交
    def do_POST(self):
        if self.path == '/save':
            # 读取表单数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # 解析数据
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            name = params.get('participant', ['匿名'])[0]
            content = params.get('content', [''])[0]
            
            # 存入数据库
            cursor.execute('INSERT INTO posts (name, content) VALUES (?, ?)', (name, content))
            conn.commit()
            
            # 返回成功消息
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            response = f'''
            <script>
                alert("✅ 数据保存成功！\\n姓名: {name}\\n内容: {content}");
                window.location.href = "/";
            </script>
            '''
            self.wfile.write(response.encode('utf-8'))
        
        else:
            self.send_error(404, "Not Found")

# 5. 启动服务器
PORT = 8000
print("=" * 60)
print("🚀 数据库网站服务器启动成功！")
print(f"👉 访问地址: http://localhost:{PORT}")
print(f"👉 查看数据: http://localhost:{PORT}/view")
print(f"📁 数据库文件: data.db")
print("=" * 60)

with socketserver.TCPServer(("", PORT), DatabaseHandler) as httpd:
    print(f"📡 服务器正在运行，按 Ctrl+C 停止")
    print("=" * 60)
    httpd.serve_forever()