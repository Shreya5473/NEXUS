import json
from groq import Groq
from app.core.config import GROQ_API_KEY
from app.tools.finance_tools import calculate_growth_rate

client = Groq(api_key=GROQ_API_KEY)

# This describes our tool to the LLM.
# The LLM reads this and decides on its own when to use it.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_growth_rate",
            "description": "Calculate percentage growth between two financial values (e.g. revenue, expenses) across two periods.",
            "parameters": {
                "type": "object",
                "properties": {
                    "previous_value": {"type": "number", "description": "The value in the earlier period"},
                    "current_value": {"type": "number", "description": "The value in the later period"},
                },
                "required": ["previous_value", "current_value"],
            },
        },
    }
]

# Maps the tool name the LLM asks for to the actual Python function that implements it.
AVAILABLE_TOOLS = {
    "calculate_growth_rate": calculate_growth_rate,
}


def run_finance_agent(user_question: str, context: str) -> str:
    """
    context: plain text with the actual numbers available, e.g.
    'Last quarter revenue: $1,200,000. This quarter revenue: $1,344,000.'
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Finance Agent for a business intelligence system. "
                "You must NEVER calculate numbers yourself — always use the "
                "calculate_growth_rate tool for any growth/percentage calculation. "
                "Answer clearly and briefly."
            ),
        },
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_question}"},
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=TOOLS,
    )

    reply = response.choices[0].message

    # If the LLM didn't need a tool, just return its answer
    if not reply.tool_calls:
        return reply.content

    # The LLM wants to call a tool — actually run it
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

    # Send the tool's real result back to the LLM so it can explain it in words
    final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
    )

    return final_response.choices[0].message.content