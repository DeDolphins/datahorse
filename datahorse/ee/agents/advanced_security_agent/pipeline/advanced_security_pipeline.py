from typing import Optional

from datahorse.ee.agents.advanced_security_agent.pipeline.advanced_security_prompt_generation import (
    AdvancedSecurityPromptGeneration,
)
from datahorse.ee.agents.judge_agent.pipeline.llm_call import LLMCall
from datahorse.helpers.logger import Logger
from datahorse.helpers.query_exec_tracker import QueryExecTracker
from datahorse.pipelines.pipeline import Pipeline
from datahorse.pipelines.pipeline_context import PipelineContext


class AdvancedSecurityPipeline:
    def __init__(
        self,
        context: Optional[PipelineContext] = None,
        logger: Optional[Logger] = None,
        query_exec_tracker: QueryExecTracker = None,
    ):
        self.query_exec_tracker = query_exec_tracker

        self.pipeline = Pipeline(
            context=context,
            logger=logger,
            query_exec_tracker=self.query_exec_tracker,
            steps=[
                AdvancedSecurityPromptGeneration(),
                LLMCall(),
            ],
        )

    def run(self, input: str):
        return self.pipeline.run(input)
