import os
from dotenv import load_dotenv
from langchain.tools import StructuredTool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
# Tools
from tools import (
    CalcCostosInput, calc_costos,
    ItinerarioInput, itinerario_simple,
    ChecklistInput, checklist_viaje,
    ConvertirMonedaInput, convertir_moneda,
)

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta GOOGLE_API_KEY. Define la variable de entorno o agrégala en .env")

# definir herramientas de agente
tools = [
        StructuredTool.from_function(
            func=calc_costos,
            name="calc_costos",
            description="Calcula un desglose y total de costos de viaje.",
            args_schema=CalcCostosInput,
        ),
        StructuredTool.from_function(
            func=itinerario_simple,
            name="itinerario_simple",
            description="Genera un itinerario sencillo de N días para un destino.",
            args_schema=ItinerarioInput,
        ),
        StructuredTool.from_function(
            func=checklist_viaje,
            name="checklist_viaje",
            description="Crea una checklist básica según el tipo de viaje.",
            args_schema=ChecklistInput,
        ),
        StructuredTool.from_function(
            func=convertir_moneda,
            name="convertir_moneda",
            description="Convierte montos entre monedas (tasa demo o manual).",
            args_schema=ConvertirMonedaInput,
        ),
    ]


# generar instancia del llm
llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash',
        api_key=API_KEY,
        temperature=0.3,
        max_output_tokens=1024,
    )

# configurar system prompt
system = (
        "Eres un Agente de Viajes útil. "
        "Puedes razonar paso a paso y usar tools cuando ayuden a obtener datos concretos. "
        "Responde en español, de forma clara y concisa. "
        "Cuando sea útil, llama a las herramientas para calcular costos, crear itinerarios, "
        "hacer checklists o convertir moneda."
    )

# configurar prompt general integrando el input, el chat_history y el agent_scratchpad
prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

# crear instancia del agente
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

# crear instancia del executor del agente
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)





if __name__ == "__main__":

    try:
        # inicializar chat_history
        chat_history = []

        # bucle principal
        while True:

            # solicitar input al usuario
            user = input("\nEscribe tu prompt (o 'salir'): ").strip()
            if user.lower() in {"salir", "exit", "quit"}:
                break

            # invocar al agente
            out = agent_executor.invoke({"input": user, "chat_history": chat_history})

            # imprimir respuesta
            print("\n--- Respuesta ---")
            print(out.get("output", out))

            # actualizar chat_history
            chat_history.append(HumanMessage(content=user))
            chat_history.append(AIMessage(content=out.get("output", "")))
    except KeyboardInterrupt:
        pass


