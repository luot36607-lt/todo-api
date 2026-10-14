from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    """数据库里的一张表 + 接口返回的格式"""
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False


class TodoCreate(SQLModel):
    """新建待办时，客户端只需传 title"""
    title: str


class TodoUpdate(SQLModel):
    """修改待办时，title 和 done 都是可选的（只传你想改的字段）"""
    title: str | None = None
    done: bool | None = None
