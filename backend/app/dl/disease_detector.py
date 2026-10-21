"""
disease_detector.py — Roboflow YOLO Vision Pipeline
Extracts multi-model computer vision disease and pest detection from run_notebook.py
"""
from __future__ import annotations
import os
import cv2
import numpy as np
import base64
import tempfile
import logging
from typing import Optional, Dict, Any, List, Tuple
from app.config import settings

logger = logging.getLogger(__name__)

# 13 Trained Agriculture Vision Models from Roboflow Universe
ROBOFLOW_MODELS = [
    {"crop": "Orange", "category": "Disease", "workspace": "citrus-leaf-disease", "project": "citrus-leaves-diseases-ykhpu"},
    {"crop": "Mango", "category": "Disease", "workspace": "mango-leaf-disease", "project": "mango-leaf-disease-kguxz"},
    {"crop": "Mango", "category": "Pest", "workspace": "project-pjsi8", "project": "mango-pests"},
    {"crop": "Watermelon", "category": "Disease", "workspace": "watermelon-diseases", "project": "watermelon-diseases"},
    {"crop": "Banana", "category": "Disease", "workspace": "tdtu-ocamc", "project": "banana-diseases-lrf9y"},
    {"crop": "Maize", "category": "Disease", "workspace": "detection-of-corn-crop-diseases-using-yolov8", "project": "maize-disease-dataset"},
    {"crop": "Maize", "category": "Pest", "workspace": "mo-qmyfx", "project": "maize-eloeo"},
    {"crop": "Beans", "category": "Disease", "workspace": "zhang-wen-hao-itjzq", "project": "beans-diseases"},
    {"crop": "Grapes", "category": "Disease", "workspace": "poramet-thongvichit", "project": "grape-leaf-disease-kf5ll"},
    {"crop": "Rice", "category": "Disease", "workspace": "riceleafdiseasedetection", "project": "rice-leaf-disease-s1asn"},
    {"crop": "Rice", "category": "Pest", "workspace": "rice-pest", "project": "rice-i9qwz"},
    {"crop": "Pomegranate", "category": "Disease + Pest", "workspace": "krish-verma-fayi1", "project": "pomegranate-disease-detection-29ocz"},
    {"crop": "Multiple Crops", "category": "Pest", "workspace": "yolo-dv5qa", "project": "pest-uruhn-yfh5t"},
]

MIN_CONFIDENCE = 40.0
INVALID_KEYWORDS = ["this dataset was exported", "roboflow.com", "exported via"]
DISEASE_KWS = ["disease", "spot", "blight", "mildew", "rust", "virus", "rot", "scab"]
PEST_KWS = ["pest", "insect", "worm", "bug", "aphid", "caterpillar", "borer", "hopper"]

_rf_client = None

def get_roboflow_client():
    global _rf_client
    if _rf_client is not None:
        return _rf_client
    try:
        from roboflow import Roboflow
        api_key = settings.ROBOFLOW_API_KEY
        if not api_key:
            raise ValueError("ROBOFLOW_API_KEY is not set.")
        _rf_client = Roboflow(api_key=api_key)
        return _rf_client
    except ImportError:
        logger.warning("roboflow library is not installed. Cloud YOLO inference will be unavailable until installed.")
        return None
    except Exception as e:
        logger.error(f"Error initializing Roboflow client: {e}")
        return None


def get_detection_color(cls_name: str) -> Tuple[int, int, int]:
    cls_lower = str(cls_name).lower()
    if any(w in cls_lower for w in DISEASE_KWS):
        return (0, 0, 220)    # Red for Disease (BGR)
    if any(w in cls_lower for w in PEST_KWS):
        return (0, 140, 255)  # Orange for Pest (BGR)
    return (0, 200, 0)        # Green for Healthy / General (BGR)


def annotate_image(
    image_bytes: bytes,
    detections: List[Dict[str, Any]]
) -> str:
    """Draw bounding boxes and labels on image, return base64 JPEG."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return ""

    img_h, img_w = img.shape[:2]
    scale_factor = max(img_h, img_w) / 800.0
    FONT_SCALE = max(0.4, 0.5 * scale_factor)
    TXT_THICK = max(1, int(1.2 * scale_factor))
    BOX_THICK = max(2, int(2.5 * scale_factor))

    for d in detections:
        x, y, w, h = d["bbox"]
        cls_name, conf = d["class_name"], d["confidence"]

        x1, y1 = int(x - w / 2), int(y - h / 2)
        x2, y2 = int(x + w / 2), int(y + h / 2)
        color = get_detection_color(cls_name)

        cv2.rectangle(img, (x1, y1), (x2, y2), color, BOX_THICK)
        label = f"{cls_name} {int(conf)}%"
        (tw, th), bl = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, TXT_THICK)
        txt_y = max(th + 5, y1)
        txt_x = max(0, min(x1, img_w - tw))
        cv2.rectangle(img, (txt_x, txt_y - th - 5), (txt_x + tw, txt_y + bl - 5), color, cv2.FILLED)
        cv2.putText(
            img, label, (txt_x, txt_y - 5),
            cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, (255, 255, 255), TXT_THICK
        )

    _, buffer = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    b64_str = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_str}"


def detect_disease_and_pests(
    image_bytes: bytes,
    target_crop: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run multi-model Roboflow YOLO detection on uploaded image.
    If target_crop is provided, filters to relevant models first for performance.
    """
    rf = get_roboflow_client()

    # Save to temp file for Roboflow API
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    all_detections = []
    models_to_scan = ROBOFLOW_MODELS

    # If target crop provided, prioritize that crop's models + generic pest model
    if target_crop:
        norm_crop = target_crop.strip().lower()
        prioritized = [
            m for m in ROBOFLOW_MODELS
            if norm_crop in m["crop"].lower() or m["crop"].lower() in norm_crop or m["crop"] == "Multiple Crops"
        ]
        if prioritized:
            models_to_scan = prioritized

    try:
        if rf is not None:
            for item in models_to_scan:
                crop, cat = item["crop"], item["category"]
                model_name_full = f"{crop} {cat}"
                try:
                    project = rf.workspace(item["workspace"]).project(item["project"])
                    # Load model safely
                    model = next((v.model for v in project.versions() if hasattr(v, "model") and v.model), None)
                    if not model:
                        model = next((v.models()[0] for v in project.versions() if hasattr(v, "models") and v.models()), None)
                    if not model:
                        continue

                    preds = model.predict(tmp_path, confidence=int(MIN_CONFIDENCE), overlap=30).json().get("predictions", [])
                    for p in preds:
                        conf = p.get("confidence", 0) * 100
                        cls_name = p.get("class", "")
                        if any(kw in cls_name.lower() for kw in INVALID_KEYWORDS):
                            continue

                        all_detections.append({
                            "model": model_name_full,
                            "class_name": cls_name,
                            "confidence": round(float(conf), 2),
                            "bbox": [float(p["x"]), float(p["y"]), float(p["width"]), float(p["height"])]
                        })
                except Exception as e:
                    logger.debug(f"Model {model_name_full} evaluation skipped: {e}")
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    # Sort detections by confidence descending
    all_detections.sort(key=lambda d: d["confidence"], reverse=True)

    if all_detections:
        top = all_detections[0]
        cls_name = top["class_name"]
        conf = top["confidence"]
        best_model = top["model"]
        detected_crop = best_model.split()[0]

        if any(k in cls_name.lower() for k in PEST_KWS):
            category = "Pest"
        elif any(k in cls_name.lower() for k in DISEASE_KWS):
            category = "Disease"
        else:
            category = "Condition"

        annotated_b64 = annotate_image(image_bytes, all_detections[:5])

        suggested_actions = [
            f"Isolate affected {detected_crop} plants to prevent further spread.",
            f"Confirm symptoms of {cls_name} with an agronomist or AI Assistant.",
            "Avoid overhead sprinkler irrigation to reduce foliar moisture.",
        ]

        return {
            "status": "success",
            "crop": detected_crop,
            "condition": cls_name,
            "category": category,
            "confidence": round(conf / 100.0, 3),
            "best_model": best_model,
            "total_detections": len(all_detections),
            "all_detections": all_detections[:10],
            "annotated_image_base64": annotated_b64,
            "suggested_actions": suggested_actions,
        }
    else:
        # Honest reporting when no detections occur or when computer vision client is offline
        detected_crop = target_crop if target_crop else "Scanned Crop Sample"
        if rf is None:
            return {
                "status": "service_unconfigured",
                "crop": detected_crop,
                "condition": "Vision YOLO models unconfigured (ROBOFLOW_API_KEY required)",
                "category": "Condition",
                "confidence": 0.0,
                "best_model": "None (Cloud YOLO offline)",
                "total_detections": 0,
                "all_detections": [],
                "annotated_image_base64": None,
                "suggested_actions": [
                    "To enable the 13 YOLO disease & pest models, configure ROBOFLOW_API_KEY in the environment.",
                    "Visually inspect leaves for discoloration, wilting, or chewing damage.",
                    "Consult your nearest Krishi Vigyan Kendra (KVK) or extension officer with field samples."
                ],
            }
        else:
            return {
                "status": "no_detections",
                "crop": detected_crop,
                "condition": "No disease or pest symptoms detected above threshold (40%)",
                "category": "Healthy",
                "confidence": 0.0,
                "best_model": "Roboflow 13-Model Agricultural YOLO Ensemble",
                "total_detections": 0,
                "all_detections": [],
                "annotated_image_base64": None,
                "suggested_actions": [
                    "No foliar symptoms or insect pests were identified above the 40% confidence threshold.",
                    "Visual scanning alone cannot rule out root-zone pathogens, systemic viruses, or latent infections.",
                    "Continue regular field scouting and maintain balanced nutrition and irrigation scheduling."
                ],
            }
