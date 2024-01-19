from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    chats = relationship("Chat", back_populates="owner")#, cascade="delete")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates='chat')#, cascade="delete")
    __table_args__ = (UniqueConstraint('owner_id', 'title'),)
    
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    ques = Column(String)
    ans = Column(String)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    chat = relationship("Chat", back_populates='messages')