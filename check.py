import sqlite3

conn = sqlite3.connect('workshop.db')
cursor = conn.cursor()

# 查看所有数据
cursor.execute("SELECT * FROM workshop_data")
rows = cursor.fetchall()

print("📊 数据库内容：")
print("-" * 50)
for row in rows:
    print(f"ID:{row[0]:3} | 用户:{row[1]:10} | 内容:{row[2]:20} | 时间:{row[3]}")
print("-" * 50)
print(f"共 {len(rows)} 条记录")

conn.close()

# 导出到文件
with open('data.txt', 'w', encoding='utf-8') as f:
    for row in rows:
        f.write(f"{row[0]},{row[1]},{row[2]},{row[3]}\n")
print("✅ 数据已导出到 data.txt")