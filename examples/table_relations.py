from datahorse.agent.base import Agent
from datahorse.connectors.sql import PostgreSQLConnector
from datahorse.ee.connectors.relations import ForeignKey, PrimaryKey
from datahorse.llm.openai import OpenAI

llm = OpenAI("sk-*************")

config_ = {"llm": llm, "direct_sql": True}

payment_connector = PostgreSQLConnector(
    config={
        "host": "localhost",
        "port": 5432,
        "database": "testdb",
        "username": "postgres",
        "password": "*****",
        "table": "orders",
    },
    connector_relations=[
        PrimaryKey("id"),
        ForeignKey(
            field="customer_id", foreign_table="customers", foreign_table_field="id"
        ),
    ],
)

customer_connector = PostgreSQLConnector(
    config={
        "host": "localhost",
        "port": 5432,
        "database": "mydb",
        "username": "root",
        "password": "root",
        "table": "customers",
    },
    connector_relations=[PrimaryKey("id")],
)

agent = Agent([payment_connector, customer_connector], config=config_, memory_size=10)

response = agent.chat("return orders count groupby country")

print(response)
