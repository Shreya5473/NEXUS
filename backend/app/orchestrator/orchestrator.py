import json
from groq import Groq
from app.core.config import GROQ_API_KEY
from app.agents.finance_agent import run_finance_agent
from app.agents.sales_agent import run_sales_agent

client = Groq(api_key=GROQ_API_KEY)

# Each agent described as a "tool" the orchestrator can call.
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "finance_agent",
            "description": "Handles questions about revenue, expenses, profit, financial growth, and financial comparisons between periods.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The specific question to ask the Finance Agent"},
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sales_agent",
            "description": "Handles questions about leads, conversions, conversion rates, and sales performance between periods.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The specific question to ask the Sales Agent"},
                },
                "required": ["question"],
            },
        },
    },
]


def run_orchestrator(user_question: str, finance_context: str, sales_context: str) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are the orchestrator for a multi-agent business intelligence system. "
                "Given a user's question, decide which specialist agent(s) are relevant and "
                "call them. You can call more than one agent if the question needs it. "
                "Once you have their findings, synthesize a single clear answer that combines "
                "what each agent found."
            ),
        },
        {"role": "user", "content": user_question},
    ]

    # Loop lets the orchestrator call multiple agents in sequence
    # (e.g. Finance first, then Sales, before giving a final combined answer)
    while True:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=AGENT_TOOLS,
        )

        reply = response.choices[0].message

        if not reply.tool_calls:
            return reply.content

        messages.append(reply)

        for tool_call in reply.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            sub_question = function_args["question"]

            if function_name == "finance_agent":
                result = run_finance_agent(sub_question, finance_context)
            elif function_name == "sales_agent":
                result = run_sales_agent(sub_question, sales_context)
            else:
                result = "Unknown agent."

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": result,
                }
            )