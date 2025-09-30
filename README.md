# Workshop: De LLMs a Agentes con LangChain + Gemini

## 1) Requisitos
- Python 3.10+
- Una API key de Google Generative AI (Gemini)
  - Consíguela en: https://ai.google.dev
  - Crea un archivo `.env` con tu clave (ver `.env.example`)

## 2) Instalación
```bash
python -m venv .venv
source .venv/bin/activate          # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # pega tu clave en .env
