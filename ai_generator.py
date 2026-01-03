import os
import sqlite3
import hashlib
import json
from datetime import datetime
from openai import OpenAI

# 数据库路径
DB_PATH = os.environ.get('DATABASE_PATH', 'data/mindspace.db')

def generate_poem_with_ai():
    client = OpenAI(api_key="你的_API_KEY", base_url="你的_API_入口")
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # 系统提示词：锁定模型一致性
    system_prompt = """
    你是一个精通中国古典文学与现代职场心理学的专家。
    请按以下 JSON 格式返回今日应景诗词，严禁包含任何多余文字：
    {
      "title": "作品名",
      "author": "诗人",
      "origin_text": "诗词正文",
      "analysis": "【原境】背景介绍...【逻辑】思维模型...【今日】职场共鸣...",
      "tag": "节气/情绪标签",
      "display_date": "YYYY-MM-DD"
    }
    """
    
    user_prompt = f"请根据日期 {today_str} 的节气特征和冬日心境，生成一段能对抗思维退化的内容。"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106", # 或 deepseek-chat 等支持 JSON Mode 的模型
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={ "type": "json_object" } # 强制返回 JSON
    )
    
    return response.choices[0].message.content

def sync_ai_to_db(json_data):
    data = json.loads(json_data)
    
    # 验证字段完整性
    required_keys = ['title', 'author', 'origin_text', 'analysis', 'tag', 'display_date']
    if not all(k in data for k in required_keys):
        raise ValueError("AI 返回数据模型不完整")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 生成唯一标识：基于日期，确保一天只有一条 AI 推荐
    uid = hashlib.md5(data['display_date'].encode()).hexdigest()
    
    # 采用 REPLACE 模式：如果日期冲突，则以最新的 AI 生成内容为准
    c.execute("""
        INSERT OR REPLACE INTO Content (id, title, author, content, analysis, tag, display_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (uid, data['title'], data['author'], data['origin_text'], 
          data['analysis'], data['tag'], data['display_date']))
    
    conn.commit()
    conn.close()
    print(f"✅ AI 模型同步成功: {data['display_date']} - {data['title']}")

if __name__ == "__main__":
    try:
        raw_json = generate_poem_with_ai()
        sync_ai_to_db(raw_json)
    except Exception as e:
        print(f"❌ 同步失败: {e}")