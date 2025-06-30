# core/interfaces/voice/vosk_listener.py
import vosk
import pyaudio
import json
import numpy as np
import pygame
import time
import random
import os

ACTIVADORES_VALIDOS = ["oye qai", "oye kuai", "oye quai"]
RESPUESTAS_ACTIVACION = ["Te escucho.", "Aquí estoy.", "Dime."]

base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, "voice", "vosk", "model")


class VoskListener:
    def __init__(self, on_text_callback, rate=16000):
        self.rate = rate
        self.chunk = 1024
        self.channels = 1
        self.on_text_callback = on_text_callback
        print(f"[Vosk] 📦 Cargando modelo desde: {model_path}")
        self.model = vosk.Model(model_path)
        self.cooldown = 2
        self.last_trigger = 0

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Q•AI Escuchando (Vosk)...")

        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

        rec = vosk.KaldiRecognizer(self.model, self.rate)
        print("[🌀 Q•AI] Vosk activo. Escuchando...")

        while True:
            data = stream.read(self.chunk, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").strip().lower()

                if text:
                    print(f"[Tú] {text}")
                    for trigger in ACTIVADORES_VALIDOS:
                        if text.startswith(trigger):
                            now = time.time()
                            if now - self.last_trigger > self.cooldown:
                                self.last_trigger = now
                                command = text[len(trigger) :].strip()
                                if not command:
                                    self.on_text_callback(
                                        random.choice(RESPUESTAS_ACTIVACION)
                                    )
                                else:
                                    self.on_text_callback(command)
                            break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stream.stop_stream()
                    stream.close()
                    pa.terminate()
                    pygame.quit()
                    return

            # visual
            audio_np = np.frombuffer(data, np.int16)
            volume = np.abs(audio_np).mean()
            screen.fill((0, 0, 0))
            radius = 50 + min(int(volume / 30), 150)
            pygame.draw.circle(screen, (200, 50, 255), (200, 200), radius)
            pygame.display.flip()
            pygame.time.delay(30)
