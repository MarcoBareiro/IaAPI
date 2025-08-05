from fastapi import APIRouter
from app.models.schemas import PreguntaRequest
from app.services.llm_orchestrator import procesar_pregunta

router = APIRouter()

@router.post("/query")
async def query(request: PreguntaRequest):
    return await procesar_pregunta(request.pregunta)