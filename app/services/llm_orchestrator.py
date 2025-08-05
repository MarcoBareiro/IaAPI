import logging
from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain_together import Together
from app.models.schemas import InstruccionModel
from app.services.ventas_service import get_objetivo_mensual
from app.utils.json_utils import extract_strict_json
from app.utils.docs_loader import load_markdown_with_instructions
from app.utils.tabular_query_engine import ejecutar_sql_sobre_json
from app.prompts.instrucciones import INSTRUCCIONES_GENERALES
from app.core.config import TOGETHER_API_KEY, LLM_MODEL

logger = logging.getLogger(__name__)

llm = Together(
    model=LLM_MODEL,
    together_api_key=TOGETHER_API_KEY,
    temperature=0,
    max_tokens=500,
    repetition_penalty=1
)

VENTAS_DOC = load_markdown_with_instructions("docs/ventas.md", INSTRUCCIONES_GENERALES)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", VENTAS_DOC),
    ("human", "{pregunta}"),
])


async def orquestar(instruccion: InstruccionModel) -> Dict[str, Any]:
    accion = instruccion.accion
    params = instruccion.parametros
    sql_query = instruccion.consulta_sql

    if accion == "get_objetivo_mensual":

        # if not params.mes:
        #     return {
        #         "accion": "solicitar_parametro",
        #         "parametros": {"parametro_faltante": "mes"},
        #         "sugerencias_usuario": "Por favor, indícame el mes para obtener el objetivo de ventas (formato YYYY-MM)."
        #     }

        datos = await get_objetivo_mensual(**params.dict())
        try:
            resultado_sql = ejecutar_sql_sobre_json(datos, sql_query)
            return {
                "resultado_sql": resultado_sql,
                "datos_endpoint": datos,
                "consulta_sql": sql_query
            }
        except Exception as e:
            return {
                "error": f"Error ejecutando SQL: {str(e)}",
                "datos_endpoint": datos
            }

    return {"error": f"Acción desconocida: {accion}"}


async def procesar_pregunta(pregunta: str):
    prompt = PROMPT.format_messages(pregunta=pregunta)
    respuesta = await llm.ainvoke(prompt)
    logger.info("Respuesta del modelo:\n%s", respuesta)

    instruccion = extract_strict_json(respuesta)
    datos = await orquestar(instruccion)

    return {
        "instruccion_generada": instruccion,
        "datos": datos
    }
