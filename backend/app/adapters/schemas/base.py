from pydantic import BaseModel

class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True
