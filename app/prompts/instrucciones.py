INSTRUCCIONES_GENERALES = """
instrucciones:
  objetivo: Proporcionar un formato estándar para respuestas de modelos de lenguaje que interactúan con bases de datos.
  estructura_de_respuesta:
    accion: string
    parametros: object
    consulta_sql: string
  reglas:
    - La respuesta debe ser un objeto JSON válido y parseable directamente.
    - No se permite el uso de markdown o bloques de código.
    - No se permite agregar texto fuera del JSON.
    - La respuesta debe ser única y no repetida.
    - El campo `consulta_sql` debe contener una única consulta SQL válida y relevante para la pregunta del humano, sin incluir consultas adicionales o innecesarias.
    - El query generado debe nombre a la tabla llamada data
  ejemplos:
    - pregunta: "¿Cuál es el total de registros en la base de datos?"
      respuesta: {{"accion": "get_registros", "parametros": {{"param1:value1"}}, "consulta_sql": "SELECT COUNT(*) AS total_registros FROM data"}}
"""