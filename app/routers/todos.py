from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.deps import get_current_user
from app.models import Todo, TodoCreate, TodoUpdate, User

# prefix="/todos" 表示这个路由器里所有路径都自动带上 /todos
router = APIRouter(prefix="/todos", tags=["待办"])


def get_own_todo(todo_id: int, user: User, session: Session) -> Todo:
    """取出属于当前用户的待办

    注意：查不到、或者查到了但属于别人，都返回 404。
    这叫“不泄露资源是否存在”——返回 403 等于告诉对方“这条确实存在，只是不给你”。
    """
    todo = session.get(Todo, todo_id)
    if todo is None or todo.user_id != user.id:
        raise HTTPException(status_code=404, detail="找不到这条待办")
    return todo


@router.get("", response_model=list[Todo])
def list_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """只查当前登录用户自己的待办"""
    return session.exec(
        select(Todo).where(Todo.user_id == current_user.id)
    ).all()


@router.post("", response_model=Todo, status_code=201)
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """新建一条待办，归属当前登录用户"""
    db_todo = Todo(title=todo.title, user_id=current_user.id)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.put("/{todo_id}/done", response_model=Todo)
def mark_done(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """标记某条待办为完成"""
    todo = get_own_todo(todo_id, current_user, session)
    todo.done = True
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.patch("/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """修改待办的 title 或 done（只更新客户端传过来的字段）"""
    todo = get_own_todo(todo_id, current_user, session)

    # exclude_unset=True：只拿到客户端真正传了的字段，没传的不动
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """删除某条待办"""
    todo = get_own_todo(todo_id, current_user, session)
    session.delete(todo)
    session.commit()
    return {"message": "已删除"}
