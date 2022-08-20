from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey,Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
# Define To Do class inheriting from Base
class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique = True)
    email = Column(String(80), unique = True)
    password = Column(Text, nullable = True)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False )
    orders = relationship('Choice', back_populates = 'user', lazy="joined")

    def __repr__(self):
        return f"<User {self.username} "


class Choice(Base):
    ORDER_STATUSES = [
        ('PENDING', 'pending'),
        ('IN-TRANSIT','in-transit'),
        ('DELIVERED','delivered')  
    ]

    PIZZA_SIZES= [
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large'),
        ('EXTRA LARGE','extra large')
    ]
    
    __tablename__='Orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable = False)
    order_status= Column(ChoiceType(ORDER_STATUSES),default = "PENDING")
    pizza_size = Column(ChoiceType(PIZZA_SIZES), default = "SMALL")
    user_id = Column(Integer,ForeignKey('Users.id'))
    user = relationship('User', back_populates = 'orders')

    def __repr__(self):
        return f"<Choice {self.id}>" 



