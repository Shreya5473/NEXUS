import json
from groq import Groq
from app.core.config import GROQ_API_KEY
from app.tools.sales_tools import calculate_conversion_rate, compare_conversion_rates

client = Groq(api_key=GROQ_API_KEY)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_conversion_rate",
            "description": "Calculate conversion rate percentage from lead count and conversion count.",
            "parameters": {
                "type": "object",
                "properties": {
                    "leads": {"type": "integer", "description": "Total number of leads"},
                    "conversions": {"type": "integer", "description": "Number of leads that converted"},
                },
                "required": ["leads", "conversions"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_conversion_rates",
            "description": "Compare two conversion rates and return the difference in percentage points.",
            "parameters": {
                "type": "object",
                "properties": {
                    "previous_rate": {"type": "number", "description": "Conversion rate from the earlier period"},
                    "current_rate": {"type": "number", "description": "Conversion rate from the later period"},
                },
                "required": ["previous_rate", "current_rate"],
            },
        },
    },
]

AVAILABLE_TOOLS = {
    "calculate_conversion_rate": calculate_conversion_rate,
    "compare_conversion_rates": compare_conversion_rates,
}


def run_sales_agent(user_question: str, context: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Sales Agent for a business intelligence system. "
                "You must NEVER calculate numbers yourself — always use the "
                "available tools for any rate or comparison calculation. "
                "Answer clearly and briefly."
            ),
        },
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_question}"},
    ]

    # Loop lets the agent call multiple tools in sequence if it needs to
    # (e.g. calculate a rate, THEN compare it to a previous rate)
    while True:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=TOOLS,
        )

        reply = response.choices[0].message

        if not reply.tool_calls:
            return reply.content

        messages.append(reply)

        for tool_call in reply.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            function_to_call = AVAILABLE_TOOLS[function_name]
            result = function_to_call(**function_args)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(result),
                }
            )