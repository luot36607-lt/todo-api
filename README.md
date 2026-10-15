# 待办 API（Todo API）

一个用 FastAPI 写的多用户待办事项后端服务，带用户注册 / 登录（JWT 鉴权）和数据隔离，数据存在 SQLite 中。

这是我学习后端开发的第一个完整项目，用来练习 FastAPI、数据库操作、用户认证和项目结构组织。

## 技术栈

- **Python 3.13**
- **FastAPI** — Web 框架
- **SQLModel** — ORM（数据库操作 + 数据校验）
- **SQLite** — 数据库（单文件，无需安装）
- **Uvicorn** — ASGI 服务器
- **PyJWT + bcrypt** — 用户认证（JWT 令牌 + 密码哈希）

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

> ⚠️ `app/security.py` 里的 `SECRET_KEY` 目前是开发用的固定值。生产部署时必须改为从环境变量读取。

## 接口列表

除注册和登录外，所有 `/todos` 接口都需要在请求头带 `Authorization: Bearer <token>`，且只能操作属于自己的数据。

| 方法 | 路径 | 说明 | 需要登录 |
|------|------|------|---------|
| GET | `/` | 健康检查 | 否 |
| POST | `/auth/register` | 注册 | 否 |
| POST | `/auth/login` | 登录，返回 JWT | 否 |
| GET | `/todos` | 查看自己的待办 | 是 |
| POST | `/todos` | 新建一条待办 | 是 |
| PUT | `/todos/{todo_id}/done` | 标记某条待办为完成 | 是 |
| PATCH | `/todos/{todo_id}` | 修改标题或完成状态 | 是 |
| DELETE | `/todos/{todo_id}` | 删除某条待办 | 是 |

请求示例：

```bash
# 1. 注册
curl -X POST http://127.0.0.1:8000/auth/register \
     -H "Content-Type: application/json" \
     -d "{\"username\": \"alice\", \"password\": \"pass123\"}"

# 2. 登录，拿到 token
curl -X POST http://127.0.0.1:8000/auth/login \
     -H "Content-Type: application/json" \
     -d "{\"username\": \"alice\", \"password\": \"pass123\"}"
# 返回 {"access_token": "eyJ...", "token_type": "bearer"}

# 3. 带着 token 新建待办
curl -X POST http://127.0.0.1:8000/todos \
     -H "Authorization: Bearer eyJ..." \
     -H "Content-Type: application/json" \
     -d "{\"title\": \"写简历\"}"
```

## 认证设计

- 密码用 **bcrypt** 加盐哈希后存储，数据库里没有明文密码。
- 登录成功签发 **JWT**，令牌里包含用户 id 和过期时间，用密钥签名防篡改。
- 每个 `/todos` 接口通过 `get_current_user` 依赖解析令牌，并校验数据归属。
- 访问他人的资源返回 **404**（而非 403），避免泄露资源是否存在。

## 项目结构

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # 程序入口：创建 app、挂载路由
│   ├── database.py      # 数据库连接与会话
│   ├── models.py        # 数据模型（用户表、待办表）
│   ├── security.py      # 密码哈希 + JWT 签发/校验
│   ├── deps.py          # 依赖：从请求解析当前登录用户
│   └── routers/
│       ├── auth.py      # 注册 / 登录
│       └── todos.py     # 待办相关接口（需登录）
├── requirements.txt     # 依赖清单
├── .gitignore           # 不提交到 git 的文件
└── README.md
```

## 后续计划

- [x] 用户系统（注册 / 登录 / JWT 鉴权 + 数据隔离）
- [ ] 待办加上截止时间、优先级
- [ ] 用 Docker 打包，部署到云服务器
- [ ] 补充单元测试（pytest）
- [ ] 数据库迁移工具（Alembic）
