from typing import Optional, Union

from datahorse.agent.base_security import BaseSecurity
from datahorse.config import load_config_from_json
from datahorse.ee.agents.advanced_security_agent.pipeline.advanced_security_pipeline import (
    AdvancedSecurityPipeline,
)
from datahorse.pipelines.abstract_pipeline import AbstractPipeline
from datahorse.pipelines.pipeline_context import PipelineContext
from datahorse.schemas.df_config import Config


class AdvancedSecurityAgent(BaseSecurity):
    def __init__(
        self,
        config: Optional[Union[Config, dict]] = None,
        pipeline: AbstractPipeline = None,
    ) -> None:
        context = None

        if isinstance(config, dict):
            config = Config(**load_config_from_json(config))
        elif config is None:
            config = Config()

        context = PipelineContext(None, config)

        pipeline = pipeline or AdvancedSecurityPipeline(context=context)
        super().__init__(pipeline)

    def evaluate(self, query: str) -> bool:
        return self.pipeline.run(query)
