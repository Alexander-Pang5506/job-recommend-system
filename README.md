# 招聘推荐系统

Django + MySQL + SimpleUI 搭建的招聘信息管理与推荐系统。

## 环境要求

| 组件 | 版本 | 路径/说明 |
|------|------|------------|
| Python | 3.12.4 | `D:\Anaconda\python.exe` |
| MySQL | 8.0.30 | `C:\Users\P.sir\Desktop\mysql-8.0.30-winx64\` |
| Django | 5.1.2 | 已安装 |
| pymysql | latest | 已安装 |
| django-simpleui | latest | 已安装 |

## 数据库配置

- **数据库名**：`recommend_job`
- **用户名**：`root`
- **密码**：`12345678`
- **端口**：`3306`
- **数据量**：job_data 表 14,377 条记录

## 在 Trae 中打开项目

1. 打开 **Trae**（或 VS Code）
2. 菜单 **文件 → 打开文件夹**
3. 选择路径：`C:\Users\P.sir\WorkBuddy\2026-06-14-20-07-12\job_recommend_project`
4. 点击 **确定**

## 运行项目

### 方法一：使用 Trae 调试（推荐）

1. 按 `F5` 或点击左侧 **运行和调试** 图标
2. 选择 **"Django: 启动服务器（自动重载）"**
3. 服务器启动后访问：http://localhost:8000

### 方法二：使用终端

在 Trae 终端（`Ctrl + `` ` ``）中运行：

```bash
D:/Anaconda/python.exe manage.py runserver 0.0.0.0:8000
```

### 方法三：双击运行（Windows）

直接双击项目根目录下的 `run.bat` 文件。

## 访问地址

| 页面 | 地址 |
|------|------|
| 前台首页 | http://localhost:8000 |
| 管理后台 | http://localhost:8000/admin |
| 职位列表 API | http://localhost:8000/admin/job/job_data |

> **管理员账号**：admin / admin123456（如密码不对，运行 `python manage.py changepassword admin` 重置）

## 常见问题

### 中文乱码？
数据库已使用 `utf8mb4` 编码，`settings.py` 已配置 `OPTIONS -> charset: utf8mb4`。如仍有问题，确认 MySQL 服务正常运行。

### MySQL 连接失败？
手动启动 MySQL：
```bash
"D:\Anaconda\python.exe" -c "import pymysql; pymysql.connect(host='localhost', user='root', password='12345678')"
```

### 端口被占用？
修改 `settings.py` 中的 `runserver` 端口，或杀掉占用进程：
```bash
netstat -ano | findstr :8000
taskkill /f /pid <PID>
```

## 项目结构

```
job_recommend_project/
├── JobRecommend/          # Django 项目配置
│   ├── settings.py        # 设置（数据库、已安装应用等）
│   ├── urls.py            # 主路由
│   └── wsgi.py
├── job/                   # 招聘应用
│   ├── models.py          # 数据模型
│   ├── views.py          # 视图函数
│   ├── admin.py          # 后台管理配置
│   └── urls.py           # 应用路由
├── templates/             # HTML 模板
├── static/                # 静态文件（CSS/JS/图片）
├── manage.py              # Django 管理脚本
├── recommend_job.sql      # 数据库备份（Navicat UTF-8 导出）
├── .vscode/              # Trae/VSCode 配置
│   ├── launch.json       # 调试配置
│   └── settings.json    # 工作区设置
└── run.bat               # Windows 一键启动脚本
```

## 技术栈

- **后端**：Django 5.1.2 + pymysql
- **数据库**：MySQL 8.0.30
- **后台 UI**：django-simpleui
- **数据可视化**：pyecharts
- **爬虫**：selenium
