from .. import models, schemas, utils, oauth2
from app.oauth2 import get_current_user
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from sqlalchemy import func 

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()
    #print(current_user.email)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.Post, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ",(post.title, post.content, post.published))
    #post = cursor.fetchone()
    #conn.commit()
    #print(post.dict())
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
#title str, content str, category,

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #cursor.execute("SELECT * from posts WHERE id = %s", (str(id),))
    #post = cursor.fetchone()
    #new_post = db.query(models.Post).get(id)
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return results

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #cursor.execute("DELETE from posts WHERE id = %s RETURNING *", (str(id),))
    #post = cursor.fetchone()
    #conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post.first()
    #print(deleted_post.owner_id)
    print(current_user.id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to delete post")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.ResponsePost)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
     #(post.title, post.content, post.published, str(id)))
    #post = cursor.fetchone()
    #conn.commit()
    query = db.query(models.Post).filter(models.Post.id == id)
    new_post = query.first()
    if new_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if new_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to delete post")

    query.update(post.dict(), False)
    db.commit()
    return new_post.first()