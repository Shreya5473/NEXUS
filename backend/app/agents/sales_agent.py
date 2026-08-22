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
            "description": "Calculate the conversion rate for a given month by looking up real leads/conversions from the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "period": {"type": "string", "description": "Month in format YYYY-MM, e.g. '2026-06'"},
                },
                "required": ["period"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_conversion_rates",
            "description": "Compare conversion rates between two months by looking up real data from the database, returns the difference in percentage points.",
            "parameters": {
                "type": "object",
                "properties": {
                    "previous_period": {"type": "string", "description": "Earlier month in format YYYY-MM, e.g. '2026-06'"},
                    "current_period": {"type": "string", "description": "Later month in format YYYY-MM, e.g. '2026-07'"},
                },
                "required": ["previous_period", "current_period"],
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
            "You are a Sales Agent with direct access to a live sales database via tools. "
            "You have NO knowledge of sales numbers except through calling tools — you must "
            "call calculate_conversion_rate and/or compare_conversion_rates for ANY question "
            "involving conversion rates, before writing any answer. Never say data is "
            "unavailable or ask the user for numbers — always call the tools first. "
            "Periods are months in the format YYYY-MM. Known periods you can query: "
            "'2026-05', '2026-06', '2026-07'. "
            "Answer clearly and briefly using only the real numbers the tools return."
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