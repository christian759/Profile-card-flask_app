from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)

class Person(db.Model):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(primary_key=True)
    UserName: Mapped[str]
    Age: Mapped[int] 
    Gender: Mapped[str] 
    Email: Mapped[str]
    Location: Mapped[str] 
    About: Mapped[str] 
    Photo: Mapped[str] 
