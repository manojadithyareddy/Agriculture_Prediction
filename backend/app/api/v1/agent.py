from fastapi import APIRouter, HTTPException
from app.schemas.agent import AgentDiagnoseRequest, AgentDiagnoseResponse
from app.agent.agriculture_agent import run_agriculture_agent

router = APIRouter(prefix="/agent", tags=["AI Agronomist Agent"])


@router.post(
    "/diagnose",
    response_model=AgentDiagnoseResponse,
    summary="Multi-modal AI Agent Diagnosis",
    description=(
        "Executes a LangGraph multi-step reasoning agent combining computer vision detection findings, "
        "agricultural scientific RAG knowledge, and urgency severity assessment to generate a tailored "
        "farmer action plan."
    ),
)
def agent_diagnose(req: AgentDiagnoseRequest):
    try:
        res = run_agriculture_agent(
            image_result=req.image_result,
            farmer_question=req.farmer_question
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent reasoning failed: {str(e)}")
