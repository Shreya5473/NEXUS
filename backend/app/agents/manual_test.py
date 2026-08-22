from app.agents.finance_agent import run_finance_agent

context = "Last quarter revenue: $1,200,000. This quarter revenue: $1,344,000."
question = "How much did our revenue grow this quarter?"

answer = run_finance_agent(question, context)
print(answer)