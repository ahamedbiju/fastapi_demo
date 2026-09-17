from sqlalchemy.orm import DeclarativeBase , Mapped, mapped_column, relationship
from sqlalchemy import Integer,String,Float,ForeignKey
   

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    products: Mapped[list["Product"]] = relationship(back_populates="owner")
    hashed_password: Mapped[str] = mapped_column(String(255))

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="products")
