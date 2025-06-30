from core.router.router import CommandRouter
from core.interfaces.whisper_listener import WhisperListener
from core.interfaces.vosk_listener import VoskListener

import pyttsx3

PELIGROSOS = ["rm ", "os.", "__import__", "eval(", "exec(", "subprocess"]


class IOHandler:
    def __init__(self, config):
        print("[DEBUG] 🧠 Entrando a IOHandler.__init__()")
        self.config = config
        self.memory = config.get("memory")
        print("[DEBUG] 📦 Config y memoria asignadas")
        self.modo_actual = config.get("modo", "voz")
        self.awaiting_confirmation = False
        self.last_input = None
        print("[DEBUG] 🧠 Inicializando motor de voz...")
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 180)
        self._set_spanish_voice()
        print("[DEBUG] 🗣️ Motor de voz listo")
        self.router = CommandRouter(config, self)
        print("[DEBUG] 🔀 Router cargado")
        print(f"[IOHandler] ⚙️ Inicializando IOHandler en modo: {self.modo_actual}")

        modo_voz = config.get("voz_engine", "whisper")
        print(f"[DEBUG] Modo de voz desde config: {modo_voz}")
        try:
            if modo_voz == "whisper":
                print("[IOHandler] 🎙️ Usando Whisper...")
                self.listener = WhisperListener(on_text_callback=self.handle_text)
            elif modo_voz == "vosk":
                print("[IOHandler] 🧠 Usando Vosk...")
                self.listener = VoskListener(on_text_callback=self.handle_text)
            else:
                raise ValueError(f"Modo de voz desconocido: {modo_voz}")
        except Exception as e:
            print(f"[IOHandler] ❌ Fallo al cargar el listener de voz: {e}")
            raise

        print("[IOHandler] ✅ Inicialización completa.")

    def es_input_seguro(texto):
        return not any(p in texto.lower() for p in PELIGROSOS)

    def _set_spanish_voice(self):
        for voice in self.engine.getProperty("voices"):
            if "es" in voice.id.lower() or "spanish" in voice.name.lower():
                self.engine.setProperty("voice", voice.id)
                break

    def speak(self, text: str):
        self.engine.stop()
        self.engine.say(text)
        self.engine.runAndWait()

    def handle_text(self, text: str):
        text = text.strip().lower()
        print(f"[Tú] {text}")
        if self.memory:
            self.memory.store_message("user", text)

        # ✅ Corrección simbólica
        if self.awaiting_confirmation and text.startswith("no, dije"):
            correccion = text.replace("no, dije", "").strip(": ").strip()
            print(f"[Q•AI] ✅ Corrigiendo a: “{correccion}”")
            if self.memory:
                self.memory.store_message(
                    "correccion",
                    {"mal_interpretado": self.last_input, "corregido_a": correccion},
                )
            self.awaiting_confirmation = False
            self.handle_text(correccion)  # Reprocesa el nuevo texto
            return

        # ✅ Confirmación directa positiva (ej: "sí", "correcto")
        if self.awaiting_confirmation and text in (
            "sí",
            "si",
            "correcto",
            "afirmativo",
        ):
            print(f"[Q•AI] ✅ Confirmado: “{self.last_input}”")
            response = self.router.route(self.last_input)
            if response:
                print(f"[Q•AI] {response}")
                self.speak(response)
                if self.memory:
                    self.memory.store_message("qai", response)
            self.awaiting_confirmation = False
            return

        # 🔁 Cambio de modo
        if text in ("modo texto", "desactiva voz", "quiero escribir"):
            self.switch_to_text_mode()
            return

        if text in ("exit", "quit", "salir"):
            print("[Q•AI] Hasta luego.")
            if self.memory:
                self.memory.store_message("qai", "Hasta luego.")
            exit()

        # 🧠 Confirmación previa si viene de voz
        if self.config.get("modo") == "voz":
            self.last_input = text
            self.awaiting_confirmation = True
            confirm_msg = f"¿Entendí bien?: {text}"
            print(f"[Q•AI] {confirm_msg}")
            self.speak(confirm_msg)
            return

        # ✨ Procesamiento normal (modo texto o ya confirmado)
        response = self.router.route(text)
        if response:
            print(f"[Q•AI] {response}")
            self.speak(response)
            if self.memory:
                self.memory.store_message("qai", response)
        self.awaiting_confirmation = False

    def start(self):
        print("[IOHandler] 🚀 Entrando a start()")
        if self.modo_actual == "voz":
            print("[IOHandler] 🎙️ Modo VOZ detectado.")
            self.listener.start()
            print("[IOHandler] ❌ Listener terminó inesperadamente.")
        else:
            print("[IOHandler] 🖥️ Modo TEXTO detectado.")
            self.loop_consola()

    def loop_consola(self):
        print("[⌨️  Modo texto activo. Escribe tus comandos.]")
        while True:
            try:
                user_input = input("> ").strip()
                if user_input.lower() in ("exit", "salir", "quit"):
                    print("[Q•AI] Hasta luego.")
                    if self.memory:
                        self.memory.store_message("qai", "Hasta luego.")
                    break
                self.handle_text(user_input)
            except KeyboardInterrupt:
                print("\n[Q•AI] Interrumpido por el usuario.")
                break

    def switch_mode(self, nuevo_modo: str):
        if nuevo_modo == self.modo_actual:
            return f"[Q•AI] Ya estás en modo {nuevo_modo}."

        if nuevo_modo == "texto":
            if self.listener:
                self.listener.stop()
            self.modo_actual = "texto"
            return "⌨️ Modo texto activado."

        elif nuevo_modo == "voz":
            self.modo_actual = "voz"
            return "🎙️ Modo voz activado."
