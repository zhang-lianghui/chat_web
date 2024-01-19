from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from web_chat.database import crud, models, schemas
from web_chat.database.database import engine
from web_chat.dependencies import get_db
from web_chat.routers import users
from fastapi.security import  OAuth2PasswordRequestForm
from web_chat.oauth2 import login_for_access_token



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="web_chat/static"), name="static")

templates = Jinja2Templates(directory="web_chat/template")


app.include_router(users.router)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": id}
    )
    
@app.get("/login", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"id": id}
    )
    
@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse(
        request=request, name="register.html", context={"id": id}
    )
    
@app.post("/register")
async def register(user: schemas.UserCreate, db :Session = Depends(get_db)):
    print(user)
    crud.create_user(db,user)
    return 'OK'
# @app.get("/chat", response_class=HTMLResponse)
# async def index(request: Request):
#     question = 'q'
#     ans = 'ans'
#     return templates.TemplateResponse(
#         request=request, name="chat.html", context={"ans": ans}
#     )
    

@app.get("/chats/", response_model=list[schemas.Chat])
def read_chats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chats = crud.get_chats(db, skip=skip, limit=limit)
    return chats


@app.post("/users/{user_id}/{chat_title}")
def save_message(user_id: int, chat_title:str, db: Session = Depends(get_db)):
    db_chat = db.query(models.Chat).filter(models.Chat.owner_id == user_id, models.Chat.title == chat_title).first()
    if db_chat is None:
        raise HTTPException(status_code=404, detail="Invalid chat")
    ques = 'ques'
    ans = 'ans'
    
    return crud.create_chat_message(db,db_chat.id, ques=ques, ans=ans)

@app.post("/token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    return await login_for_access_token(form_data , db)
    

