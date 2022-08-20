from fastapi import APIRouter, status, HTTPException, Depends
from database import Base, engine
import models
import schemas
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder#this jsonable_encoder is the same as jsonify in flask as it turns dictionary into json
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash



auth_router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
    

)


@auth_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    try: 
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "invalid Token")
    
    return {"message":"hello  new cats"}
                                                   

@auth_router.post('/signup', response_model =schemas.Signup, status_code=status.HTTP_201_CREATED )
async def signup(request:schemas.Signup):
    session = Session(bind=engine, expire_on_commit=False)
    #we will first check whether the given email already exits in the database
    db_email = session.query(models.User).filter(models.User.email == request.email).first()
    
    # a fallback that handles when a user with the same credentials is created more than once 
    if db_email is not None:
        raise HTTPException (status_code = status. HTTP_400_BAD_REQUEST,
        detail = "User  with the email already exists" ) 
    #this means if the new user exists then it should raise the error
    '''not none, the none keyword is used to define a null value or no value at all'''
    db_username= session.query(models.User).filter(models.User.username == request.username).first()
    
    if db_username is not None:
        raise HTTPException (status_code = status. HTTP_400_BAD_REQUEST,
        detail = "User  with the the username  already exists" ) 
    #creating a new user object that will handle all the inputs
    new_user = models.User(
        username =request.username,
        email = request.email,
        password = generate_password_hash(request.password),
        is_active = request.is_active,
        is_staff = request.is_staff)
    
    
    #saving the new user object in the database
    session.add(new_user)
    session.commit()

    return new_user


@auth_router.post('/login' )
async def login(request:schemas.LoginModel, Authorize:AuthJWT=Depends()):
   session = Session(bind=engine, expire_on_commit=False)
   db_user=session.query(models.User).filter(models.User.username==request.username).first()
   #we are checking whether the user exists inorder we give the user a jwt and if a user doesnot exist we raise a http exception

   if db_user and check_password_hash(db_user.password, request.password):
       #we are checing whether the user an the password match in the db
       access_token = Authorize.create_access_token(subject=db_user.username)
       refresh_token=Authorize.create_refresh_token(subject = db_user.username)

       response ={
           "access":access_token,
           "refresh":refresh_token
       } 
       return jsonable_encoder(response)




       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid username or password")

#refreshing tokens
@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please provid a valid refresh code")
    
    current_user = Authorize.get_jwt_subject()
    
    access_token = Authorize.create_access_token(subject = current_user)

    return jsonable_encoder({"access":access_token})