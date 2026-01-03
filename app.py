import sqlite3
import uuid
import os
from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime

app = Flask(__name__)
DB_PATH = os.environ.get('DATABASE_PATH', 'data/mindspace.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Content (
        id TEXT PRIMARY KEY, title TEXT, author TEXT, 
        content TEXT, analysis TEXT, tag TEXT, display_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Comments (
        id TEXT PRIMARY KEY, ref_id TEXT, user TEXT, 
        body TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/today')
def get_today():
    conn = get_db()
    c = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    # 优先匹配日期，否则随机推荐一条
    row = c.execute("SELECT * FROM Content WHERE display_date = ?", (today,)).fetchone()
    if not row:
        row = c.execute("SELECT * FROM Content ORDER BY RANDOM() LIMIT 1").fetchone()
    
    comments = c.execute("SELECT * FROM Comments WHERE ref_id = ? ORDER BY timestamp DESC LIMIT 3", 
                         (row['id'] if row else '',)).fetchall()
    
    res = dict(row) if row else {"content": "暂无内容", "analysis": "请通过 sync_content.py 导入数据"}
    res['comments'] = [dict(cmt) for cmt in comments]
    conn.close()
    return jsonify(res)

@app.route('/api/comment', methods=['POST'])
def add_comment():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO Comments VALUES (?,?,?,?,?)",
              (str(uuid.uuid4()), data['ref_id'], data['user'], data['body'], datetime.now()))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)