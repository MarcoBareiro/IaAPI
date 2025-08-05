import json
import re
import logging
from typing import Dict, Any
from app.models.schemas import InstruccionModel

logger = logging.getLogger(__name__)

def extract_strict_json(text: str) -> Dict[str, Any]:
    try:
        text_clean = re.sub(r'[^{}[\]]+', '', text)
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]

        data = json.loads(json_str)
        return InstruccionModel(**data)
    except Exception as e:
        logger.error(f"Error extrayendo JSON: {str(e)}")
        raise ValueError(f"Formato de respuesta inválido: {str(e)}")
