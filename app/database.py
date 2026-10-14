from sqlmodel import Session, create_engine

# 数据库连接（SQLite 文件放在项目根目录）
engine = create_engine("sqlite:///todo.db", connect_args={"check_same_thread": False})


def get_session():
    """给每个请求分配一个独立的数据库会话"""
    with Session(engine) as session:
        yield session
