import os

from datahorse import Agent
from datahorse.connectors.yahoo_finance import YahooFinanceConnector

yahoo_connector = YahooFinanceConnector("MSFT")

# By default, unless you choose a different LLM, it will use BambooLLM.
# You can get your free API key signing up at https://datahorse.ai/ (you can also configure it in your .env file)
os.environ["DATAHORSE_API_KEY"] = "your-api-key"

agent = Agent(yahoo_connector)

response = agent.chat("What is the closing price for yesterday?")
print(response)
