from auto import board
from datetime import datetime
from core.logs.logger import log


def sugerir_acciones():
    tareas = board.load_tasks()
    ahora = datetime.now()
    propuestas = []

    titulos = [t["title"].lower() for t in tareas]

    if not any("video" in t for t in titulos):
        propuestas.append(
            {
                "type": "publicar",
                "title": "Crear nuevo video sobre",
                "prioridad": "media",
                "target": "x",
            }
        )

    if not any("reel" in t for t in titulos):
        propuestas.append(
            {
                "type": "publicar",
                "title": "Subir reel simbólico de bienvenida a Q•zar",
                "prioridad": "alta",
                "target": "discord",
            }
        )

    if not any("comentario" in t or "responder" in t for t in titulos):
        propuestas.append(
            {
                "type": "responder",
                "title": "Responder comentarios recientes de TikTok",
                "prioridad": "alta",
            }
        )

    if not any("artículo" in t or "medium" in t for t in titulos):
        propuestas.append(
            {
                "type": "publicar",
                "title": "Publicar artículo breve sobre coherencia simbólica",
                "prioridad": "media",
                "target": "medium",
            }
        )

    for p in propuestas:
        if not board.was_already_done(p["title"], p["type"]):
            log(f"[Sugerencia] 💡 Nueva acción simbólica: {p['title']}")
            board.add_task(p)
        else:
            log(f"[Sugerencia] (Ignorada, ya fue hecha): {p['title']}")
