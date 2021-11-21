# from sqlalchemy.sql.schema import Column
from fastapi import FastAPI  # , Response, status, HTTPException, Depends
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
# from typing import Optional, List
# from sqlalchemy.orm import Session
from . import models
from .schemas import *
from .database import engine
from .routers import post, user, auth, vote
from pydantic import BaseSettings
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind=engine)
# esse cmnd fl p sqlalchemy p rodar o cmnd create p gerar as tbls qnd roda d inc,mas agr cm alembic n prcs dl
# middleware é tp fnç q roda antes d td request
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_posts = [{'title': 'favorite foods', 'content': 'I like pizza', "id": 1}]


# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {'message': 'hello world'}
