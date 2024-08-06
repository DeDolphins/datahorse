"""Example of using PandasAI with a CSV file."""

from datahorse import Agent



agent = Agent(
    "examples/data/Loan payments data.csv",
)
response = agent.chat("How many loans are from men and have been paid off?")

print(response)
# Output: 247 loans have been paid off by men.
