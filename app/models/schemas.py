from pydantic import BaseModel

class PreguntaRequest(BaseModel):
    pregunta: str

class ParametrosObjetivoMensual(BaseModel):
    mes: str

class InstruccionModel(BaseModel):
    accion: str
    parametros: ParametrosObjetivoMensual
    consulta_sql: str