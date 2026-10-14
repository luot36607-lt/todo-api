# 待办 API（Todo API）

一个用 FastAPI 写的待办事项后端服务，数据存在 SQLite 中，支持增删改查。

这是我学习后端开发的第一个完整项目，用来练习 FastAPI、数据库操作和项目结构组织。

## 技术栈

- **Python 3.13**
- **FastAPI** — Web 框架
- **SQLModel** — ORM（数据库操作 + 数据校验）
- **SQLite** — 数据库（单文件，无需安装）
- **Uvicorn** — ASGI 服务器

## 如何运行

```bash
# 1. 创建并激活虚拟环境
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
uvicorn app.main:app --reload

# 4. 打开浏览器
# 接口文档： http://127.0.0.1:8000/docs
```

## 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 健康检查 |
| GET | `/todos` | 查看所有待办 |
| POST | `/todos` | 新建一条待办 |
| PUT | `/todos/{todo_id}/done` | 标记某条待办为完成 |
| DELETE | `/todos/{todo_id}` | 删除某条待办 |

请求示例：

```bash
curl -X POST http://127.0.0.1:8000/todos \
     -H "Content-Type: application/json" \
     -d "{\"title\": \"写简历\"}"
```

## 项目结构

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # 程序入口：创建 app、挂载路由
│   ├── database.py      # 数据库连接与会话
│   ├── models.py        # 数据模型（数据库表）
│   └── routers/
│       └── todos.py     # 待办相关接口
├── requirements.txt     # 依赖清单
├── .gitignore           # 不提交到 git 的文件
└── README.md
```

## 后续计划

- [ ] 加上用户系统（注册 / 登录 / JWT 鉴权）
- [ ] 待办加上截止时间、优先级
- [ ] 用 Docker 打包，部署到云服务器
- [ ] 补充单元测试
