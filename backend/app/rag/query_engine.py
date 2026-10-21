"""
query_engine.py — Context-Aware Agricultural RAG Synthesis Engine
=================================================================
Phase 5: Full-context LLM synthesis with structured prompts,
conversation memory, and improved template fallback.

Pipeline:
    1. Retrieve relevant docs via hybrid vector store
    2. Re-rank and filter low-relevance results
    3. Synthesize answer via LLM (with full context, not truncated)
    4. Fall back to high-quality template synthesis if no LLM
    5. Generate context-aware follow-up suggestions
"""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

from app.config import settings
from app.rag.vector_store import vector_store

logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────
# LLM Pipeline (lazy-loaded)
# ────────────────────────────────────────────────────────────
_hf_pipeline = None
_hf_attempted = False


def get_hf_llm():
    """Lazy-load a local HuggingFace LLM pipeline for text generation."""
    global _hf_pipeline, _hf_attempted
    if _hf_pipeline is not None or _hf_attempted:
        return _hf_pipeline
    _hf_attempted = True
    try:
        from transformers import pipeline
        logger.info(f"Loading local LLM pipeline: {settings.LOCAL_LLM_MODEL}...")
        _hf_pipeline = pipeline(
            "text2text-generation",
            model=settings.LOCAL_LLM_MODEL,
            max_length=512,
            do_sample=False,
        )
        logger.info("Local LLM pipeline ready.")
    except Exception as e:
        logger.info(
            f"Local HuggingFace model not active ({e}); "
            "using structured template synthesizer."
        )
        _hf_pipeline = None
    return _hf_pipeline


# ────────────────────────────────────────────────────────────
# Structured LLM Prompt Template
# ────────────────────────────────────────────────────────────
LLM_PROMPT_TEMPLATE = """You are an expert agricultural scientist and certified agronomist.
Answer the farmer's question using ONLY the provided context documents.
Be specific about dosages, timings, and scientific names.
If the context doesn't contain enough information, say so clearly.

### Context Documents:
{context}

### Conversation History:
{history}

### Farmer's Question:
{question}

### Expert Agricultural Advisory:"""


def _build_llm_prompt(
    question: str,
    context_chunks: List[str],
    conversation_history: Optional[List[Dict[str, str]]] = None,
) -> str:
    """Build a structured prompt for the LLM with full context."""
    # Include all context, not truncated
    context_text = "\n\n---\n\n".join(
        f"[Source {i+1}]: {chunk}" for i, chunk in enumerate(context_chunks)
    )

    # Include last 3 conversation turns if available
    history_text = "None (first question)"
    if conversation_history:
        recent = conversation_history[-3:]
        history_lines = []
        for turn in recent:
            role = turn.get("role", "user").capitalize()
            content = turn.get("content", "")[:200]
            history_lines.append(f"{role}: {content}")
        history_text = "\n".join(history_lines)

    return LLM_PROMPT_TEMPLATE.format(
        context=context_text,
        history=history_text,
        question=question,
    )


# ────────────────────────────────────────────────────────────
# Phase 5: Improved Template-Based Synthesis (no-LLM fallback)
# ────────────────────────────────────────────────────────────
def _extract_management_steps(content: str) -> List[str]:
    """Extract numbered management steps from knowledge base content."""
    steps = []

    # Pattern: (1) ... (2) ... (3) ...
    pattern = r"\((\d+)\)\s*([^(]+?)(?=\(\d+\)|$)"
    matches = re.findall(pattern, content)
    if matches:
        for num, step_text in matches:
            clean = step_text.strip().rstrip(". ")
            if clean and len(clean) > 10:
                steps.append(clean)

    # Fallback: look for bullet points or numbered lists
    if not steps:
        for line in content.split("\n"):
            line = line.strip()
            if re.match(r"^[\d•\-\*]+[.)\s]", line):
                clean = re.sub(r"^[\d•\-\*]+[.)\s]+", "", line).strip()
                if clean and len(clean) > 10:
                    steps.append(clean)

    return steps


TELUGU_CROP_MAP = {
    "rice": "వరి (Paddy)",
    "paddy": "వరి (Paddy)",
    "maize": "మొక్కజొన్న (Maize)",
    "cotton": "ప్రత్తి (Cotton)",
    "banana": "అరటి (Banana)",
    "mango": "మామిడి (Mango)",
    "grapes": "ద్రాక్ష (Grapes)",
    "orange": "బత్తాయి / నారింజ (Sweet Orange)",
    "papaya": "బొప్పాయి (Papaya)",
    "pomegranate": "దానిమ్మ (Pomegranate)",
    "watermelon": "పుచ్చకాయ (Watermelon)",
    "muskmelon": "ఖర్బూజ (Muskmelon)",
    "blackgram": "మినుము (Black Gram)",
    "chickpea": "శనగ (Chickpea)",
    "pigeonpeas": "కందులు (Red Gram)",
    "groundnut": "వేరుశనగ (Groundnut)",
    "chilli": "మిరప (Chilli)",
}

TELUGU_COND_MAP = {
    "blast": "అగ్గితెగులు (Rice Blast)",
    "brown plant hopper": "సుడిదోమ (Brown Plant Hopper)",
    "black sigatoka": "సిగటోకా ఆకుమచ్చ తెగులు (Sigatoka)",
    "fall armyworm": "కత్తెర పురుగు (Fall Armyworm)",
    "turcicum leaf blight": "ఆకు ఎండు తెగులు (Turcicum Blight)",
    "citrus canker": "నిమ్మ గజ్జి తెగులు (Citrus Canker)",
    "mango hopper": "తేనెమంచు పురుగు (Mango Hopper)",
    "anthracnose": "కొమ్మ ఎండు తెగులు / మచ్చ తెగులు (Anthracnose)",
    "pink bollworm": "గులాబీ రంగు కాయ తొలుచు పురుగు (Pink Bollworm)",
    "bacterial blight": "బ్యాక్టీరియల్ ఆకు ఎండు తెగులు (Bacterial Blight)",
    "downy mildew": "డౌనీ మిల్డో తెగులు (Downy Mildew)",
    "powdery mildew": "బూడిద తెగులు (Powdery Mildew)",
    "nutrient deficiency": "పోషక లోపం (Nutrient Deficiency)",
}


def _is_telugu(text: str, language: Optional[str] = None) -> bool:
    if language and language.lower().startswith("te"):
        return True
    return bool(re.search(r"[\u0C00-\u0C7F]", text))


def _synthesize_template_response(
    question: str,
    retrieved: List[Dict[str, Any]],
    crop: Optional[str] = None,
    condition: Optional[str] = None,
    language: Optional[str] = "en",
    location: Optional[str] = None,
    growth_stage: Optional[str] = None,
) -> str:
    """
    Generate a high-quality agronomist response using retrieved documents
    without requiring an LLM, supporting both Telugu and English.
    """
    is_te = _is_telugu(question, language)
    top_doc = retrieved[0] if retrieved else None
    raw_crop = crop or (top_doc.get("crop", "Field Crop") if top_doc else "Field Crop")
    raw_cond = condition or (top_doc.get("condition", "Crop Health") if top_doc else "Crop Health")

    target_crop = TELUGU_CROP_MAP.get(raw_crop.lower(), raw_crop) if is_te else raw_crop
    target_cond = TELUGU_COND_MAP.get(raw_cond.lower(), raw_cond) if is_te else raw_cond

    # Check for missing critical context on dosage/spray queries
    is_spray_query = any(w in question.lower() for w in ["spray", "dose", "chemical", "pesticide", "fertilizer quantity", "kg/ha", "మందు", "పిచికారీ", "మోతాదు"])
    missing_context_notes = []
    if is_spray_query:
        if not crop:
            missing_context_notes.append("పంట పేరు (Crop Type)" if is_te else "Specific Crop Type")
        if not growth_stage:
            missing_context_notes.append("పంట దశ (Growth Stage: vegetative, flowering, or maturity)" if is_te else "Current Crop Growth Stage (e.g. seedling, vegetative, flowering)")
        if not location:
            missing_context_notes.append("జిల్లా / ప్రాంతం (District / Region)" if is_te else "District / Regional Weather Context")

    lines = []
    if is_te:
        lines.append(f"🌾 **రైతు మిత్ర AI వ్యవసాయ సలహాదారు: {target_crop} — {target_cond}**")
        lines.append("")
        lines.append(f"**రైతు ప్రశ్న**: *\"{question.strip()}\"*")
        lines.append("")
        if location or growth_stage:
            lines.append(f"📍 **క్షేత్ర వివరాలు**: ప్రాంతం: {location or 'తెలియజేయలేదు'} | దశ: {growth_stage or 'సాధారణ'}")
            lines.append("")
    else:
        lines.append(f"🌾 **AI Agronomist Advisory: {target_crop} — {target_cond}**")
        lines.append("")
        lines.append(f"**Question**: *\"{question.strip()}\"*")
        lines.append("")
        if location or growth_stage:
            lines.append(f"📍 **Field Context**: Location: {location or 'General'} | Growth Stage: {growth_stage or 'Standard'}")
            lines.append("")

    # If critical information was missing for spray/dosage recommendations, display guidance
    if missing_context_notes:
        if is_te:
            lines.append("⚠️ **అధిక ప్రభావ సలహా హెచ్చరిక (Context Required)**:")
            lines.append(f"రసాయన లేదా ఎరువుల ఖచ్చితమైన మోతాదు కొరకు ఈ కింది వివరాలు అవసరం: {', '.join(missing_context_notes)}.")
            lines.append("కింది సలహాలు ప్రామాణిక విశ్వవిద్యాలయ సిఫార్సుల ఆధారంగా సాధారణ మార్గదర్శకాలకు మాత్రమే.")
            lines.append("")
        else:
            lines.append("⚠️ **High-Impact Advisory Notice (Additional Context Recommended)**:")
            lines.append(f"Accurate pesticide doses and fertilizer rates require: {', '.join(missing_context_notes)}.")
            lines.append("The agronomic protocols below reflect standard ICAR/State Agriculture University baselines.")
            lines.append("")

    # Diagnosis section from top document
    if top_doc:
        content = top_doc.get("content", "")

        has_management = "Management" in content
        if has_management:
            parts = content.split("Management", 1)
            symptoms_text = parts[0].strip()
            management_text = "Management" + parts[1] if len(parts) > 1 else ""
        else:
            symptoms_text = content
            management_text = ""

        if is_te:
            lines.append("### 🔍 వ్యాధి / సమస్య నిర్ధారణ (Diagnosis & Symptoms):")
            lines.append(symptoms_text)
            lines.append("")
        else:
            lines.append("### 🔍 Diagnosis & Key Symptoms:")
            lines.append(symptoms_text)
            lines.append("")

        # Extract and format management steps
        if management_text:
            steps = _extract_management_steps(management_text)
            if steps:
                if is_te:
                    lines.append("### 🛡️ సిఫార్సు చేసిన సమగ్ర యాజమాన్య పద్ధతులు (Management Protocols):")
                else:
                    lines.append("### 🛡️ Recommended Integrated Management Protocol:")

                for i, step in enumerate(steps, 1):
                    step_lower = step.lower()
                    if any(kw in step_lower for kw in ["cultural", "prune", "spacing", "rotation", "sanitation", "drain"]):
                        icon = "🌱"
                        label = "సాగు పద్ధతులు (Cultural)" if is_te else "Cultural"
                    elif any(kw in step_lower for kw in ["spray", "fungicide", "insecticide", "chemical", "apply"]):
                        icon = "💊"
                        label = "రసాయన నివారణ (Chemical)" if is_te else "Chemical"
                    elif any(kw in step_lower for kw in ["bio", "tricho", "bacillus", "release", "trap", "pheromone"]):
                        icon = "🦠"
                        label = "జీవ నియంత్రణ (Biological)" if is_te else "Biological"
                    elif any(kw in step_lower for kw in ["seed treatment", "treat"]):
                        icon = "🌰"
                        label = "విత్తన శుద్ధి (Seed Treatment)" if is_te else "Seed Treatment"
                    elif any(kw in step_lower for kw in ["nutrient", "fertili", "potassium", "nitrogen", "zinc"]):
                        icon = "🧪"
                        label = "పోషక యాజమాన్యం (Nutritional)" if is_te else "Nutritional"
                    else:
                        icon = "📋"
                        label = "చర్య (Action)" if is_te else "Action"
                    lines.append(f"  {i}. {icon} **{label}**: {step}")
                lines.append("")

    # Supplementary Agricultural Insights
    if len(retrieved) > 1:
        if is_te:
            lines.append("### 💡 అదనపు పరిశోధనా ఆధారాలు (Supporting Evidence):")
        else:
            lines.append("### 💡 Supplementary Agricultural Insights:")

        for doc in retrieved[1:3]:
            doc_title = doc.get("title", "Guide")
            doc_content = doc.get("content", "")[:300]
            lines.append(f"- **{doc_title}**: {doc_content}...")
        lines.append("")

    # Safety guidelines
    if is_te:
        lines.extend([
            "### ⚠️ పురుగుమందుల వాడకం భద్రతా సూత్రాలు (Safety Guidelines):",
            "- ఎండ తీవ్రత తక్కువగా ఉన్న ఉదయం (6:00–9:00 AM) లేదా సాయంత్రం (4:00–6:00 PM) వేళల్లో మాత్రమే పిచికారీ చేయాలి.",
            "- పురుగుమందులు పిచికారీ చేసేటప్పుడు తప్పనిసరిగా చేతి తొడుగులు, మాస్క్, రక్షణ దుస్తులు ధరించాలి.",
            "- పంట కోతకు ముందు మందుల ప్రభావాన్ని పరిగణించే 'ప్రీ-హార్వెస్ట్ ఇంటర్వెల్ (PHI)' తప్పక పాటించాలి.",
            "- పిచికారీ పరికరాలను ఉపయోగించిన వెంటనే శుభ్రమైన నీటితో కడగాలి.",
            "- సందేహాలు ఉంటే సమీప కృషి విజ్ఞాన కేంద్రం (KVK) లేదా వ్యవసాయ విస్తరణ అధికారి (AEO) సలహా పొందండి.",
        ])
    else:
        lines.extend([
            "### ⚠️ Application Safety Guidelines:",
            "- Apply chemical sprays during **early morning (6:00–9:00 AM)** or "
            "**late afternoon (4:00–6:00 PM)** to minimize pollinator exposure and UV degradation.",
            "- Wear recommended PPE: gloves, mask, full-sleeve protective clothing.",
            "- Observe the **Pre-Harvest Interval (PHI)** specified on the product label.",
            "- Maintain sprayer hygiene: flush equipment with clean water after each use.",
            "- Confirm uncertain diagnoses with your local Krishi Vigyan Kendra (KVK) or Agriculture Officer.",
        ])

    # Fallback if no documents matched
    if not top_doc:
        if is_te:
            lines = [
                f"🌾 **రైతు మిత్ర AI వ్యవసాయ సలహాదారు: {target_crop}**",
                "",
                f"**రైతు ప్రశ్న**: *\"{question.strip()}\"*",
                "",
                "### 🔍 ప్రాథమిక శాస్త్రీయ సూచనలు:",
                "ఆచార్య ఎన్.జి. రంగా / ప్రొఫెసర్ జయశంకర్ తెలంగాణ వ్యవసాయ విశ్వవిద్యాలయాల ప్రామాణిక సిఫార్సుల ప్రకారం:",
                "- నేల ఆరోగ్య కార్డు సూచనల ఆధారంగా సమతుల్య **N-P-K** ఎరువులను మాత్రమే వాడండి.",
                "- పొలంలో నీరు నిల్వ ఉండకుండా మురుగు నీటి కాలువలు ఏర్పాటు చేసుకోండి.",
                "- ప్రతి వారం పంటను పరిశీలించి ప్రారంభ దశలోనే పురుగులు లేదా తెగుళ్లను గుర్తించండి.",
                "- వివరణాత్మక సిఫార్సుల కోసం సమీప మండల వ్యవసాయ అధికారి లేదా కేవీకే (KVK) ను సంప్రదించండి.",
            ]
        else:
            lines = [
                f"🌾 **AI Agronomist Advisory: {target_crop}**",
                "",
                f"**Question**: *\"{question.strip()}\"*",
                "",
                "### 🔍 General Recommendations:",
                "Based on standard ICAR/SAU protocols for the queried crop:",
                "- Maintain balanced **N-P-K** soil fertility through periodic soil testing.",
                "- Ensure well-drained fields and appropriate irrigation scheduling.",
                "- Scout fields weekly for early symptoms of foliar lesions, sucking pests, or nutrient deficiency.",
                "- Consult your nearest **Krishi Vigyan Kendra (KVK)** or district agricultural extension officer for localized advisory.",
            ]

    return "\n".join(lines)



# ────────────────────────────────────────────────────────────
# Smart Follow-up Suggestions
# ────────────────────────────────────────────────────────────
def _generate_followups(
    question: str,
    crop: Optional[str],
    condition: Optional[str],
    retrieved: List[Dict[str, Any]],
) -> List[str]:
    """Generate context-aware follow-up questions based on retrieved docs."""
    crop_name = crop or "this crop"
    cond_name = condition or "this condition"

    # Base suggestions
    followups = []

    # Condition-specific follow-ups
    if condition:
        cond_lower = condition.lower()
        if any(kw in cond_lower for kw in ["blast", "blight", "wilt", "mildew", "canker", "rot"]):
            followups.append(f"What resistant varieties of {crop_name} are available against {cond_name}?")
            followups.append(f"What is the economic threshold level for spraying against {cond_name}?")
        elif any(kw in cond_lower for kw in ["armyworm", "hopper", "bollworm", "aphid", "borer"]):
            followups.append(f"What biological control agents are effective against {cond_name}?")
            followups.append(f"What is the pheromone trap protocol for monitoring {cond_name}?")
        elif any(kw in cond_lower for kw in ["nitrogen", "phosphorus", "potassium", "deficiency", "zinc"]):
            followups.append(f"What is the recommended soil testing schedule for {crop_name}?")
            followups.append(f"Can foliar spray correct {cond_name} faster than soil application?")

    # General follow-ups
    followups.extend([
        f"What is the recommended fertilizer schedule for {crop_name}?",
        f"How much irrigation water does {crop_name} need at the current growth stage?",
        f"What is the market price forecast for {crop_name} in our district?",
    ])

    # Deduplicate and limit
    seen = set()
    unique = []
    for fq in followups:
        key = fq.lower()
        if key not in seen:
            seen.add(key)
            unique.append(fq)
    return unique[:4]


# ────────────────────────────────────────────────────────────
# Main RAG Query Interface
# ────────────────────────────────────────────────────────────
def query_rag(
    farmer_question: str,
    crop: Optional[str] = None,
    condition: Optional[str] = None,
    k: int = 3,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    language: Optional[str] = "en",
    location: Optional[str] = None,
    growth_stage: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute the full RAG pipeline:
    1. Retrieve relevant agricultural documents (hybrid search)
    2. Filter low-relevance results
    3. Synthesize expert agronomist response (LLM or template) in requested language (English / Telugu)
    4. Generate context-aware follow-up suggestions

    Args:
        farmer_question: The farmer's question in natural language.
        crop: Optional crop filter (e.g., "Rice", "Banana").
        condition: Optional condition filter (e.g., "Blast", "Sigatoka").
        k: Number of documents to retrieve.
        conversation_history: Optional list of previous conversation turns
            for multi-turn context awareness.
        language: "en" or "te" (Telugu).
        location: District or region for localized advisory.
        growth_stage: Current crop growth stage.

    Returns:
        Dict with response, sources, follow-ups, and retrieval metadata.
    """
    # 1. Retrieve top matching knowledge chunks
    retrieved = vector_store.similarity_search(
        query=farmer_question,
        k=k,
        crop_filter=crop,
        condition_filter=condition,
    )

    # Format sources
    sources = [
        f"{doc.get('title', 'Guide')}: {doc.get('source', 'Agricultural Extension')}"
        for doc in retrieved
    ]

    # Combine context chunks
    context_chunks = [doc.get("content", "") for doc in retrieved if doc.get("content")]

    # 2. Try LLM synthesis with full context (Phase 5)
    response_text = None
    llm = get_hf_llm()

    if llm and context_chunks:
        try:
            prompt = _build_llm_prompt(
                question=farmer_question,
                context_chunks=context_chunks,
                conversation_history=conversation_history,
            )
            # Use full context, not truncated
            generated = llm(prompt[:2048])[0]["generated_text"]
            if generated and len(generated.strip()) > 20:
                response_text = (
                    f"🌾 **AI Agronomist Advisory**\n\n"
                    f"{generated.strip()}\n\n"
                    f"---\n"
                    f"*Based on {len(retrieved)} verified agricultural sources.*"
                )
        except Exception as e:
            logger.warning(f"LLM inference error: {e}")
            response_text = None

    # 3. Template-based synthesis fallback (Phase 5 — improved)
    if not response_text:
        response_text = _synthesize_template_response(
            question=farmer_question,
            retrieved=retrieved,
            crop=crop,
            condition=condition,
            language=language,
            location=location,
            growth_stage=growth_stage,
        )

    # 4. Generate smart follow-up suggestions
    suggested_followups = _generate_followups(
        question=farmer_question,
        crop=crop,
        condition=condition,
        retrieved=retrieved,
    )

    return {
        "response": response_text,
        "sources": sources,
        "suggested_followups": suggested_followups,
        "retrieved_docs": retrieved,
        "retrieval_method": retrieved[0].get("retrieval_method", "unknown") if retrieved else "none",
        "documents_searched": vector_store.document_count,
    }
