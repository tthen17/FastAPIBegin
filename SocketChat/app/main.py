from fastapi import FastAPI, WebSocket, Request, Depends, HTTPException,status, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.auth import models, schemas
from app.auth.models import User,TokenTable
import jwt
from datetime import datetime, timezone
from .database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.auth.auth_bearer import JWTBearer
from app.auth.utils import create_access_token,create_refresh_token,verify_password,get_hashed_password
from app.socket.conmanager import ConnectionManager

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

models.Base.metadata.create_all(bind=engine) #DB tables created here

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def loadlogin(request: Request):
    return templates.TemplateResponse("login.html", {"request":request})

@app.post("/register")
def register_user(user: schemas.UserCreate, session: Session = Depends(get_db)):
    existing_user = session.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)

    new_user = models.User(username=user.username, email=user.email, password=encrypted_password )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message":"user created successfully"}


@app.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    formdata = await request.form()
    email = formdata["user_email"]
    password = formdata["user_pass"]
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    
    hashed_pass = user.password
    if not verify_password(password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    access=create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = models.TokenTable(user_id=user.id,  access_toke=access,  refresh_toke=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    response = RedirectResponse(url="/chat", status_code=status.HTTP_303_SEE_OTHER)
    return response


@app.get("/chat")
async def get(request: Request, 
              #dependencies=Depends(JWTBearer()) RESOLVE ISSUE WITH JWT NOT AUTH
              ):
    return templates.TemplateResponse("main.html", {"request":request})


manager = ConnectionManager()

@app.websocket("/chat/ws") #add clientid to end of path
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You: {data}", websocket)
            #await manager.broadcast(f"Other says: {data}") use when implemented with clientid
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        #await manager.broadcast("A client has left") use when implemented with clientid