import pandas as pd
import duckdb
from typing import Any, Dict, List

def ejecutar_sql_sobre_json(json_data: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    # Convertimos el JSON a un DataFrame
    df = pd.DataFrame(json_data)

    # Ejecutamos la consulta SQL sobre el DataFrame con DuckDB
    resultado = duckdb.query_df(df, "data", sql_query).to_df()

    # Convertimos el resultado a lista de diccionarios
    return resultado.to_dict(orient="records")