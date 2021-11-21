# .. é p vltr 1 drtr
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# obs->o tp d dd q vc clc p current_user n md nd em cm o cod fnc


@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute(""" SELECT * FROM posts""")
    #posts = cursor.fetchall()
    # .filter(models.Post.id==current_user.id).all() usava isso se quisesse q so rtrn os posts dql usr espcfc
    print(limit)
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts  # o fast api auto serializa ele p


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# esse Body(...) extrai tds fields d body d response,vira dcnr e clc n vr payload
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # payload: dict = Body(...)
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # # fzr dss frm sem ser f str bloqueia a pssbldd d ter sql injection
    # new_post = cursor.fetchone()
    # conn.commit()
    # clc tds os vls em tds os fields sem prcsr fzr n mao
    new_post = models.Post(owner_id=current_user.id, ** post.dict())
    print(current_user.email)
    db.add(new_post)
    db.commit()
    # é tp o returning *,ele pg o vl d newpost e armzn n prpr newpost
    db.refresh(new_post)
    return new_post

# qnd extrai os dds e clc n prmtr,é clcd cm mdl pydantic,tds tm o mtd .dict p converter p dncr py
# protcolo PUT atlz tds fields (msm q seja p clc o msm vl) e PATCH só atlz um field,mas tanto faz n pratica


# td vl d prmtr d url SMPR sera str
@router.get('/{id}', response_model=schemas.PostOut)
# esse :int converte drt p int | [, response: Response]
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",
    #                (str(id)))  # ele fl q da prblm as vezes s n clc vrgl
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND ou só 404
        # return {'message': f'post with id : {id} was not found'}

    return post


""" obs-> qnd for fzr a ordem ds fnçs d oprçs path,vc tm q clc as q tm vrs
por ult,q ai o fastapi n confunde as vrs cm os vls ds urls d vdd,e ai n da
um bug totalmente desnecessario ou md a url p ter crtz"""


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)  # a query
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            details=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            details=f"Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
# em vez d ns prmtrs so clc o db:Session=Depends(get_db),pd so imprtr,mas essa cm prmtr dx testar mais facil
