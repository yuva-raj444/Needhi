"""
NyayaSahaya — Legal issue classifier endpoint.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ClassifyRequest, ClassifyResponse
from app.services.classifier_service import ClassifierService

router = APIRouter()


@router.post("/", response_model=ClassifyResponse)
async def classify_legal_issue(request: ClassifyRequest):
    """
    Classify a legal issue into a category: Criminal, Civil, Family, Consumer, Land, Welfare.
    Supports Tamil and English input.
    """
    try:
        classifier = ClassifierService()
        result = await classifier.classify(request.description)
        return ClassifyResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")
