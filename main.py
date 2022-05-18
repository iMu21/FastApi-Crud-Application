from fastapi import Depends, FastAPI,Depends
import schema,models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog')
def create(request:schema.blog,db:Session=Depends(get_db)):
    new_blog = models.blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db:Session=Depends(get_db)):
    blogs = db.query(models.blog).all()
    return blogs

@app.get('/blog/{id:int}')
def show(id,db:Session=Depends(get_db)):
    blog = db.query(models.blog).filter(models.blog.id==id).first()
    return blog

@app.delete('/blog/{id:int}')
def destroy(id,request:schema.blog,db:Session=Depends(get_db)):
    db.query(models.blog).filter(models.blog.id==id).update(request)
    db.commit()
    return {'msg':'updated'}

app.put('/blog/{id:int}')
def update(id,db:Session=Depends(get_db)):
    db.query(models.blog).filter(models.blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {'msg':'deleted'}