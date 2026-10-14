from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routers import todos


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 程序启动时：建表
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="我的待办 API", lifespan=lifespan)

# 把待办相关的接口挂载进来
app.include_router(todos.router)


@app.get("/")
def read_root():
    return {"message": "待办 API 跑起来了！"}
