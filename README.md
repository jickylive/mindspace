# 阅界 (MindSpace) —— 跨平台企业文化屏保系统



## 📖 项目介绍
**阅界 (MindSpace)** 是一款旨在利用办公电脑空闲时间，通过展示深度诗词解析来对抗思维退化的跨平台系统。

---

## 🚀 部署场景 (Deployment Scenarios)

### 场景一：个人单机部署 (轻量化运行)
适用于希望在自己电脑上运行屏保的用户。
1. **环境**：安装 Python 3.8+。
2. **运行**：
   ```bash
   pip install flask
   python sync_content.py  # 初始化数据
   python app.py           # 启动服务
   ```
3. **展示**：使用浏览器全屏（F11）打开 `http://127.0.0.1:5001`。

### 场景二：企业内网集群部署 (CI/CD 模式)
适用于 IT 部门统一管理，通过服务器下发内容。
1. **配置**：在 Git 仓库维护 `content.csv`。
2. **构建**：CI 流程触发 Docker 镜像构建。
3. **分发**：使用 Docker Compose 部署。
   ```bash
   docker-compose up -d --build
   ```
4. **终端**：员工电脑通过“网页屏保壳”指向中心服务器 IP。



### 场景三：离线/安全内网部署 (全隔离环境)
适用于金融、政务等无法访问公网的环境。
1. **打包**：在有网环境下载依赖：
   ```bash
   pip download -r requirements.txt -d ./packages
   ```
2. **迁移**：将项目文件夹与 `packages` 拷贝至目标机。
3. **安装**：
   ```bash
   pip install --no-index --find-links=./packages -r requirements.txt
   ```

### 场景四：开发者模式 (AI 自动驾驶)
适用于希望内容自动更新的场景。
1. **配置**：在 `ai_generator.py` 中设置 API Key。
2. **调度**：设置 Cron Job 每天定时生成。
   ```bash
   # 每天 08:30 自动生成今日应景内容
   30 8 * * * /usr/bin/python3 /path/to/ai_generator.py
   ```

---

## 🛠 技术规格与数据模型

### 数据结构 (Data Schema)

* **Content 表**：存储诗词原文、三维解析（原境/逻辑/今日）、展示日期。
* **Comments 表**：存储通过移动端扫码提交的员工感悟。

### API 规范
* `GET /api/today`: 获取今日展示内容及其关联评论。
* `POST /api/comment`: 提交新的感悟数据。

---

## 🖥 终端适配说明

| 平台 | 实现方式 | 推荐方案 |
| :--- | :--- | :--- |
| **麒麟 (Kirin)** | UKUI 自定义屏保脚本 | `firefox --kiosk [URL]` |
| **Windows** | 网页屏保包装器 (Web Screensaver) | 设置 URL 为本地或服务器 IP |
| **macOS** | 系统 AirPlay 端口避让 | 使用 5001 端口运行 |

---

## 🛠 技术架构与规格

项目基于轻量级架构设计，支持从单机到集群的平滑迁移。

* **后端服务**: Python Flask + SQLite
* **前端展示**: HTML5 Canvas & CSS3 动效
* **数据契约**: [MindSpace 数据模型规范](./docs/DATABASE.md)



---

## 📂 项目结构
* `app.py`: 后端核心逻辑。
* `docs/`: 
    * `DATABASE.md`: **[核心文档]** 完整数据结构模型补充说明。
* `static/`: 前端静态资源。
* `ai_generator.py`: AI 自动化更新模块。

---

## 🤝 参与贡献
如果您有优秀的文案内容，请提交 Pull Request 修改 `content.csv`。

> **“心平气和，则百疾不生。”**