from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.responses import RedirectResponse #used to redirect after finishing func
from fastapi.templating import Jinja2Templates #used to load html template
# from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine) #DB tables created here
app = FastAPI()

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/") #load root main page
async def root(request: Request, db: Session = Depends(get_db)):
   events = crud.get_events(db=db) #RETRIEVE SCHEDULE FROM POSTGRES  
   return templates.TemplateResponse("scheduler.html", {"request":request,"eventdict":events}) #RETURN SCHEDULE TO SITE

@app.get("/add") #load root main page
async def root(request: Request, db: Session = Depends(get_db)):
   events = crud.get_events(db=db) #RETRIEVE SCHEDULE FROM POSTGRES  
   return templates.TemplateResponse("add.html", {"request":request,"eventdict":events}) #RETURN SCHEDULE TO SITE



@app.post("/add/addevent", response_model=schemas.Event)
async def add_event(request:Request, db: Session = Depends(get_db),):
    events = crud.get_events(db=db)
    idcount = 0
    for i in events:
        idcount+=1
    id = idcount+1
    formdata = await request.form()
    event_name = formdata["event_name"]
    event_date = formdata["event_date"]
    event_area = formdata["event_area"]
    db_event = crud.get_event_by_name(db, name=event_name)
    if db_event:
        raise HTTPException(status_code=400, detail="Event exists")
    crud.create_event(db=db, id=id, name=event_name, date=event_date, area=event_area)
    return RedirectResponse("/",303)

@app.get("/delete/{id}")
async def delete_event(id:int, db: Session = Depends(get_db)):
    crud.delete_event(db=db, id=id)
    return RedirectResponse("/",303)