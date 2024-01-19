from fastapi import FastAPI, Request, Depends, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import crud, models, schemas
from ..dependencies import get_db, get_token_header


router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/chats/")
def create_chat_for_user(
    user_id: int, chat: schemas.ChatCreate, db: Session = Depends(get_db)
):
    if db.query(models.Chat).filter(models.Chat.title == chat.title, models.Chat.owner_id == user_id).first():
        return "标题重复"
    return crud.create_user_chat(db=db, chat=chat, user_id=user_id)

@router.post("/{user_id}/unregister")
def unregister_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")