from core.memory.memory import MemoryManager
from core.generators.generator import Generator
from core.router.dynamic_router import dynamic_commands, load_all_modules
from core.router import core_commands, memory_commands
from core.router import board_commands, module_commands
import random


FRASES_NO_ENTENDIDO = [
    "No entendí bien, ¿puedes repetir?",
    "¿Eso era un comando?",
    "No tengo eso registrado como acción.",
    "Hmm... no capté ninguna instrucción clara.",
    "¿Puedes decirlo otra vez de otro modo?",
]


class CommandRouter:
    def __init__(self, config, io_handler):
        print("[CommandRouter] 🧠 Iniciando construcción del router...")
        self.config = config
        self.io = io_handler
        self.memory = config.get("memory") or MemoryManager()
        self.generator = Generator()
        load_all_modules()
        print("MCP Command Router modularizado.")

        # Esto debe ir aquí, dentro del __init__
        self.command_modules = [
            core_commands,
            memory_commands,
            board_commands,
            module_commands,
        ]

    def route(self, command):
        command = command.strip()
        if not command:
            return "No command received."

        for module in self.command_modules:
            result = module.handle(command, self)
            if result is not None:
                return result

        for dyn in dynamic_commands:
            if command.startswith(dyn["trigger"]):
                return dyn["function"](command, self)

        respuesta = random.choice(FRASES_NO_ENTENDIDO)
        return respuesta
