# COMANDO EXECUTAR SERVER LOCAL: uvicorn main:app --reload

from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)


@app.get("/")
async def root():
    return {"mensagem": "API rodando com sucesso!"}


# endpoint:
# /ordens

# CRUD
# Rest APIs
# Get -> leitura/pegar
# Post -> enviar/criar
# Put/Path -> edição
# Delete -> deletar