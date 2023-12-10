from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Numeric, desc, update
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.sql import func
from fastapi import HTTPException, Depends, Body, FastAPI
import AuthGrocery
from typing import Optional
from pydantic import BaseModel, validator, ValidationError
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

aws_mysql_config = {
    "username": "supersavers",
    "password": "Superdoc69*",
    "host": "supersaver.cbbcfmfp6t7q.us-east-1.rds.amazonaws.com",
    "port": "3306",
    "database": "supersaver",
}

connection_string = f"mysql+mysqlconnector://{aws_mysql_config['username']}:{aws_mysql_config['password']}@{aws_mysql_config['host']}:{aws_mysql_config['port']}/{aws_mysql_config['database']}"

engine = create_engine(connection_string, pool_pre_ping=True)
Base = declarative_base()

# Model for the cart
class ItemCart(BaseModel):
    user: Optional[str] = None
    name: str
    old_price: float
    new_price: float
    quantity: int
    image: str
    description: str
    source: str
    
@validator("quantity")
def validate_quantity(cls, value):
        if not 0 <= value <= 100:
            raise ValueError("Quantity should be between 0 and 100.")
        return value

@validator("old_price", "new_price")
def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price should be a positive number.")
        return value

class ItemIdentity(BaseModel):
    name: str

class CartItem(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(length=50), index=True)
    name = Column(String(length=100))
    bought = Column(Boolean, default=False)
    quantity = Column(Integer)
    old_price = Column(Numeric(precision=10, scale=2))
    new_price = Column(Numeric(precision=10, scale=2))
    source = Column(String(length=100))
    description = Column(String(length=255))
    image = Column(String(length=255))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=True, bind=engine)

app = FastAPI()

async def saving(
    current_user: str = Depends(AuthGrocery.UserManager.get_current_user),
    db = SessionLocal()
) -> dict:
    try:
        existing_items = (
            db.query(CartItem)
            .filter_by(user=current_user, bought=True)
            .all()
        )
        diff = 0
        for x in existing_items:
            saving = (x.old_price - x.new_price) * x.quantity
            diff = diff + saving
        db.commit()
        return diff
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

async def add_to_cart(
    item: ItemCart = Body(...),
    current_user: str = Depends(AuthGrocery.UserManager.get_current_user),
    db=SessionLocal()
) -> dict:
    try:


        existing_items = (
            db.query(CartItem)
            .filter_by(user=current_user, name=item.name)
            .all()
        )

        if existing_items and any(not item.bought for item in existing_items):
            # If there are existing unbought items, add quantity to them
            for existing_item in existing_items:
                if not existing_item.bought:
                    existing_item.quantity += item.quantity

        else:
            # If no unbought items, or item is not in the list, create a new item
            if item.quantity > 1000 or item.quantity<0 or item.old_price<0 or item.new_price<0 :
                raise HTTPException(status_code=422, detail=f"Input validation error: {e}")
            
            new_item = CartItem(
                user=current_user,
                name=item.name,
                bought=False,
                old_price=item.old_price,
                new_price=item.new_price,
                source=item.source,
                quantity=item.quantity,
                description=item.description,
                image=item.image,
            )
            db.add(new_item)

        db.commit()
        return {"message": "Item added to the cart successfully."}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Input validation error: {e}")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    

async def change_bought(
    item: ItemIdentity = Body(...),
    current_user: str = Depends(AuthGrocery.UserManager.get_current_user),
    db = SessionLocal()
):
    try:
        # Update all items with the given name for the current user where bought is False
        db.query(CartItem).filter(CartItem.user == current_user, CartItem.name == item.name, CartItem.bought == False).update({"bought": True, "timestamp": datetime.now()})
        db.commit()
        return {"message": f"All unbought items with name '{item.name}' marked as bought successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

async def increment(
    item: ItemIdentity = Body(...),
    current_user: str = Depends(AuthGrocery.UserManager.get_current_user),
    db = SessionLocal()
):
    try:
        existing_item = (
            db.query(CartItem)
            .filter_by(user=current_user, name=item.name, bought=False)
            .first()
        )

        if existing_item:
            if existing_item.quantity < 100:
                existing_item.quantity = existing_item.quantity + 1
                existing_item.timestamp = datetime.utcnow()
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Item '{item.name}' not found in the cart for user {current_user}."
            )

        db.commit()
        return {"message": f"Item '{item.name}' Quantity has decreased"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

async def decrement(
    item: ItemIdentity = Body(...),
    current_user: str = Depends(AuthGrocery.UserManager.get_current_user),
    db = SessionLocal()
):
    try:
        existing_item = (
            db.query(CartItem)
            .filter_by(user=current_user, name=item.name, bought=False)
            .first()
        )

        if existing_item:
            if existing_item.quantity > 0:
                existing_item.quantity = existing_item.quantity - 1
                existing_item.timestamp = datetime.utcnow()
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Item '{item.name}' not found in the cart for user {current_user}."
            )

        db.commit()
        return {"message": f"Item '{item.name}' Quantity has decreased"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

async def get_cart_items_bought(current_user: str = Depends(AuthGrocery.UserManager.get_current_user), db = SessionLocal()):
    try:
        unbought_items = db.query(CartItem).filter(CartItem.user == current_user, CartItem.bought==True).order_by(desc(CartItem.timestamp)).all()

        # Convert CartItem objects to instances of Item
        unbought_items_as_items = [
            ItemCart(
                user=item.user,
                name=item.name,
                old_price=float(item.old_price),
                new_price=float(item.new_price),
                quantity=item.quantity,
                image=item.image,
                description=item.description,
                source=item.source
            )
            for item in unbought_items
        ]
        db.commit()
        return unbought_items_as_items
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

async def get_cart_items_unbought(
    current_user: str = Depends(AuthGrocery.UserManager.get_current_user),
    db: Session =  SessionLocal()
):
    try:
        unbought_items = db.query(CartItem).filter(CartItem.user == current_user, CartItem.bought==False).all()

        # Convert CartItem objects to instances of Item
        unbought_items_as_items = [
            ItemCart(
                user=item.user,
                name=item.name,
                old_price=float(item.old_price),
                new_price=float(item.new_price),
                quantity=item.quantity,
                image=item.image,
                description=item.description,
                source=item.source
            )
            for item in unbought_items
        ]
        db.commit()
        return unbought_items_as_items

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

async def remove_from_cart(
    item_id: int = Body(...),
    current_user: str = Depends(AuthGrocery.UserManager.get_current_user),
    db = SessionLocal()
):
    try:
        item_to_remove = db.query(CartItem).filter(CartItem.name == item_id.name, CartItem.user == current_user, CartItem.bought == False).first()

        if item_to_remove:
            db.delete(item_to_remove)
            db.commit()
            return {"message": f"Item {item_id} removed from the cart successfully."}
        else:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found in the cart.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
