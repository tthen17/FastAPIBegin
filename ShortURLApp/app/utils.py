import hashlib
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from . import models, schemas

def get_short_url(original_url: str) -> str:
    base_url = "http://short.url/"
    hash_value = hashlib.md5(original_url.encode()).hexdigest()[:6]
    short_url = base_url + hash_value
    return short_url

def find_shorturl(db: Session, new_short_url: str):
    return db.query(models.Url).filter_by(short_url=new_short_url).first()

def create_shorturl(db: Session, new_short_url: str, url: str):
    new_url = models.Url(short_url=new_short_url, original_url=url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return {"Shorturl created " : new_short_url}

def redirect_shorturl(existing_url:models.Url):
    original_site = '/'+existing_url.original_url
    response = RedirectResponse(url=original_site)
    return response