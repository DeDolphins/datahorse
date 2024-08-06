"""Example of using PandasAI with am Excel file."""

import os

from datahorse import Agent

# By default, unless you choose a different LLM, it will use BambooLLM.
# You can get your free API key signing up at https://datahorse.ai/ (you can also configure it in your .env file)
os.environ["DATAHORSE_API_KEY"] = "your-api-key"

agent = Agent("examples/data/Loan payments data.xlsx")
response = agent.chat("How many loans are from men and have been paid off?")
print(response)
# Output: 247 loans have been paid off by men.
