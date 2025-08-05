# Documentación del tópico: Ventas

## 🎯 Descripción general

Este módulo permite consultar y operar sobre datos de ventas mensuales, objetivos y métricas.

---

## ✅ Acción: `get_objetivo_mensual`

- **Descripción**: Devuelve el objetivo de ventas para un mes específico.
- **Parámetros**:
  - `mes`: (obligatorio) Fecha en formato `YYYY-MM`. Ejemplo: `2025-05`.
- **Ejemplo de respuesta de la acción**

```json
[
  {{
    "mes": "2025-05",
    "id_vendedor": 1,
    "nombre_vendedor": "Carlos Gómez",
    "sucursal": "Asunción",
    "objetivo_monto": 50000000,
    "objetivo_cantidad_ventas": 15
  }},
  {{
    "mes": "2025-05",
    "id_vendedor": 2,
    "nombre_vendedor": "Laura Rivas",
    "sucursal": "Luque",
    "objetivo_monto": 48000000,
    "objetivo_cantidad_ventas": 13
  }}
  // ... más registros
]
```
