import httpx
import logging
from typing import Dict, Any
from app.core.config import URL_API_BASE

logger = logging.getLogger(__name__)

async def get_objetivo_mensual(mes: str) -> Dict[str, Any]:

    url_service = URL_API_BASE+"/ventas/objetivo_mensual?mes="+mes 

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url_service, timeout=10.0)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Error HTTP: {e.response.status_code} - {e.response.text}")
        return {"error": "Error consultando el servicio de objetivos"}
    except Exception as e:
        logger.exception("Error inesperado")
        return {"error": "Error interno al obtener los objetivos"}

    if not data:
        return {"error": f"No hay datos para {mes}"}

    return data