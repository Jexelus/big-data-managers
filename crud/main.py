from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlmodel import Session
from models import Manager
from database import get_session, init_db
from uuid import UUID


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database on startup
    from models import Manager
    from base import BASE, engine
    BASE.metadata.create_all(bind=engine)
    yield
    # Clean up resources on shutdown (if needed)
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

@app.get("/", response_model=list[Manager])
def root(session: Session = Depends(get_session)):
    return session.query(Manager).all()

@app.get("/{manager_id}", response_model=Manager)
def get_manager(manager_id: UUID, session: Session = Depends(get_session)):
    manager = session.get(Manager, manager_id)
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manager not found")
    return manager

@app.post("/", response_model=Manager, status_code=status.HTTP_201_CREATED)
def create_manager(manager: Manager, session: Session = Depends(get_session)):
    session.add(manager)
    session.commit()
    session.refresh(manager)
    return manager

@app.put("/{manager_id}", response_model=Manager)
def update_manager(manager_id: UUID, updated_data: Manager, session: Session = Depends(get_session)):
    manager = session.get(Manager, manager_id)
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manager not found")
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(manager, key, value)
    session.commit()
    session.refresh(manager)
    return manager

@app.delete("/{manager_id}")
def delete_manager(manager_id: UUID, session: Session = Depends(get_session)):
    manager = session.get(Manager, manager_id)
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manager not found")
    session.delete(manager)
    session.commit()
    return {"message": "Manager deleted"}

@app.get("/reports/report")
def generate_report(session: Session = Depends(get_session)):
    managers = session.query(Manager).all()
    report = {str(manager.name): manager.contracts_count for manager in managers}
    return report


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)