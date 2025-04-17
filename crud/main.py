from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlmodel import Session
from models import Manager
from database import get_session, init_db
from uuid import UUID
import requests
import boto3

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database on startup
    from models import Manager
    from base import BASE, engine
    BASE.metadata.create_all(bind=engine)
    yield
    # Clean up resources on shutdown (if needed)
    print("Shutting down...")

REPOERT_SERVICE_URL = "http://reportservice:8000"

access_key = "minioadmin"
secret_key = "minioadmin"
endpoint_url = "http://minio:9000"

s3_client = boto3.client(
    "s3",
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

bucket_name = "main"
try:
    s3_client.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created successfully.")
except Exception:
    print("cant create bucket, already exists")

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
    report = requests.get(REPOERT_SERVICE_URL + "/report/file").json()
    print(report)
    return report

@app.get("/reports/file")
def generate_report(session: Session = Depends(get_session)):
    report = requests.get(REPOERT_SERVICE_URL + "/report/file").json()
    print(report)
    return report

@app.get("/reports/report_file/{report_id}")
def get_report(report_id: str, session: Session = Depends(get_session)):
    s3_client.download_file(bucket_name, f"{report_id}", f"{report_id}")
    return FileResponse(f"{report_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)