from typing import Optional

from datahorse.ee.agents.judge_agent.pipeline.judge_prompt_generation import (
    JudgePromptGeneration,
)
from datahorse.ee.agents.judge_agent.pipeline.llm_call import LLMCall
from datahorse.helpers.logger import Logger
from datahorse.helpers.query_exec_tracker import QueryExecTracker
from datahorse.pipelines.judge.judge_pipeline_input import JudgePipelineInput
from datahorse.pipelines.pipeline import Pipeline
from datahorse.pipelines.pipeline_context import PipelineContext


class JudgePipeline:
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
                JudgePromptGeneration(),
                LLMCall(),
            ],
        )

    def run(self, input: JudgePipelineInput):
        return self.pipeline.run(input)
