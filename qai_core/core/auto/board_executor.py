from datetime import datetime, timedelta
from core.auto import board
from core.logs.logger import log
from modules.social.social import post_to_network


class BoardExecutor:
    def __init__(self):
        self.actions = {
            "publicar": self.publicar_contenido,
            "responder": self.responder_comentario,
            "evento": self.recordar_evento,
        }

    def run_supervisor_mode(self):
        """No ejecuta tareas. Solo evalúa y propone decisiones"""
        from auto import board
        from datetime import datetime, timedelta

        tareas = board.load_tasks()
        ahora = datetime.now()

        for i, t in enumerate(tareas):
            if t.get("status") != "pending":
                continue

            fecha = t.get("fecha")
            prioridad = t.get("prioridad", "media")

            if fecha:
                try:
                    fecha_dt = datetime.fromisoformat(fecha)
                    tiempo_restante = fecha_dt - ahora

                    if tiempo_restante < timedelta(minutes=0):
                        log(f"[Supervisor] ⚠️ Tarea vencida: {t['title']} ({prioridad})")
                    elif tiempo_restante < timedelta(minutes=30):
                        log(f"[Supervisor] ⏳ En breve: {t['title']} ({prioridad})")
                except Exception as e:
                    log(f"[Supervisor] ❌ Fecha malformada en tarea: {e}")
            else:
                log(f"[Supervisor] 🧠 Tarea sin fecha: {t['title']} ({prioridad})")

    def run_auto_executor(self):
        tareas = board.load_tasks()
        ahora = datetime.now()

        for i, t in enumerate(tareas):
            if t.get("status") != "pending":
                continue

            tipo = t.get("type")
            prioridad = t.get("prioridad", "media").lower()
            fecha_txt = t.get("fecha")
            action = self.actions.get(tipo)

            if not action:
                log(f"[Executor] ⚠️ Tipo no soportado: {tipo}")
                continue

            minutos_faltantes = 99999
            if fecha_txt:
                try:
                    fecha_dt = datetime.fromisoformat(fecha_txt)
                    minutos_faltantes = (fecha_dt - ahora).total_seconds() / 60
                except Exception as e:
                    log(f"[Executor] ❌ Fecha inválida: {e}")

            if prioridad == "alta" and minutos_faltantes < 10:
                log(f"[AUTO] 🔥 Ejecutando urgente: {t['title']}")
                try:
                    action(t)
                    board.complete_task(i + 1)
                except Exception as e:
                    log(f"[Executor] ❌ Error: {e}")
            else:
                log(
                    f"[AUTO] 🧠 Tarea pendiente observada: {t['title']} (Prioridad: {prioridad}, faltan {int(minutos_faltantes)}m)"
                )

    def publicar_contenido(self, task):
        target = task.get("target", "all")
        mensaje = f"📤 Publicación automática: {task.get('title')}"
        log(f"[AUTO] {mensaje}")
        post_to_network(mensaje, target)

    def responder_comentario(self, task):
        log(f"[AUTO] 💬 Respondiendo simbólicamente: {task.get('title')}")

    def recordar_evento(self, task):
        log(f"[AUTO] 📅 Recordatorio de evento: {task.get('title')}")
