"""
agriculture_agent.py — LangGraph Multi-Modal Agriculture Agent
================================================================
Enhanced with:
- Robust regex-based action extraction (not fragile string splitting)
- Severity scoring with weighted heuristics
- Full integration with improved RAG pipeline
- Structured diagnostic report formatting
"""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional, TypedDict

from app.rag.vector_store import vector_store

logger = logging.getLogger(__name__)


class AgricultureState(TypedDict):
    image_result: Dict[str, Any]
    farmer_question: str
    crop: str
    condition: str
    category: str
    confidence: float
    urgency_level: str
    retrieved_sources: List[str]
    action_plan: List[str]
    final_answer: str


# ────────────────────────────────────────────────────────────
# Urgency Classification
# ────────────────────────────────────────────────────────────
HIGH_URGENCY_KEYWORDS = [
    "blast", "sigatoka", "fall armyworm", "bacterial blight", "wilt",
    "bollworm", "borer", "late blight", "brown plant hopper", "telya",
]
MODERATE_URGENCY_KEYWORDS = [
    "pest", "hopper", "mildew", "spot", "canker", "anthracnose",
    "thrips", "aphid", "whitefly", "rust", "mosaic", "rot",
]


def _classify_urgency(condition: str, confidence: float) -> str:
    """Classify urgency based on condition severity and detection confidence."""
    lower_cond = condition.lower()

    if any(kw in lower_cond for kw in HIGH_URGENCY_KEYWORDS):
        base = "High"
    elif any(kw in lower_cond for kw in MODERATE_URGENCY_KEYWORDS):
        base = "Moderate"
    else:
        base = "Low"

    # Escalate if confidence is very high
    if confidence >= 0.90 and base == "Moderate":
        base = "High"

    return base


# ────────────────────────────────────────────────────────────
# Robust Action Extraction
# ────────────────────────────────────────────────────────────
def _extract_actions_from_content(content: str, max_actions: int = 5) -> List[str]:
    """
    Extract numbered management steps using regex instead of
    fragile string splitting.
    """
    actions = []

    # Pattern 1: (1) step text (2) step text ...
    numbered = re.findall(r"\((\d+)\)\s*(.+?)(?=\(\d+\)|$)", content, re.DOTALL)
    if numbered:
        for _num, step_text in numbered[:max_actions]:
            clean = step_text.strip().rstrip(". ")
            if clean and len(clean) > 15:
                actions.append(clean[:250])

    # Pattern 2: Management: or Control: followed by text
    if not actions:
        mgmt_match = re.search(
            r"(?:Management|Control|Treatment|Remedy)[:\s]+(.+)",
            content,
            re.IGNORECASE | re.DOTALL,
        )
        if mgmt_match:
            mgmt_text = mgmt_match.group(1)
            # Split on sentence boundaries
            sentences = re.split(r"(?<=[.!])\s+", mgmt_text)
            for sent in sentences[:max_actions]:
                sent = sent.strip()
                if sent and len(sent) > 15:
                    actions.append(sent[:250])

    return actions


# ────────────────────────────────────────────────────────────
# Agent Nodes
# ────────────────────────────────────────────────────────────
def analyze_detection_node(state: AgricultureState) -> Dict[str, Any]:
    """Node 1: Parse and classify disease/pest detection severity."""
    res = state.get("image_result", {})
    crop = str(res.get("crop", "Unknown Crop"))
    condition = str(res.get("condition", "General Condition"))
    category = str(res.get("category", "Disease"))
    conf = float(res.get("confidence", 0.75))
    urgency = _classify_urgency(condition, conf)

    return {
        "crop": crop,
        "condition": condition,
        "category": category,
        "confidence": conf,
        "urgency_level": urgency,
    }


def rag_retrieval_node(state: AgricultureState) -> Dict[str, Any]:
    """Node 2: Retrieve verified scientific agronomic protocols."""
    crop = state.get("crop", "")
    condition = state.get("condition", "")
    question = state.get("farmer_question", "")

    query = f"{crop} {condition} {question} control treatment symptoms management"
    docs = vector_store.similarity_search(
        query, k=4, crop_filter=crop, condition_filter=condition
    )

    sources = [
        f"{d.get('title', 'Guide')}: {d.get('source', 'Agricultural Extension')}"
        for d in docs
    ]

    # Extract action steps using robust regex extraction
    actions = []
    for doc in docs:
        content = doc.get("content", "")
        extracted = _extract_actions_from_content(content)
        actions.extend(extracted)
        if len(actions) >= 5:
            break

    # Deduplicate actions
    seen = set()
    unique_actions = []
    for act in actions:
        key = act[:50].lower()
        if key not in seen:
            seen.add(key)
            unique_actions.append(act)

    if not unique_actions:
        unique_actions = [
            f"Isolate affected plants and scout nearby rows for similar {condition} signs.",
            "Verify soil moisture and ensure field drainage is unobstructed.",
            "Collect leaf/plant samples and submit to nearest Krishi Vigyan Kendra (KVK) for laboratory diagnosis.",
            "Consult local agricultural extension officer for field-specific advisory.",
        ]

    return {
        "retrieved_sources": sources,
        "action_plan": unique_actions[:5],
    }


def synthesis_node(state: AgricultureState) -> Dict[str, Any]:
    """Node 3: Formulate final comprehensive agronomist diagnostic report."""
    crop = state.get("crop", "Crop")
    condition = state.get("condition", "Condition")
    category = state.get("category", "Disease")
    confidence = state.get("confidence", 0.0)
    urgency = state.get("urgency_level", "Moderate")
    sources = state.get("retrieved_sources", [])
    actions = state.get("action_plan", [])
    question = state.get("farmer_question", "")

    # Urgency-specific styling
    urgency_icon = {"High": "🔴", "Moderate": "🟡", "Low": "🟢"}.get(urgency, "⚪")

    report_lines = [
        f"🌾 **AGRIPREDICT AI AGENT DIAGNOSTIC REPORT**",
        "=" * 50,
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| **Crop** | {crop} |",
        f"| **Identified Issue** | {condition} |",
        f"| **Category** | {category} |",
        f"| **Detection Confidence** | {confidence:.1%} |",
        f"| **Urgency** | {urgency_icon} {urgency.upper()} |",
        "",
        f"**Farmer's Inquiry**: *\"{question.strip()}\"*",
        "",
        "### 🚨 Priority Action Plan:",
    ]

    for idx, act in enumerate(actions, 1):
        report_lines.append(f"  {idx}. {act}")

    report_lines.extend([
        "",
        "### 🛡️ Integrated Crop Management (ICM) Recommendations:",
        f"- Maintain balanced soil nutrition; avoid excessive nitrogen which can aggravate {condition.lower()}.",
        "- Disinfect pruning tools with 2% sodium hypochlorite between rows to prevent pathogen spread.",
        "- Follow integrated pest & disease management (IPM/IDM) guidelines to preserve beneficial predators.",
        "- Monitor weather forecasts — high humidity and temperature favor disease outbreaks.",
        "",
        "### 📚 Knowledge Sources:",
    ])

    for src in sources[:4]:
        report_lines.append(f"  - {src}")

    return {"final_answer": "\n".join(report_lines)}


# ────────────────────────────────────────────────────────────
# LangGraph Agent Compilation
# ────────────────────────────────────────────────────────────
_compiled_agent = None


def get_agriculture_agent():
    """Compile LangGraph agent workflow (cached)."""
    global _compiled_agent
    if _compiled_agent is not None:
        return _compiled_agent

    try:
        from langgraph.graph import END, StateGraph

        workflow = StateGraph(AgricultureState)
        workflow.add_node("analyze_detection", analyze_detection_node)
        workflow.add_node("retrieve_rag", rag_retrieval_node)
        workflow.add_node("synthesize_report", synthesis_node)

        workflow.set_entry_point("analyze_detection")
        workflow.add_edge("analyze_detection", "retrieve_rag")
        workflow.add_edge("retrieve_rag", "synthesize_report")
        workflow.add_edge("synthesize_report", END)

        _compiled_agent = workflow.compile()
        logger.info("Compiled LangGraph Agriculture Agent successfully.")
        return _compiled_agent
    except Exception as e:
        logger.error(
            f"Failed to compile LangGraph agent ({e}); fallback runner will be used."
        )
        return None


def run_agriculture_agent(
    image_result: Dict[str, Any],
    farmer_question: str,
) -> Dict[str, Any]:
    """Execute the multi-modal agent on detection outcome + farmer question."""
    agent = get_agriculture_agent()

    initial_state: AgricultureState = {
        "image_result": image_result,
        "farmer_question": farmer_question,
        "crop": "",
        "condition": "",
        "category": "",
        "confidence": 0.0,
        "urgency_level": "Moderate",
        "retrieved_sources": [],
        "action_plan": [],
        "final_answer": "",
    }

    if agent:
        try:
            result = agent.invoke(initial_state)
            return {
                "status": "success",
                "crop": result["crop"],
                "condition": result["condition"],
                "category": result["category"],
                "confidence": result["confidence"],
                "urgency_level": result["urgency_level"],
                "final_answer": result["final_answer"],
                "sources": result["retrieved_sources"],
                "action_plan": result["action_plan"],
            }
        except Exception as e:
            logger.warning(f"LangGraph execution exception: {e}; using direct pipeline.")

    # Direct sequential fallback
    s1 = analyze_detection_node(initial_state)
    initial_state.update(s1)
    s2 = rag_retrieval_node(initial_state)
    initial_state.update(s2)
    s3 = synthesis_node(initial_state)
    initial_state.update(s3)

    return {
        "status": "success",
        "crop": initial_state["crop"],
        "condition": initial_state["condition"],
        "category": initial_state["category"],
        "confidence": initial_state["confidence"],
        "urgency_level": initial_state["urgency_level"],
        "final_answer": initial_state["final_answer"],
        "sources": initial_state["retrieved_sources"],
        "action_plan": initial_state["action_plan"],
    }
