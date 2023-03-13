from secrets import token_hex
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import CONN, Pessoas, Tokens
import hashlib

app = FastAPI()


def conecta_banco():
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


def verifica_dados(user, senha):
    if len(user) > 20 or len(user) < 3:
        return 'Usuário não pode ser maior que 20 ou menor que 3 caracteres'
    elif len(senha) > 10 or len(senha) < 3:
        return 'Senha maior que 10 ou menor que 3 caracteres'

    return {'status': 'cadastro efetuado!'}


@app.post('/cadastro')
def cadastrar(nome: str, user: str, senha: str):
    session = conecta_banco()

    dados_verificados = verifica_dados(user, senha)
    if dados_verificados != 1:

        usuario = session.query(Pessoas).filter_by(usuario=user, senha=senha).all()
        if len(usuario) == 0:
            senha = hashlib.sha256(senha.encode()).hexdigest()
            x = Pessoas(nome=nome, usuario=user, senha=senha)
            session.add(x)
            session.commit()
            return {'status': 'cadastro efetuado!'}

        elif len(usuario) > 0:
            return {'status': 'usuario já cadastrado'}


@app.post('/login')
def login(usuario: str, senha: str):
    session = conecta_banco()
    senha = hashlib.sha256(senha.encode()).hexdigest()
    user = session.query(Pessoas).filter_by(usuario=usuario, senha=senha).all()
    if len(user) == 0:
        return {'status': 'usuário inexistente!'}

    while True:
        token = token_hex(50)
        tokenExiste = session.query(Tokens).filter_by(token=token).all()
        if len(tokenExiste) == 0:
            pessoaExiste = session.query(Tokens).filter_by(id_pessoa=user[0].id).all()
            if len(pessoaExiste) == 0:
                novoToken = Tokens(id_pessoa=user[0].id, token=token)
                session.add(novoToken)
            elif len(pessoaExiste) > 0:
                pessoaExiste[0].token = token

            session.commit()
            break

        return token

    if len(user) > 0:
        return {'logado': True}