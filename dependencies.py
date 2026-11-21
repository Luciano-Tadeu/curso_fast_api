from models import db
from sqlalchemy.orm import sessionmaker, Session
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

def pegar_sessao():
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        usuario_id = int(dic_info.get("sub")) 
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    # verificar se o token é válido
    # extrair o ID do usuário do token
    usuario = session.query(Usuario).filter(Usuario.id==usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Negado")
    return usuario