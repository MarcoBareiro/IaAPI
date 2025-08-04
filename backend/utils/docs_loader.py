def load_markdown(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_markdown_with_instructions(md_path: str, instrucciones: str) -> str:
    with open(md_path, "r", encoding="utf-8") as f:
        contenido_md = f.read()
    return f"{contenido_md.strip()}\n\n{instrucciones.strip()}"        