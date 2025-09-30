import os
from dotenv import load_dotenv
from langchain.tools import StructuredTool
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
# Tools
from tools import (
search,
    )

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta GOOGLE_API_KEY. Define la variable de entorno o agrégala en .env")

# definir herramientas de agente
tools = [
search
    ]


# generar instancia del llm
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

# configurar system prompt
system = (
        "Eres un Agente de Viajes útil. "
        "Puedes razonar paso a paso y usar tools cuando ayuden a obtener datos concretos. "
        "Responde en español, de forma clara y concisa. "
        "Cuando sea útil, llama a las herramientas para calcular costos o crear itinerarios."
    )


agent_executor = create_react_agent(model, tools)


if __name__ == "__main__":

    try:


        # bucle principal
        while True:

            # solicitar input al usuario
            user = input("\nEscribe tu prompt (o 'salir'): ").strip()
            if user.lower() in {"salir", "exit", "quit"}:
                break

            input_message = {"role": "user", "content": user}

            # invocar al agente
            response = agent_executor.invoke({"messages": [input_message]})

            # imprimir respuesta
            print("\n--- Respuesta ---")
            for message in response["messages"]:
                message.pretty_print()


    except KeyboardInterrupt:
        pass


