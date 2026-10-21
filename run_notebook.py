"""
AgriFusion AI — Local Execution Script
========================================
Converted from Gen_AI_Intern_Integrated.ipynb (Google Colab)
to run locally on Windows with hardcoded paths and API key.

Usage:
    python run_notebook.py
"""

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import os
import sys
import glob
import io

# Fix Windows console encoding for emoji/unicode characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ============================================================
# CELL 1: Configuration — API Keys & Paths
# ============================================================
print("=" * 60)
print("🌾 AgriFusion AI — Local Execution")
print("=" * 60)

# Roboflow API Key
os.environ["ROBOFLOW_API_KEY"] = "piCQRV6hQpQMRRREQWpi"
# OpenAI API Key (not used — notebook uses free local HuggingFace model)
os.environ["OPENAI_API_KEY"] = "sk-placeholder-not-used"

# Local file paths
IMAGE_PATH = r"H:\My Drive\chatgpt notes\images.jpg"
PDF_DIR = r"H:\My Drive\DL intenship project datasets\disease pdfs"

print("✅ API keys loaded")
print(f"📷 Image path: {IMAGE_PATH}")
print(f"📄 PDF directory: {PDF_DIR}")

# Verify files exist
if not os.path.isfile(IMAGE_PATH):
    print(f"⚠️ WARNING: Image not found at {IMAGE_PATH}")
else:
    print(f"✅ Image file found ({os.path.getsize(IMAGE_PATH)} bytes)")

pdf_files_list = glob.glob(os.path.join(PDF_DIR, "*.pdf"))
if not pdf_files_list:
    print(f"⚠️ WARNING: No PDF files found in {PDF_DIR}")
else:
    print(f"✅ Found {len(pdf_files_list)} PDF files:")
    for p in pdf_files_list:
        print(f"   - {os.path.basename(p)}")

# ============================================================
# CELL 2: Import Libraries
# ============================================================
print("\n" + "=" * 60)
print("📦 Importing libraries...")
print("=" * 60)

import cv2
import numpy as np
try:
    import langchain
except ImportError:
    import langchain_classic as langchain
import langchain_core
import langgraph
import importlib.metadata
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for local execution
import matplotlib.pyplot as plt

print("OpenCV :", cv2.__version__)
print("NumPy  :", np.__version__)
print("LangChain :", langchain.__version__)
print("LangChain Core :", langchain_core.__version__)

try:
    print("LangGraph :", importlib.metadata.version("langgraph"))
except importlib.metadata.PackageNotFoundError:
    print("LangGraph : Not found")

print("\n✅ Environment ready")

# ============================================================
# CELL 3: Connect to Roboflow
# ============================================================
print("\n" + "=" * 60)
print("🔗 Connecting to Roboflow...")
print("=" * 60)

from roboflow import Roboflow

rf = Roboflow(
    api_key=os.environ["ROBOFLOW_API_KEY"]
)

print("✅ Roboflow connected")

# ============================================================
# CELL 4: Roboflow Model Links
# ============================================================
roboflow_links = [
    {"crop": "Orange", "category": "Disease",
     "workspace": "citrus-leaf-disease",
     "project": "citrus-leaves-diseases-ykhpu"},

    {"crop": "Mango", "category": "Disease",
     "workspace": "mango-leaf-disease",
     "project": "mango-leaf-disease-kguxz"},

    {"crop": "Mango", "category": "Pest",
     "workspace": "project-pjsi8",
     "project": "mango-pests"},

    {"crop": "Watermelon", "category": "Disease",
     "workspace": "watermelon-diseases",
     "project": "watermelon-diseases"},

    {"crop": "Banana", "category": "Disease",
     "workspace": "tdtu-ocamc",
     "project": "banana-diseases-lrf9y"},

    {"crop": "Maize", "category": "Disease",
     "workspace": "detection-of-corn-crop-diseases-using-yolov8",
     "project": "maize-disease-dataset"},

    {"crop": "Maize", "category": "Pest",
     "workspace": "mo-qmyfx",
     "project": "maize-eloeo"},

    {"crop": "Beans", "category": "Disease",
     "workspace": "zhang-wen-hao-itjzq",
     "project": "beans-diseases"},

    {"crop": "Grapes", "category": "Disease",
     "workspace": "poramet-thongvichit",
     "project": "grape-leaf-disease-kf5ll"},

    {"crop": "Rice", "category": "Disease",
     "workspace": "riceleafdiseasedetection",
     "project": "rice-leaf-disease-s1asn"},

    {"crop": "Rice", "category": "Pest",
     "workspace": "rice-pest",
     "project": "rice-i9qwz"},

    {"crop": "Pomegranate", "category": "Disease + Pest",
     "workspace": "krish-verma-fayi1",
     "project": "pomegranate-disease-detection-29ocz"},

    {"crop": "Multiple Crops", "category": "Pest",
     "workspace": "yolo-dv5qa",
     "project": "pest-uruhn-yfh5t"}
]

print("Number of models:", len(roboflow_links))

# ============================================================
# CELL 5: OpenCV Detection Pipeline (adapted for local)
# ============================================================
print("\n" + "=" * 60)
print("🖼️  Running image detection pipeline...")
print("=" * 60)

# Configuration & Helpers
MIN_CONFIDENCE = 50.0
INVALID_KEYWORDS = ["this dataset was exported", "roboflow.com", "exported via"]
DISEASE_KWS = ["disease", "spot", "blight", "mildew", "rust", "virus", "rot", "scab"]
PEST_KWS = ["pest", "insect", "worm", "bug", "aphid"]


def get_detection_color(cls_name):
    cls_lower = str(cls_name).lower()
    if any(w in cls_lower for w in DISEASE_KWS): return (255, 0, 0)
    if any(w in cls_lower for w in PEST_KWS): return (255, 128, 0)
    return (0, 200, 0)


# Use the hardcoded image path directly (no google.colab upload)
filename = IMAGE_PATH
ext = os.path.splitext(filename)[1].lower()

is_video = ext in ['.mp4', '.avi', '.mov', '.mkv']
is_image = ext in ['.jpg', '.jpeg', '.png', '.bmp']

if not is_video and not is_image:
    raise ValueError(f"❌ Unsupported file format '{ext}'. Please upload an image or video.")

print(f"\n✅ Using file: {filename}")
if is_image:
    print("🖼️ File type detected: IMAGE")
else:
    print("🎬 File type detected: VIDEO")


# Multi-Model Image Scanning
def scan_image_all_models(img_path):
    print("\n🔍 Scanning across all agriculture models to find the best match...")
    all_detections = []

    for item in roboflow_links:
        crop, cat = item["crop"], item["category"]
        model_name_full = f"{crop} {cat}"
        print(f"   Analyzing: {model_name_full}...")
        try:
            project = rf.workspace(item["workspace"]).project(item["project"])

            # Load model safely
            model = next((v.model for v in project.versions() if hasattr(v, "model") and v.model), None)
            if not model:
                model = next((v.models()[0] for v in project.versions() if hasattr(v, "models") and v.models()), None)
            if not model:
                continue

            # Run Inference
            preds = model.predict(img_path, confidence=int(MIN_CONFIDENCE), overlap=30).json().get("predictions", [])

            for p in preds:
                conf = p.get("confidence", 0) * 100
                cls_name = p.get("class", "")
                if any(kw in cls_name.lower() for kw in INVALID_KEYWORDS): continue

                all_detections.append({
                    "Model": model_name_full,
                    "Class": cls_name,
                    "Confidence": conf,
                    "BBox": (p["x"], p["y"], p["width"], p["height"]),
                    "Model_Obj": model
                })
        except Exception as e:
            print(f"      ⚠️ Skipped ({e})")

    return all_detections


# Variable to hold detection results
df = None
best_detection = None
best_model_name = None

# PROCESS IMAGE
if is_image:
    detections = scan_image_all_models(filename)

    if not detections:
        print("\n❌ No valid detections found.")
    else:
        # Sort and show results
        df = pd.DataFrame(detections).sort_values(by="Confidence", ascending=False).reset_index(drop=True)
        df["Conf_Display"] = df["Confidence"].apply(lambda x: f"{x:.1f}%")

        print("\n" + "=" * 60 + "\n🌾 AGRICULTURE AI RESULT (BEST MATCH)\n" + "=" * 60)
        print(df[["Model", "Class", "Conf_Display"]].to_string())

        # Draw on image
        img = cv2.imread(filename)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_h, img_w = img_rgb.shape[:2]

        scale_factor = max(img_h, img_w) / 800.0
        FONT_SCALE = max(0.4, 0.5 * scale_factor)
        TXT_THICK = max(1, int(1.2 * scale_factor))
        BOX_THICK = max(2, int(2.5 * scale_factor))

        # Only draw detections from the top-performing model
        best_model_name = df.iloc[0]["Model"]
        best_detections_list = [d for d in detections if d["Model"] == best_model_name]

        for d in best_detections_list:
            x, y, w, h = d["BBox"]
            cls_name, conf = d["Class"], d["Confidence"]

            x1, y1 = int(x - w / 2), int(y - h / 2)
            x2, y2 = int(x + w / 2), int(y + h / 2)
            color = get_detection_color(cls_name)

            cv2.rectangle(img_rgb, (x1, y1), (x2, y2), color, BOX_THICK)

            label = f"{cls_name} {int(conf)}%"
            (tw, th), bl = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, TXT_THICK)
            txt_y = max(th + 5, y1)
            txt_x = max(0, min(x1, img_w - tw))
            cv2.rectangle(img_rgb, (txt_x, txt_y - th - 5), (txt_x + tw, txt_y + bl - 5), color, cv2.FILLED)
            cv2.putText(img_rgb, label, (txt_x, txt_y - 5), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, (255, 255, 255),
                        TXT_THICK)

        # Save annotated image instead of plt.show()
        output_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "detection_output.png")
        plt.figure(figsize=(12, 12 * (img_h / img_w)))
        plt.imshow(img_rgb)
        plt.axis("off")
        plt.savefig(output_img_path, bbox_inches="tight", dpi=150)
        plt.close()
        print(f"\n📷 Annotated image saved to: {output_img_path}")

# PROCESS VIDEO
elif is_video:
    cap = cv2.VideoCapture(filename)
    ret, frame = cap.read()
    if not ret:
        raise ValueError("❌ Could not read video file.")

    temp_first_frame = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_first_frame.jpg")
    cv2.imwrite(temp_first_frame, frame)

    print("\n🎬 Analyzing the first frame of the video to auto-select the right AI model...")
    detections = scan_image_all_models(temp_first_frame)

    if not detections:
        print("\n❌ No detections found in the first frame. Cannot determine which model to use.")
    else:
        best_detection = max(detections, key=lambda x: x["Confidence"])
        selected_model = best_detection["Model_Obj"]
        best_model_name = best_detection["Model"]

        print(f"\n🌾 Auto-selected best model: {best_model_name} (Confidence: {best_detection['Confidence']:.1f}%)")
        print("\n🚀 Starting full video detection...\n")

        fps = cap.get(cv2.CAP_PROP_FPS)
        width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        output_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agriculture_unified_output.mp4")
        out = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_number = 0
        total_det_count = 0
        FRAME_SKIP = 10

        while True:
            ret, frame = cap.read()
            if not ret: break
            frame_number += 1
            if frame_number % FRAME_SKIP != 0:
                out.write(frame)
                continue

            temp_frame = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_frame_vid.jpg")
            cv2.imwrite(temp_frame, frame)

            try:
                preds = selected_model.predict(temp_frame, confidence=40, overlap=30).json().get("predictions", [])
                for pred in preds:
                    conf, cls_name = pred.get("confidence", 0) * 100, pred.get("class", "unknown")
                    x, y, w, h = pred.get("x", 0), pred.get("y", 0), pred.get("width", 0), pred.get("height", 0)
                    x1, y1 = int(x - w / 2), int(y - h / 2)
                    x2, y2 = int(x + w / 2), int(y + h / 2)
                    color = get_detection_color(cls_name)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    label = f"{cls_name} {conf:.1f}%"
                    cv2.putText(frame, label, (x1, max(y1 - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    total_det_count += 1
            except:
                pass

            out.write(frame)
            if frame_number % 100 == 0:
                print(f"Processed {frame_number}/{total_frames} frames...")

        cap.release()
        out.release()

        print("\n" + "=" * 60 + "\nVIDEO PROCESSING COMPLETED\n" + "=" * 60)
        print(f"Total frames processed: {frame_number}")
        print(f"Total detections found: {total_det_count}")
        print(f"📹 Output saved to: {output_filename}")

# ============================================================
# CELL 6: Integration Bridge — Detection → RAG + GenAI
# ============================================================
print("\n" + "=" * 60)
print("🔗 Building detection_result bridge...")
print("=" * 60)


def build_detection_result():
    try:
        if df is not None and len(df) > 0:
            top = df.iloc[0]
            cls_name = str(top["Class"])
            confidence = float(top["Confidence"]) / 100.0
            model_name = top["Model"] if "Model" in top else cls_name
            crop = str(model_name).split()[0]

            if any(k in cls_name.lower() for k in PEST_KWS):
                category = "Pest"
            elif any(k in cls_name.lower() for k in DISEASE_KWS):
                category = "Disease"
            else:
                category = "Healthy"

            return {
                "crop": crop,
                "condition": cls_name,
                "category": category,
                "confidence": confidence,
            }

        if best_detection is not None:
            cls_name = str(best_detection["Class"])
            confidence = float(best_detection["Confidence"]) / 100.0
            crop = str(best_model_name).split()[0] if best_model_name else cls_name.split()[0]

            if any(k in cls_name.lower() for k in PEST_KWS):
                category = "Pest"
            elif any(k in cls_name.lower() for k in DISEASE_KWS):
                category = "Disease"
            else:
                category = "Healthy"

            return {
                "crop": crop,
                "condition": cls_name,
                "category": category,
                "confidence": confidence,
            }

    except Exception as e:
        print("⚠️ Could not auto-build detection_result from detections:", e)

    return None


detection_result = build_detection_result()

if detection_result is None:
    print("⚠️ No detection output found. Falling back to manual example values.")
    detection_result = {
        "crop": "Banana",
        "condition": "Black Sigatoka",
        "category": "Disease",
        "confidence": 0.83,
    }

print("✅ detection_result created:")
print(detection_result)

# ============================================================
# CELL 7: RAG — Load PDFs from local directory
# ============================================================
print("\n" + "=" * 60)
print("📄 Loading PDF documents for RAG...")
print("=" * 60)

# Collect all PDFs from the local directory
pdf_paths = glob.glob(os.path.join(PDF_DIR, "*.pdf"))
print(f"Found {len(pdf_paths)} PDFs:")
for p in pdf_paths:
    print(f"   - {os.path.basename(p)}")

# ============================================================
# CELL 8: Load and Split PDF Documents
# ============================================================
print("\n" + "=" * 60)
print("✂️  Splitting PDF documents into chunks...")
print("=" * 60)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

all_documents = []

for pdf_path in pdf_paths:
    print("Reading:", os.path.basename(pdf_path))
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    chunks = splitter.split_documents(pages)
    all_documents.extend(chunks)

print("\nTotal chunks:", len(all_documents))

# ============================================================
# CELL 9: Create Embeddings & ChromaDB Vector Store
# ============================================================
print("\n" + "=" * 60)
print("🧠 Creating embeddings and vector store...")
print("=" * 60)

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Use a local persist directory within the project
persist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agriculture_db")

vector_store = Chroma.from_documents(
    documents=all_documents,
    embedding=embeddings,
    persist_directory=persist_dir
)

print("✅ Agriculture RAG database created")

# ============================================================
# CELL 10: RAG Query — Retrieve Relevant Documents
# ============================================================
print("\n" + "=" * 60)
print("🔎 Querying RAG database...")
print("=" * 60)

query = """
What are the symptoms, treatment,
management and prevention of
banana Black Sigatoka?
"""

documents = vector_store.similarity_search(
    query,
    k=4
)

# Display Retrieved Sources
print("Retrieved documents:", len(documents))

for i, doc in enumerate(documents):
    print(f"\n========== SOURCE {i + 1} ==========")
    print(doc.page_content[:1000])

# ============================================================
# CELL 11: Load Free Local LLM (Hugging Face FLAN-T5)
# ============================================================
print("\n" + "=" * 60)
print("🤖 Loading free local LLM (Hugging Face)...")
print("=" * 60)

from transformers import pipeline as hf_pipeline

llm_local = None
try:
    print("⏳ Loading free local LLM (Hugging Face)...")
    llm_local = hf_pipeline("text2text-generation", model="google/flan-t5-base")
    print("✅ Local GenAI Ready")
except Exception as e:
    print("Could not load local model, setting up fallback summary processor.", e)
    llm_local = None

# ============================================================
# CELL 12: agriculture_ai() — Integrate Detection + RAG + GenAI
# ============================================================
print("\n" + "=" * 60)
print("🌾 Defining agriculture_ai pipeline...")
print("=" * 60)


def agriculture_ai(detection_result, farmer_question):
    crop = detection_result.get("crop", "Crop")
    condition = detection_result.get("condition", "Condition")
    category = detection_result.get("category", "Category")
    confidence = detection_result.get("confidence", 0.0)

    # 1. Query local RAG database
    query = f"{crop} {condition} symptoms control prevention"
    documents = vector_store.similarity_search(query, k=3)

    # 2. Extract facts from retrieved documents
    rag_facts = []
    for doc in documents:
        content = doc.page_content.strip()
        if "Sigatoka" in content or "banana" in content.lower():
            rag_facts.append(content)

    context = "\n".join(rag_facts) if rag_facts else "\n".join([d.page_content[:400] for d in documents])

    # 3. Use local free model to formulate response or fallback to direct extraction
    intro = f"🌾 AGRICULTURE AI REPORT\n=======================\n1. Crop: {crop}\n2. Condition: {condition}\n3. Category: {category}\n4. Confidence: {confidence:.1%}\n\n"

    if llm_local:
        prompt = f"Answer the question using the context. Question: {farmer_question}. Context: {context[:800]}"
        try:
            local_answer = llm_local(prompt, max_length=256)[0]['generated_text']
            return intro + "🤖 AI Answer (Local Model):\n" + local_answer + "\n\n📖 Supporting Source Material Found:\n" + context[:600] + "..."
        except Exception as e:
            pass

    # Fallback to precise extraction if model inference fails
    return intro + "📝 Summary of Retrieved Agriculture Information:\n" + context[:1200] + "..."


print("✅ agriculture_ai function defined")

# ============================================================
# CELL 13: NLP — Define Farmer's Question
# ============================================================
farmer_question = """
What are the symptoms of this disease
and how can I control it?
"""

print(f"👨‍🌾 Farmer's question: {farmer_question.strip()}")

# ============================================================
# CELL 14: GENAI — Generate Final Diagnostic Response
# ============================================================
print("\n" + "=" * 60)
print("🤖 Generating AI response...")
print("=" * 60)

answer = agriculture_ai(detection_result, farmer_question)
print(answer)

# ============================================================
# CELL 15: LangGraph Agent — Define & Build
# ============================================================
print("\n" + "=" * 60)
print("🤖 Building LangGraph Agriculture Agent...")
print("=" * 60)

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END


class AgricultureState(TypedDict):
    image_result: dict
    farmer_question: str
    final_answer: str


def agriculture_agent_node(state: AgricultureState):
    result = state["image_result"]
    question = state["farmer_question"]
    answer = agriculture_ai(result, question)
    return {"final_answer": answer}


workflow = StateGraph(AgricultureState)
workflow.add_node("agriculture_ai", agriculture_agent_node)
workflow.set_entry_point("agriculture_ai")
workflow.add_edge("agriculture_ai", END)

agriculture_agent = workflow.compile()
print("✅ Agriculture Agent created")

# ============================================================
# CELL 16: Execute Agriculture AI Agent
# ============================================================
print("\n" + "=" * 60)
print("🚀 Executing Agriculture AI Agent...")
print("=" * 60)

agent_result = agriculture_agent.invoke({
    "image_result": detection_result,
    "farmer_question": """
    What are the symptoms and
    treatment for this problem?
    """
})

print(agent_result["final_answer"])

# ============================================================
# DONE
# ============================================================
print("\n" + "=" * 60)
print("🎉 ALL CELLS EXECUTED SUCCESSFULLY!")
print("=" * 60)
