from .. import models, schemas, utils, oauth2
from app.oauth2 import get_current_user
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db 

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote_info: schemas.Vote,  db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_id = vote_info.post_id
    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id:{post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == post_id, models.Vote.user_id == current_user.id)
    prev_vote = vote_query.first()
    
    if vote_info.vote_dir == 1:
        if prev_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You already voted in the post of id: {post_id}")

        new_vote = models.Vote(user_id=current_user.id, post_id=vote_info.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "You voted successfully"}
    else:
        if not prev_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}




   
    
