from typing import Union, List
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer

app = FastAPI()

# SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///./db.sqlite3:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# A SQLAlchemny ORM Place
class DBItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String, nullable=True)
    price = Column(Float)
    is_offer = Column(Boolean)


Base.metadata.create_all(bind=engine)


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_offer: Union[bool, None] = None

    class Config:
        orm_mode = True


# Methods for interacting with the database
def get_item(db: Session, item_id: int):
    return db.query(DBItem).where(DBItem.id == item_id).first()


def get_items(db: Session):
    return db.query(DBItem).all()


def create_item(db: Session, item: Item):
    db_item = DBItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Put Fixed Paths First
@app.get("/")
def read_root():
    return {"msg": "Welcome to my Online Cafe!"}


# you can declare path parameters or variables with the same syntax used by Python formatted strings
@app.get("/list/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db), q: Union[str, None] = None):
    # item_id will be passed to the handler as an argument
    # return {"item_id": item_id, "q": q}
    return get_item(db, item_id)


@app.put("/update/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    for key, val in item.dict().items():
        setattr(db_item, key, val)
    db.commit()
    return get_item(db, item_id)


@app.post("/add", response_model=Item)
def add_item(item: Item, db: Session = Depends(get_db)):
    db_item = create_item(db, item)
    return db_item


@app.get("/list", response_model=List[Item])
def list_items(db: Session = Depends(get_db)):
    return get_items(db)


@app.delete("/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        db.query(DBItem).where(DBItem.id == item_id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)
    return {"delete status:", "Success!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("toy_item_example:app", reload=True)
