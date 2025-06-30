# Q•AI – Asistente de Inteligencia Simbólica

Q•AI es un asistente simbólico modular y extensible en Python, diseñado para operar como motor de pensamiento, organizador de ideas, y ejecutor de comandos simbólicos.

## 🚀 Características

- Núcleo simbólico basado en contexto
- Memoria simbólica, afectiva y episódica
- Interfaz modular con comandos personalizados
- Modo de sugerencia de acciones (autónomo)
- Compatible con módulos externos descargables

## 🧠 Estructura

qai_core/
├── core/ # Núcleo del asistente (memoria, IO, reflexión)
├── store/ # Módulos y extensiones descargables
├── config/ # Configuraciones por JSON
└── main.py # Punto de entrada del sistema

## ⚙️ Instalación

```bash
git clone https://github.com/Q-YZX0/QarzAI
cd qai
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
python qai_core/main.py
