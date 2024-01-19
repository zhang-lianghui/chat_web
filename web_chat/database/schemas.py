from pydantic import BaseModel


class ChatBase(BaseModel):
    title: str


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True



class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    chats: list[Chat] = []

    class Config:
        orm_mode = True



class MessageBase(BaseModel):
    ques: str
    ans: str

class MessageCreate(MessageBase):
    pass
        
class Message(MessageBase):
    id: int
    ques: str
    ans: str
    chat_id: int

    class Config:
        orm_mode = True