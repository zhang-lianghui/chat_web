from sqlalchemy.orm import Session
from ..oauth2 import get_password_hash
from sqlalchemy.exc import IntegrityError
from . import models, schemas




def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        if "UNIQUE constraint failed: users.username" in str(e):
            raise ValueError("用户名已被注册")


def delete_user(db: Session, user_id: int):
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
    return user_to_delete

def get_chats(db: Session, user: models.User):
    return db.query(models.Chat).filter(models.Chat.owner_id == user.id).all()


def delete_chat(db: Session, user_id: int, chat_title: str):
    chat_to_delete = db.query(models.Chat).filter(models.Chat.owner_id == user_id, models.Chat.title == chat_title,).first()
    if chat_to_delete:
        db.delete(chat_to_delete)
        db.commit()
        #db.refresh(chat_to_delete)
    return chat_to_delete

def create_user_chat(db: Session, chat: schemas.ChatCreate, user_id: int):
    db_chat = models.Chat(**chat.dict(), owner_id=user_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def create_chat_message(db: Session, chat_id: int, ques: str, ans: str):
    db_message = models.Message(chat_id = chat_id, ques = ques, ans = ans)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message