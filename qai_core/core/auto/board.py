import os
import json
from datetime import datetime

LOGS_DIR = os.path.join("logs")
os.makedirs(LOGS_DIR, exist_ok=True)

BOARD_PATH = os.path.join(LOGS_DIR, "board.json")
ARCHIVE_PATH = os.path.join(LOGS_DIR, "board_archive.json")

if not os.path.exists(BOARD_PATH):
    with open(BOARD_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)

if not os.path.exists(ARCHIVE_PATH):
    with open(ARCHIVE_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)


def add_task(task: dict):
    tasks = load_tasks()
    task["status"] = "pending"
    task["timestamp"] = datetime.now().isoformat()
    tasks.append(task)
    with open(BOARD_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    print(f"[Board] Tarea añadida: {task['type']}")


def load_tasks():
    with open(BOARD_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def show_tasks():
    tasks = load_tasks()
    if not tasks:
        print("[Board] No hay tareas pendientes.")
        return
    for i, task in enumerate(tasks):
        status = task.get("status", "pending")
        print(f"{i+1}. [{task['type'].upper()}] {task.get('title', '...')} ({status})")


def clear_tasks():
    with open(BOARD_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)
    print("[Board] Tareas borradas.")


def complete_task(index: int):
    tasks = load_tasks()
    if index < 1 or index > len(tasks):
        print(f"[Board] Índice fuera de rango. Total: {len(tasks)} tareas.")
        return

    completed = tasks[index - 1]
    completed["status"] = "done"

    # Guardar en board_archive.json
    with open(ARCHIVE_PATH, "r", encoding="utf-8") as f:
        archive = json.load(f)
    archive.append(completed)
    with open(ARCHIVE_PATH, "w", encoding="utf-8") as f:
        json.dump(archive, f, indent=2, ensure_ascii=False)

    # Eliminar de board.json
    tasks.pop(index - 1)
    with open(BOARD_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

    print(f"[Board] Tarea #{index} marcada como completada y archivada.")


def show_archive():
    if not os.path.exists(ARCHIVE_PATH):
        print("[Archive] No hay historial aún.")
        return

    with open(ARCHIVE_PATH, "r", encoding="utf-8") as f:
        archive = json.load(f)

    if not archive:
        print("[Archive] El historial está vacío.")
        return

    print("[Archive] Tareas completadas:")
    for i, task in enumerate(archive):
        print(
            f"{i+1}. [{task['type'].upper()}] {task.get('title', '...')} ({task.get('timestamp', '')})"
        )


def was_already_done(title: str, type_filter: str = None) -> bool:
    if not os.path.exists(ARCHIVE_PATH):
        return False
    with open(ARCHIVE_PATH, "r", encoding="utf-8") as f:
        archive = json.load(f)
    for task in archive:
        if type_filter and task.get("type") != type_filter:
            continue
        if title.lower().strip() in task.get("title", "").lower():
            return True
    return False
