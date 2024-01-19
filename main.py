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
from web_chat.oauth2 import login_for_access_token, oauth2_scheme, token_blacklist, token_middleware, get_current_user, get_current_active_user
from fastapi.middleware import Middleware
import uvicorn


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="web_chat/static"), name="static")

templates = Jinja2Templates(directory="web_chat/template")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next, db: Session = Depends(get_db)):
    print("Before handling the request in my_custom_middleware")
    response = await token_middleware(request,call_next)
    print("After handling the request in my_custom_middleware")
    return response

app.include_router(users.router)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )
    
@app.get("/login", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={}
    )
    
@app.post("/login", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={}
    )
  
@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse(
        request=request, name="register.html", context={}
    )
    
@app.post("/register")
async def register(user: schemas.UserCreate, db :Session = Depends(get_db)):
    try:
        crud.create_user(db,user)
        return 'OK'
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    token_blacklist.add(token)
    return {"message": "Logout successful"}

@app.get("/get_user", response_model=schemas.User)
async def get_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token","")
    current_user = await get_current_user(db,token)
    db_user = await get_current_active_user(current_user)
    return db_user


@app.get("/chat", response_class=HTMLResponse)
async def index(request: Request):
    ques = 'q'
    ans = 'ans'
    return templates.TemplateResponse(
        request=request, name="chat.html", context={"ans": ans, 'ques':ques}
    )
    

# @app.post("/chats/", response_model=list[schemas.Chat])
# async def read_chats(current_user: models.User = Depends(get_current_active_user)):
#     chats = crud.get_chats(db, skip=skip, limit=limit)
#     return chats


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
    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)