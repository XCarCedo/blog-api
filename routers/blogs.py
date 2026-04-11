from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db.models.blogs import Blog
from dependencies.auth import UserDep, SuperUserDep
from dependencies.database import SessionDep
from schemas.blogs import BlogPublic, BlogCreate, BlogUpdate

router = APIRouter(prefix="/blog")

@router.post("/", response_model=BlogPublic)
async def create_blog(user: SuperUserDep, session: SessionDep, blog: BlogCreate):
    new_blog = Blog(**blog.model_dump())
    session.add(new_blog)
    session.commit()
    session.refresh(new_blog)

    return new_blog

@router.get("/", response_model=list[BlogPublic])
async def get_all_blogs(user: UserDep, session: SessionDep):
    blogs = session.exec(select(Blog)).all()
    return blogs

@router.get("/{blog_id}", response_model=BlogPublic)
async def get_blog_by_id(user: UserDep, blog_id: int, session: SessionDep):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Couldn't find a Blog with id of {str(blog_id)!r}")

    return blog

@router.put("/{blog_id}", response_model=BlogPublic)
@router.patch("/{blog_id}", response_model=BlogPublic)
async def update_blog(user: SuperUserDep, blog_id: int, session: SessionDep, blog_update: BlogUpdate):
    db_blog = session.get(Blog, blog_id)
    if not db_blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Couldn't find a Blog with id of {str(blog_id)!r}")
    
    update_data = blog_update.model_dump(exclude_unset=True)
    db_blog.sqlmodel_update(update_data)
    session.add(db_blog)
    session.commit()
    session.refresh(db_blog)

    return db_blog

@router.delete("/{blog_id}")
async def delete_blog(user: SuperUserDep, blog_id: int, session: SessionDep):
    db_blog = session.get(Blog, blog_id)
    if not db_blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Couldn't find a Blog with id of {str(blog_id)!r}")
    
    session.delete(db_blog)
    session.commit()
    return {"ok":True}