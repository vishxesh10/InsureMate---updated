"""Prediction endpoint router."""
from fastapi import APIRouter
from insuremate.models import Userinput
from insuremate.services.predict import predict_from_user

router = APIRouter()


@router.post("/predict")
def predict(data: Userinput):
    prediction, db_record = predict_from_user(data)
    return {
        "predicted_category": prediction,
        "result_id": db_record.id,
        "message": "Prediction saved successfully"
    }
