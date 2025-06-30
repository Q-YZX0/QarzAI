import sys
import json
import traceback

# Asegura acceso a rutas internas
sys.path.append("core")

from core.memory.boot_context import SymbolicContext
from core.interfaces.io import IOHandler

# Importa log
try:
    from core.logs.logger import log
except ImportError:

    def log(msg):
        print("[Q•AI]", msg)


# Carga configuración
def load_config():
    try:
        with open("config/qai_config.json", "r") as f:
            return json.load(f)
    except Exception as e:
        log(f"❌ Error al cargar configuración: {e}")
        return {}


# 🧠 Inicializa Q•AI
def main():
    config = load_config()

    with SymbolicContext() as memory:
        config["memory"] = memory
    print("🧠 Contexto cerrado. Continuando...")
    if config.get("reflejo_sistemico", True):
        try:
            from core.auto.board_executor import BoardExecutor
            from core.auto.idea_suggester import sugerir_acciones

            log("🔁 Iniciando reflejo simbólico del sistema...")
            BoardExecutor().run_supervisor_mode()
            sugerir_acciones()
        except Exception as e:
            log(f"⚠️ Falló reflejo simbólico: {e}")
    try:
        io = IOHandler(config)
        print("✅ IOHandler construido.")
        log("🌐 Bienvenido a Q.ark Console")
        io.start()
    except Exception as e:
        log("❌ Error iniciando Q•AI:")
        log(str(e))
        log(traceback.format_exc())


if __name__ == "__main__":
    main()
