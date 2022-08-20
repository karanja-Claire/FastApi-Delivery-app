from fastapi import APIRouter,Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from flask_login import current_user
import sqlalchemy
import models
import schemas
from database import Base, engine
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix ='/orders',
    tags = ['orders']
)


@order_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail ="invalid Token")
    return {"message":"hello cats"}


@order_router.post('/order', status_code = status.HTTP_201_CREATED)
async def place_an_order(request:schemas.OrderModel, Authorize:AuthJWT=Depends()):
    session = Session(bind=engine, expire_on_commit=False)

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail ="invalid Token")
    
    #getting current user details
    current_user = Authorize.get_jwt_subject()
    #checking whether the current user details match in the database
    user = session.query(models.User).filter(models.User.username==current_user).first()

    #we are creating an instance of the orders(choice)database table
    new_order = models.Choice(
        pizza_size = request.pizza_size,
        quantity = request.quantity
    )
    #we are using relationships to get the request order with the credentials of the user that placed the order
    # user = relationship('User', back_populates = 'orders')
    #new_order.user(from the choice table  the attribute user)
    new_order.user=user

    session.add(new_order)
    session.commit()

    response ={
        "pizza_size":new_order.pizza_size,
        "quantity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status
        }

    return jsonable_encoder(response)


@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends()):
    session = Session(bind=engine, expire_on_commit=False)
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail ="invalid Token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(models.User).filter(models.User.username==current_user).first()

    #after checking the current user we will check if the user is a superuser

    if user.is_staff:
        orders = session.query(models.Choice).all()
        return jsonable_encoder(orders)
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail ="you are not a superuser")



@order_router.get('/orders/{id}')
async def get_order_by_id(id:int, Authorize:AuthJWT=Depends()):
    session = Session(bind=engine, expire_on_commit=False)
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail ="invalid Token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(models.User).filter(models.User.username==current_user).first()
    #we want to know if current user is a superuser since only superuser can only access the records
    if user.is_staff:
        order = session.query(models.Choice).filter(models.Choice.id == id).first()

        return jsonable_encoder(order)
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail ="you dont have administrative access")


@order_router.get('/user/orders')
async def get_users_orders(Authorize:AuthJWT=Depends()):
    session = Session(bind=engine, expire_on_commit=False)
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail ="invalid Token")
    

    user = Authorize.get_jwt_subject()
    print(user)
    orders = session.query(models.User).join(models.Choice, models.User.id == models.Choice.user_id).add_columns(models.User.orders).filter(models.User.username==user).first()
    print(current_user)

    return jsonable_encoder(orders)


#------------------------------------------------------------

#-----------------------------------------------------------


@order_router.get('/user/order/{id}/')
async def get_specific_order(id:int,Authorize:AuthJWT=Depends()):
    session = Session(bind=engine, expire_on_commit=False)
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail ="invalid Token")

    
    current_user = Authorize.get_jwt_subject()
    user = session.query(models.User).filter(models.User.username==current_user).first()

    orders = user.orders

    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)

    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail ="no order with such id")