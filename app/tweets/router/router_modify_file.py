from fastapi.responses import JSONResponse
from fastapi import Depends, UploadFile, File
from typing import List
import io
from ..service import Service, get_service
from . import router


@router.post("/upload/{tweet_id:str}")
def upload_file(
    tweet_id: str,
    files: List[UploadFile] = File(...),
    svc: Service = Depends(get_service),
):
    result = []
    for file in files:
        file_object = file.file
        filename = file.filename
        file_bytes = file_object.read()
        file_stream = io.BytesIO(file_bytes)
        url = svc.s3_service.upload_file_by_tweet(file_stream, filename, tweet_id)
        result.append(url)
    return {"msg": result}


@router.get("/get/{tweet_id:str}")
def get_file(
    tweet_id: str,
    svc: Service = Depends(get_service),
):
    file_path = svc.s3_service.get_file_by_tweet(tweet_id)
    if file_path is None:
        return JSONResponse(
            status_code=404,
            content={"message": "File not found."},
        )

    # Construct the desired JSON response
    response_data = {
        "_id": tweet_id,
        "type": "rent",
        "price": 150000,
        "address": "Астана, Алматы р-н, ул. Нажимеденова, 16 – Сарыколь",
        "area": 46.5,
        "rooms_count": 2,
        "description": "...",
        "user_id": "{user_id пользователя создавшего объявление}",
        "media": [f"https://{svc.s3_service.bucket}/{file_path.split('/')[-1]}"],
    }

    return response_data



