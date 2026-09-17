from fastapi import FastAPI
from db_models import Base
from database import engine


from routers.products import router as products_router
from routers.users import router as users_router
from routers.auth import router as auth_router




app = FastAPI()

app.include_router(products_router)
app.include_router(users_router)
app.include_router(auth_router)












