from . import models, schemas
from .models import Url
from .database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse 
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Depends, HTTPException,status, Request, Form
from .utils import get_short_url, find_shorturl, create_shorturl, redirect_shorturl
from fastapi.middleware.cors import CORSMiddleware

templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
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
async def root(request: Request):
   return templates.TemplateResponse("main.html", {"request":request})

@app.post("/shorten")
async def shorten_url(url: str = Form(...), session: Session = Depends(get_db)):
    new_short_url = get_short_url(url)

    existing_hash = find_shorturl(session, new_short_url)
    if existing_hash:
        raise HTTPException(status_code=500, detail="Invalid hash")

    return create_shorturl(session, new_short_url, url)

@app.get("/http://short.url/{shorturl}")
async def redirect_url(shorturl:str, session: Session = Depends(get_db)):
    url = "http://short.url/" + shorturl

    existing_url = find_shorturl(session, url)
    if not existing_url:
        raise HTTPException(status_code=400, detail="Invalid url")
    
    # #return {"Original site " : original_site}
    return redirect_shorturl(existing_url)