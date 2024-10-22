from sqlalchemy.orm import Session

from . import models, schemas

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def create_event(db: Session, id:int, name: str, date: str, area:str):
    db_event = models.Event(id=id, name=name, date=date, area=area)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event_by_name(db: Session, name: str):
    return db.query(models.Event).filter(models.Event.name == name).first()

def delete_event(db: Session, id:int):
    db_event = db.query(models.Event).filter(models.Event.id==id).first()
    db.delete(db_event)
    db.commit()