from datahorse.helpers.logger import Logger
from datahorse.pipelines.pipeline import Pipeline
from datahorse.pipelines.pipeline_context import PipelineContext


class BaseJudge:
    context: PipelineContext
    pipeline: Pipeline
    logger: Logger

    def __init__(
        self,
        pipeline: Pipeline,
    ) -> None:
        self.pipeline = pipeline

    def evaluate(self, query: str, code: str) -> bool:
        raise NotImplementedError
