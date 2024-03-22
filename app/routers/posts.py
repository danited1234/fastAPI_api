# import psycopg2
# from psycopg2.extras import RealDictCursor


# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost',database = "fastapi",user = 'postgres',
#                                 password = "nestedloop0#",cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected To The Database")
#         break
#     except Exception as e:
#         print(f"Connection to the database failed Error\n{e}")
#         time.sleep(2)
    

from fastapi import HTTPException, status, Response, Depends,APIRouter
from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from . import oauth2

router = APIRouter(prefix="/posts",
                   tags=['Posts'])


@router.get("/",response_model=List[schemas.Post])
async def get_post(db: Session = Depends(get_db)):
    posts= db.query(models.Post).all()

#     cursor.execute("""
# SELECT * FROM posts
#                    """)
# #     my_posts = cursor.fetchall()
#     return {"data":my_posts}
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_post(post:schemas.PostCreate,db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
#     cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *;
# """,(post.title,post.content,post.published))
#     post_dict = cursor.fetchone()
#     conn.commit()
#     return {"data":post_dict}
    return new_post

@router.get("/{id}",response_model=schemas.Post)
async def get_post_id(id:int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
#     cursor.execute("""
# SELECT * FROM posts WHERE id = %s;
# """,(str(id),))
#     posts = cursor.fetchone()
    if not post:
    # for posts in my_posts:
    #     if posts['id'] == id: #when we enter a path parementer it returns as a string
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    return post
        
 
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def update_post(id:int,post:schemas.PostCreate,db:Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                (post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    updated_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return updated_post.first()