from sqlmodel import Field, SQLModel


# ---------- 用户 ----------
class User(SQLModel, table=True):
    """用户表：只存用户名和密码哈希，绝不存明文密码"""
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str


class UserCreate(SQLModel):
    """注册 / 登录时，客户端传的字段"""
    username: str
    password: str


class UserRead(SQLModel):
    """返回给客户端的用户信息（绝不包含密码）"""
    id: int
    username: str


# ---------- 待办 ----------
class Todo(SQLModel, table=True):
    """数据库里的一张表 + 接口返回的格式"""
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)  # 这条待办属于谁
    title: str
    done: bool = False


class TodoCreate(SQLModel):
    """新建待办时，客户端只需传 title"""
    title: str


class TodoUpdate(SQLModel):
    """修改待办时，title 和 done 都是可选的（只传你想改的字段）"""
    title: str | None = None
    done: bool | None = None
