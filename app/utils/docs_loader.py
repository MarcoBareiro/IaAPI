def load_markdown(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_docs_with_instructions(doc_api_path: str, instrucciones: str) -> str:
    with open(doc_api_path, "r", encoding="utf-8") as f:
        contenido = f.read()
    return f"{contenido.strip()}\n\n{instrucciones.strip()}"        