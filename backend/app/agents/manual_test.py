from app.orchestrator.orchestrator import run_orchestrator

finance_context = "Last quarter revenue: $1,200,000. This quarter revenue: $1,344,000."
sales_context = "Last month: 10200 leads, 1120 conversions. This month: 9800 leads, 740 conversions."

question = "Our sales conversion dropped this month — did that affect our revenue growth too?"

answer = run_orchestrator(question, finance_context, sales_context)
print(answer)