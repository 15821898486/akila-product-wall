import sqlite3
import os

print("=" * 60)
print("开始修复数据库问题")
print("=" * 60)

# 1. 检查当前目录
print(f"当前目录: {os.getcwd()}")
print(f"文件列表: {os.listdir('.')}")

# 2. 检查 workshop.db
db_path = 'workshop.db'
if not os.path.exists(db_path):
    print(f"❌ {db_path} 不存在，正在创建...")
    open(db_path, 'w').close()

# 3. 连接数据库并修复
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 删除可能损坏的旧表
cursor.execute("DROP TABLE IF EXISTS workshop_data")

# 创建新表
cursor.execute('''
    CREATE TABLE workshop_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        participant TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("✅ 创建 workshop_data 表")

# 插入测试数据
test_data = [
    ('张三', '第一条测试留言'),
    ('李四', '这个网站可以保存数据到数据库'),
    ('王五', '数据会保存在 workshop.db 文件中')
]

for name, msg in test_data:
    cursor.execute("INSERT INTO workshop_data (participant, content) VALUES (?, ?)", (name, msg))

conn.commit()
print(f"✅ 插入 {len(test_data)} 条测试数据")

# 4. 验证数据
cursor.execute("SELECT COUNT(*) FROM workshop_data")
count = cursor.fetchone()[0]
print(f"✅ 验证: 数据库中共有 {count} 条记录")

cursor.execute("SELECT * FROM workshop_data")
rows = cursor.fetchall()
print("\n📊 数据库内容预览:")
print("-" * 50)
for row in rows:
    print(f"ID:{row[0]} | 用户:{row[1]} | 内容:{row[2][:20]}... | 时间:{row[3]}")
print("-" * 50)

conn.close()

# 5. 生成简易查看页面
html_path = 'view_data.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html>
<head><title>查看数据库数据</title>
<style>
    body { font-family: Arial; margin: 40px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
    th { background-color: #4CAF50; color: white; }
    tr:nth-child(even) { background-color: #f2f2f2; }
</style>
</head>
<body>
<h1>📊 数据库中的数据</h1>
<p>数据库文件: <code>workshop.db</code></p>
''')
    
    # 重新连接获取数据
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workshop_data ORDER BY created_at DESC")
    rows = cursor.fetchall()
    
    if rows:
        f.write('<table>')
        f.write('<tr><th>ID</th><th>用户</th><th>内容</th><th>时间</th></tr>')
        for row in rows:
            f.write(f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>')
        f.write('</table>')
    else:
        f.write('<p style="color:red;">数据库为空！</p>')
    
    conn.close()
    
    f.write(f'''
    <p style="margin-top: 30px;">
        <strong>总记录数:</strong> {count}<br>
        <strong>数据库文件大小:</strong> {os.path.getsize(db_path)} 字节
    </p>
    <p><a href="/">返回首页</a></p>
</body>
</html>''')

print(f"\n✅ 已生成查看页面: {html_path}")
print("👉 可以直接用浏览器打开这个文件查看数据")
print("👉 或者访问: http://localhost:5000/view")

print("\n" + "=" * 60)
print("修复完成！")
print("接下来:")
print("1. 运行: python app.py")
print("2. 访问: http://localhost:5000/")
print("3. 提交表单测试")
print("4. 访问: http://localhost:5000/view 查看数据")
print("=" * 60)

input("\n按回车键运行 app.py...")

# 自动运行 app.py
os.system("python app.py")