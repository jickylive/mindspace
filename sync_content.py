import sqlite3
import hashlib
import os
import csv

# 数据库路径，确保与 app.py 一致
DB_PATH = os.environ.get('DATABASE_PATH', 'data/mindspace.db')

def init_table(conn):
    """确保数据库表存在"""
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Content (
        id TEXT PRIMARY KEY, 
        title TEXT, 
        author TEXT, 
        content TEXT, 
        analysis TEXT, 
        tag TEXT, 
        display_date TEXT)''')
    conn.commit()

def sync(csv_path):
    if not os.path.exists(csv_path):
        print(f"错误: 找不到文件 {csv_path}")
        return
    
    # 确保数据库目录存在
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    
    # 1. 先初始化表结构
    init_table(conn)
    
    c = conn.cursor()
    
    try:
        # 显式指定 utf-8-sig 以处理某些 Windows 导出的带 BOM 的 CSV 文件
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            success_count = 0
            
            for row in reader:
                # 生成基于原文和日期的唯一ID，防止重复导入
                raw_str = f"{row['origin_text']}{row['display_date']}"
                uid = hashlib.md5(raw_str.encode()).hexdigest()
                
                c.execute("""
                    INSERT OR IGNORE INTO Content 
                    (id, title, author, content, analysis, tag, display_date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (uid, row['title'], row['author'], row['origin_text'], 
                      row['analysis'], row['tag'], row['display_date']))
                
                if c.rowcount > 0:
                    success_count += 1
            
            conn.commit()
            print(f"同步完成！成功向数据库中存入 {success_count} 条新内容。")
    except KeyError as e:
        print(f"解析出错: CSV 缺少列 {e}。请检查 CSV 表头是否为: title,author,origin_text,analysis,tag,display_date")
    except Exception as e:
        print(f"解析出错: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    sync('content.csv')