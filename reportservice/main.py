from fastapi import FastAPI, HTTPException
from client import get_report_data
import uuid
import boto3

app = FastAPI()

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

@app.get("/report")
async def generate_report():
    try:
        return get_report_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import json
@app.get("/report/file")
async def get_report_file():
    try:
        report_data = get_report_data()
        file_name = f"report_{uuid.uuid4()}.json"
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(report_data).encode('utf-8'))
        return {"file_name": file_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)