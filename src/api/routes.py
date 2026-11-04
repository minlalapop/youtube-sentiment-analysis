
from fastapi import APIRouter

from .schemas import BatchRequest
from .predictor import predict


router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "model": "loaded"
    }


@router.post("/predict_batch")
def predict_batch(request: BatchRequest):
    return predict(request.comments)
