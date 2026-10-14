from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    """数据库里的一张表 + 接口返回的格式"""
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False


class TodoCreate(SQLModel):
    """新建待办时，客户端只需传 title"""
    title: str
