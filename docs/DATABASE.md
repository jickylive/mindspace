# 阅界 (MindSpace) 项目数据结构模型说明 (Data Schema)

本说明文档详细定义了系统的存储层、逻辑层以及接口层的数据协议，旨在指导 AI 生成、CSV 同步及前后端开发。

---

## 1. 逻辑架构模型

系统数据流遵循 **“多源输入 -> 标准化存储 -> 多端分发”** 的逻辑。



---

## 2. 数据库表结构 (SQLite)

系统核心由两张表构成，通过内容唯一标识符进行关联。

### A. 内容表 (Content)
用于存储核心展示素材。每条记录代表一次屏保展示的完整内容。

| 字段名 (Field) | 类型 (Type) | 约束 (Constraint) | 说明 (Description) |
| :--- | :--- | :--- | :--- |
| **id** | TEXT | PRIMARY KEY | 内容唯一指纹 (MD5) |
| **title** | TEXT | NOT NULL | 作品标题 (如：《定风波》) |
| **author** | TEXT | NOT NULL | 作者姓名 (如：苏轼) |
| **content** | TEXT | NOT NULL | 核心原文片段 (100字以内) |
| **analysis** | TEXT | NOT NULL | 三维解析文本 (含原境/逻辑/今日) |
| **tag** | TEXT | - | 检索标签 (如：韧性, 立春) |
| **display_date** | TEXT | UNIQUE | 预定展示日期 (格式：YYYY-MM-DD) |

### B. 评论感悟表 (Comments)
存储员工通过移动端扫码提交的即时感悟。

| 字段名 (Field) | 类型 (Type) | 约束 (Constraint) | 说明 (Description) |
| :--- | :--- | :--- | :--- |
| **id** | TEXT | PRIMARY KEY | 评论唯一标识符 |
| **ref_id** | TEXT | FOREIGN KEY | 关联的 Content 表 id |
| **user** | TEXT | DEFAULT '匿名' | 提交人姓名或工号 |
| **body** | TEXT | NOT NULL | 感悟正文 (200字以内) |
| **timestamp** | DATETIME | DEFAULT CURRENT_TIMESTAMP | 提交时间 |



---

## 3. 核心对象协议 (JSON)

当 API (`/api/today`) 响应或 AI 模块下发内容时，必须严格遵守以下 JSON Schema：

```json
{
  "id": "md5_hash_string",
  "title": "作品名",
  "author": "作者",
  "content": "原文正文",
  "analysis": "【原境】...【逻辑】...【今日】...",
  "tag": "标签1,标签2",
  "display_date": "2026-01-03",
  "comments": [
    {
      "user": "员工姓名",
      "body": "评论内容",
      "timestamp": "2026-01-03 10:00:00"
    }
  ]
}
```

---

## 4. 数据生成规范 (Validation)

### 唯一性生成规则 (ID Generation)
1. **手动 CSV 导入**：`id = MD5(content + display_date)`。用于确保同一天同一个内容不重复。
2. **AI 自动生成**：`id = MD5(display_date)`。确保每天系统仅保留并展示一条 AI 推荐内容。

### 内容解析模版 (Analysis Template)
AI 生成的 `analysis` 字段必须严格包含以下占位符，以配合前端排版渲染：
- **【原境】**：解析诗词创作的历史背景与物理环境。
- **【逻辑】**：剖析诗句背后的底层思维逻辑或哲学意图。
- **【今日】**：关联现代职场、个人成长或中年生活的心境共鸣。

---

## 5. 开发建议
* **索引优化**：由于查询频繁使用 `display_date`，建议在数据库中为该字段建立索引。
* **安全性**：`POST /api/comment` 接口应加入简单的关键词过滤，防止脏数据入库。