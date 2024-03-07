import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    name: Mapped[str]
    surname: Mapped[str]


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[intpk]
    name: Mapped[str]


class Fruit(Base):
    __tablename__ = 'fruits'

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]
    price_for_kg: Mapped[float]
    total_quantity: Mapped[int]
    rating: Mapped[float] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete='CASCADE'))

    category: Mapped["Category"] = relationship()


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    total_price: Mapped[float] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship()


class OrderProduct(Base):
    __tablename__ = 'order_products'

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("fruits.id", ondelete="CASCADE"))
    quantity: Mapped[int]
    total_price: Mapped[float]


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=True)
    session_key: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)


class CartProduct(Base):
    __tablename__ = 'cart_products'

    id: Mapped[intpk]
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("fruits.id", ondelete="CASCADE"))
    quantity: Mapped[int]
    total_price: Mapped[float]


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[intpk]
    rating: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    fruit_id: Mapped[int] = mapped_column(ForeignKey("fruits.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
