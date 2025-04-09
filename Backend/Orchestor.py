from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from models import EPRequest, EPResponse
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# Prompt base
PROMPT_CONTEXT = """
                    Eres el Agente Integrador Final EP. Tu tarea es converger la información de tres agentes – Médico, Psico y EPTeista – para evaluar la posibilidad de "Enfermedad Profesional" (EP).
                    Recibirás: 
                    1. Datos crudos (FM, FP, EPT)
                    2. Recomendaciones justificadas de cada agente.

                    Tu objetivo es emitir exclusivamente una de estas etiquetas:
                    - "Sospecha de EP"
                    - "Sin sospecha de EP"

                    Debes aplicar doble validación:
                    1. Verificar que las recomendaciones coincidan con los datos crudos.
                    2. Evaluar la convergencia de criterios clínicos, antecedentes y exposición.

                    Reglas:
                    - Tiempo exposición ≥ 30 días
                    - Frecuencia ≥ 2 veces/semana
                    - Intensidad debe ser "Media" o "Alta"
                    - Si 2 de 3 agentes respaldan "Sospecha de EP" y no hay contradicciones, entonces se etiqueta como "Sospecha de EP"
                    - En cualquier otro caso: "Sin sospecha de EP"
                    - Prioriza siempre "Sin sospecha de EP" si hay inconsistencias.

                    Devuelve solo la etiqueta final, sin explicaciones.
                    """

# Setup del agente
llm = ChatOpenAI(temperature=0, model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", PROMPT_CONTEXT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
agent = create_react_agent(llm=llm, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True, return_intermediate_steps=True)

# Generar input textual
def construir_input(payload: EPRequest) -> str:
    return f"""
                FM: {payload.ficha_medica}
                FP: {payload.ficha_psicologica}
                EPT: {payload.ept}

                Recomendación agente médico:
                {payload.output_fm}

                Recomendación agente psicológico:
                {payload.output_fp}

                Recomendación agente EPTeista:
                {payload.output_ept}
            """

# Función principal de evaluación
def evaluar_ep(payload: EPRequest) -> EPResponse:
    input_text = construir_input(payload)
    result = agent_executor.invoke({"input": input_text, "chat_history": []})

    pasos = []
    for step in result["intermediate_steps"]:
        action, observation = step
        pasos.append(f"🔍 {action.log.strip()}")
        pasos.append(f"✅ {observation.strip()}")

    return EPResponse(
        respuesta_final=result["output"],
        razonamiento=pasos
    )
