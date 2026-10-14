from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Todo, TodoCreate, TodoUpdate

# prefix="/todos" 表示这个路由器里所有路径都自动带上 /todos
router = APIRouter(prefix="/todos", tags=["待办"])


@router.get("", response_model=list[Todo])
def list_todos(session: Session = Depends(get_session)):
    """查出所有待办"""
    return session.exec(select(Todo)).all()


@router.post("", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    """新建一条待办"""
    db_todo = Todo(title=todo.title)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.put("/{todo_id}/done", response_model=Todo)
def mark_done(todo_id: int, session: Session = Depends(get_session)):
    """标记某条待办为完成"""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="找不到这条待办")
    todo.done = True
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.patch("/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    session: Session = Depends(get_session),
):
    """修改待办的 title 或 done（只更新客户端传过来的字段）"""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="找不到这条待办")

    # exclude_unset=True：只拿到客户端真正传了的字段，没传的不动
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    """删除某条待办"""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="找不到这条待办")
    session.delete(todo)
    session.commit()
    return {"message": "已删除"}
