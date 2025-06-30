import os
from dotenv import load_dotenv
from openai import OpenAI


class Generator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "[Generator] No se encontró el key de openai en .env o en entorno."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.simulado = False

        self.context_path = os.path.join("qai_core", "config", "qai_context.md")
        self.system_context = self._load_context()

    def _load_context(self) -> str:
        try:
            with open(self.context_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return "Eres Q•AI, el asistente simbólico central de Q.arz."

    def create(self, prompt: str) -> str:
        if self.simulado:
            return self._respuesta_simulada(prompt)

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_context},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            self.simulado = True
            return self._respuesta_simulada(prompt, str(e))

    def _respuesta_simulada(self, prompt: str, error_msg: str = "") -> str:
        print(f"[Error no conexion] ⚠️ Modo simulado activado.")
        print(error_msg)
        return f"[Q•AI] No puedo contactar con la fuente ahora."
