from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.schemas.detection import DetectionResponse
from app.dl.disease_detector import detect_disease_and_pests

router = APIRouter(prefix="/detect", tags=["Disease & Pest Detection"])


@router.post(
    "/disease",
    response_model=DetectionResponse,
    summary="Detect plant diseases and pests from image",
    description=(
        "Upload a leaf or plant image (JPEG/PNG). The image is evaluated against 13 specialized "
        "YOLO computer vision models for Rice, Maize, Banana, Mango, Orange, Watermelon, Grapes, "
        "Beans, and Pomegranate. Returns annotated bounding boxes, detected condition, confidence, "
        "and agronomic recommendations."
    ),
)
async def detect_disease(
    file: UploadFile = File(..., description="Plant or leaf image file"),
    target_crop: Optional[str] = Form(None, description="Optional target crop to prioritize detection"),
):
    # Validate mime type
    if file.content_type not in ["image/jpeg", "image/png", "image/webp", "image/jpg"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image type '{file.content_type}'. Please upload JPEG, PNG, or WebP."
        )

    # Read bytes with size limit (15MB)
    contents = await file.read()
    if len(contents) > 15 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image file exceeds 15MB size limit.")

    try:
        result = detect_disease_and_pests(contents, target_crop=target_crop)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection error: {str(e)}")
