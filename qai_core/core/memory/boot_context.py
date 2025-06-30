from contextlib import contextmanager
from core.memory.memory import MemoryManager


@contextmanager
def SymbolicContext():
    memory = MemoryManager()

    nombre = memory.get_fact("nombre_usuario") or "desconocido"
    plan = memory.get_fact("plan_general") or "sin plan"
    foco = memory.get_focus() or "ninguno"

    print("🧠 Cargando contexto simbólico...")
    print(f"👤 Usuario: {nombre}")
    print(f"📌 Plan: {plan}")
    print(f"🎯 Foco actual: {foco}")
    print("🗒️ Últimos mensajes:")
    for m in memory.get_recent_messages(3):
        print(f"[{m['role']}] {m['content']}")

    try:
        yield memory
    finally:
        try:
            print("💾 Guardando snapshot de contexto...")
            memory._save()
            print("✅ Memoria persistente actualizada.")
        except Exception as e:
            print(f"❌ Error al guardar memoria persistente: {e}")
