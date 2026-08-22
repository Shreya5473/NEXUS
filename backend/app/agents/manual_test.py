from app.agents.finance_agent import run_finance_agent
from app.agents.sales_agent import run_sales_agent

finance_context = "Last quarter revenue: $1,200,000. This quarter revenue: $1,344,000."
finance_question = "How much did our revenue grow this quarter?"
print("FINANCE AGENT:")
print(run_finance_agent(finance_question, finance_context))

print()

sales_context = "Last month: 10200 leads, 1120 conversions. This month: 9800 leads, 740 conversions."
sales_question = "Why did our conversion rate drop this month?"
print("SALES AGENT:")
print(run_sales_agent(sales_question, sales_context))