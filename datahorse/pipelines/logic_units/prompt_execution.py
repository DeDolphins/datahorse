from typing import Any

from datahorse.exceptions import LLMNotFoundError
from datahorse.pipelines.base_logic_unit import BaseLogicUnit
from datahorse.prompts.file_based_prompt import FileBasedPrompt


class PromptExecution(BaseLogicUnit):
    def execute(self, input: FileBasedPrompt, **kwargs) -> Any:
        config = kwargs.get("config")
        if config is None or getattr(config, "llm", None) is None:
            raise LLMNotFoundError()
        llm = getattr(config, "llm")
        return llm.call(input)
