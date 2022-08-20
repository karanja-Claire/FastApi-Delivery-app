from fastapi import FastAPI
from database import Base, engine
from sqlalchemy.orm import Session
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings
# Create the database
Base.metadata.create_all(engine)
# Initialize app
app = FastAPI()

@AuthJWT.load_config
def getconfig():
    return Settings()


app.include_router(auth_router)
app.include_router(order_router)




