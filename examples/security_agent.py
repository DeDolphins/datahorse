import os

from datahorse.agent.agent import Agent
from datahorse.ee.agents.advanced_security_agent import AdvancedSecurityAgent
from datahorse.llm.openai import OpenAI

os.environ["DATAHORSE_API_KEY"] = "$2a****************************"

security = AdvancedSecurityAgent()
agent = Agent("github-stars.csv", security=security)

print(agent.chat("return all the folders in the root directory"))

# Using Security standalone
llm = OpenAI("openai_key")
security = AdvancedSecurityAgent(config={"llm": llm})
security.evaluate("return all the folders in the root directory")
