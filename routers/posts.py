# routers/posts.py
from fastapi import APIRouter, Depends, HTTPException
from schemas import PostCreate, Post, Like, Comment
from dependencies import get_current_user
from database import fake_posts_db, fake_likes_db, fake_comments_db
from typing import List

router = APIRouter(prefix="/posts", tags=["Posts"])

# Create a post
@router.post("/", response_model=Post)
def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    post_id = len(fake_posts_db) + 1
    new_post = {"id": post_id, "text": post.text, "owner_id": current_user["id"]}
    fake_posts_db.append(new_post)
    return new_post

# Get all posts
@router.get("/", response_model=List[Post])
def get_all_posts():
    return fake_posts_db

# Delete a post
@router.delete("/{post_id}")
def delete_post(post_id: int, current_user: dict = Depends(get_current_user)):
    for post in fake_posts_db:
        if post["id"] == post_id:
            if post["owner_id"] != current_user["id"]:
                raise HTTPException(status_code=403, detail="Not authorized to delete this post")
            fake_posts_db.remove(post)
            return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")

# Like a post
@router.post("/like", response_model=Like)
def like_post(like: Like, current_user: dict = Depends(get_current_user)):
    # Ensure post exists
    post_exists = any(post["id"] == like.post_id for post in fake_posts_db)
    if not post_exists:
        raise HTTPException(status_code=404, detail="Post not found")

    fake_likes_db.append({"post_id": like.post_id, "user_id": current_user["id"]})
    return {"post_id": like.post_id, "user_id": current_user["id"]}

# Comment on a post
@router.post("/comment", response_model=Comment)
def comment_post(comment: Comment, current_user: dict = Depends(get_current_user)):
    post_exists = any(post["id"] == comment.post_id for post in fake_posts_db)
    if not post_exists:
        raise HTTPException(status_code=404, detail="Post not found")

    fake_comments_db.append({
        "post_id": comment.post_id,
        "user_id": current_user["id"],
        "text": comment.text
    })
    return {"post_id": comment.post_id, "user_id": current_user["id"], "text": comment.text}
