import pyaudio
import numpy as np
import time
import pygame
import random
import whisper
import tempfile
import wave

ACTIVADORES_VALIDOS = [
    "oye kuai",
    "oye qai",
    "oye quai",
    "oye quaii",
    "oye quai!",
    "oye quai kuai",
]

RESPUESTAS_ACTIVACION = [
    "Te escucho.",
    "¿Sí?",
    "Aquí estoy.",
    "Dime.",
    "Conectado, Kuai presente.",
    "Kuai operativo.",
    "Sistema en línea.",
    "Estoy contigo.",
    "¿En qué te puedo ayudar?",
    "Procesando tu atención simbólica.",
]


class WhisperListener:
    def __init__(self, on_text_callback, model_name="tiny", rate=16000):
        self.chunk = 1024
        self.rate = rate
        self.channels = 1
        self.format = pyaudio.paInt16
        self.on_text_callback = on_text_callback
        self.model = whisper.load_model(model_name)
        self.cooldown = 2
        self.last_trigger = 0
        self.buffer = b""

    def transcribe_buffer(self, audio_bytes):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                temp_path = f.name

            with wave.open(temp_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.rate)
                wf.writeframes(audio_bytes)

            result = self.model.transcribe(temp_path, language="es")
            return result.get("text", "").lower().strip()
        except Exception as e:
            print(f"[LiveListener] ❌ Error al transcribir audio: {e}")
            return ""
        finally:
            try:
                import os

                os.remove(temp_path)
            except Exception as e:
                print(f"[LiveListener] ⚠️ No se pudo eliminar archivo temporal: {e}")

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Q•AI Escuchando...")

        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )
        stream.start_stream()

        print("[🌀 Q•AI] Visualizador activo. Esperando voz...")

        while True:
            try:
                data = stream.read(self.chunk, exception_on_overflow=False)
                self.buffer += data
            except Exception as e:
                print(f"[LiveListener] ❌ Error al leer audio: {e}")
                continue

            audio_np = np.frombuffer(data, np.int16)
            volume = np.abs(audio_np).mean()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stream.stop_stream()
                    stream.close()
                    pa.terminate()
                    pygame.quit()
                    return

            screen.fill((0, 0, 0))
            radius = 50 + min(int(volume / 30), 150)
            pygame.draw.circle(screen, (0, 200, 255), (200, 200), radius)
            pygame.display.flip()

            # Procesar cada 2 segundos de audio
            if len(self.buffer) >= self.rate * 5 * 2:
                text = self.transcribe_buffer(self.buffer)
                self.buffer = b""
                if text:
                    print(f"[Tú] {text}")
                    for trigger in ACTIVADORES_VALIDOS:
                        if text.startswith(trigger):
                            now = time.time()
                            if now - self.last_trigger > self.cooldown:
                                self.last_trigger = now
                                print(f"[🧠 Q•AI] Activado por: {trigger}")
                                command = text[len(trigger) :].strip()
                                if not command:
                                    self.on_text_callback(
                                        random.choice(RESPUESTAS_ACTIVACION)
                                    )
                                else:
                                    self.on_text_callback(command)
                            break

            pygame.time.delay(30)
