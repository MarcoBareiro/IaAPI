import json
from typing import Dict, Any
import httpx
from fastapi import FastAPI, Body
from utils.docs_loader import load_markdown_with_instructions
from prompts.instrucciones import INSTRUCCIONES_GENERALES

from langchain_together import Together  # Chat model
from langchain.prompts import ChatPromptTemplate

import re

import logging

from pydantic import BaseModel     

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class PreguntaRequest(BaseModel):
    pregunta: str

class ParametrosObjetivoMensual(BaseModel):
    mes: str

class InstruccionModel(BaseModel):
    accion: str
    parametros: ParametrosObjetivoMensual
    sugerencias_usuario: str = None    

# --- Función mejorada de extracción JSON ---
def extract_strict_json(text: str) -> Dict[str, Any]:
    """Extrae y valida el JSON de la respuesta del modelo"""
    try:
        # Elimina todo lo que no sea JSON
        text_clean = re.sub(r'[^{}[\]]+', '', text)
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]
        
        # Validación con Pydantic
        data = json.loads(json_str)
        validated = InstruccionModel(**data)
        return validated.dict()
    except Exception as e:
        logger.error(f"Error extrayendo JSON: {str(e)}")
        raise ValueError(f"Formato de respuesta inválido: {str(e)}")



# --------- Tool / Endpoint real ------------------------------------------------
MOCKAPI_URL = "https://688cb01dcd9d22dda5ce179e.mockapi.io/ventas/objetivo_mensual"

async def get_objetivo_mensual(mes: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(MOCKAPI_URL, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()

    registro = next((d for d in data if d["mes"].strip() == mes.strip()), None)
    logger.info("datos del endpoint:\n%s", registro)

    if not registro:
        return {"error": f"No hay datos para {mes}"}

    vendedores = registro["objetivos_por_vendedor"]
    return {
        "mes": mes,
        "total_objetivo_monto": sum(v["objetivo_monto"] for v in vendedores),
        "total_objetivo_ventas": sum(v["objetivo_cantidad_ventas"] for v in vendedores),
        "vendedores": [
            {
                "nombre": v["nombre_vendedor"],
                "sucursal": v["sucursal"],
                "objetivo_monto": v["objetivo_monto"],
                "objetivo_ventas": v["objetivo_cantidad_ventas"],
            }
            for v in vendedores
        ],
    }

# --------- Orquestador ---------------------------------------------------------
async def orquestar(instruccion: Dict[str, Any]) -> Dict[str, Any]:
    accion = instruccion.get("accion")
    params = instruccion.get("parametros", {})

    if accion == "get_objetivo_mensual":
        return await get_objetivo_mensual(**params)

    return {"error": f"Acción desconocida: {accion}"}

# --------- LLM -----------------------------------------------------------------
llm = Together(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    temperature=0,
    together_api_key="3b08fe176664c025aad1781dfdb966b2684b0bd57c8e10fa7c842572158db441",
    max_tokens=500,
    repetition_penalty=1
)

VENTAS_DOC = load_markdown_with_instructions("docs/ventas.md", INSTRUCCIONES_GENERALES)

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", VENTAS_DOC),
        ("human", "{pregunta}"),
    ]
)

# --------- FastAPI endpoint ----------------------------------------------------
@app.post("/query")
async def query(request: PreguntaRequest):
    try:
        prompt = PROMPT.format_messages(pregunta=request.pregunta)    
        respuesta = await llm.ainvoke(prompt)
        logger.info("Respuesta del modelo:\n%s", respuesta)

        instruccion = extract_strict_json(respuesta)
        logger.info("Instrucción:\n%s", instruccion)

        datos = await orquestar(instruccion)
        logger.info("datos del orquestador:\n%s", datos)

        return {
            "instruccion_generada": instruccion,
            "datos": datos,
        }

    except json.JSONDecodeError as je:
        return {
            "error": f"JSON inválido: {str(je)}",
            "raw": respuesta
        }
    except Exception as e:
        logger.error("Error no controlado: %s", e)
        return {
            "error": str(e)
        }
     
