from app.orchestrator.orchestrator import run_orchestrator

question = "Our sales conversion dropped from June to July — did that affect our revenue growth from Q2 to Q3?"

answer = run_orchestrator(question, finance_context="", sales_context="")
print(answer)