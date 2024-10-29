from pydantic import BaseModel

class UrlCreate(BaseModel):
    original_url: str