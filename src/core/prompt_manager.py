from src.core.logger import Logger
from src.prompts.registry import PromptRegistry
from src.skills.registry import SkillRegistry


class PromptManager:
    def __init__(
        self,
        prompt_registry: PromptRegistry,
        skill_registry: SkillRegistry,
        logger: Logger,
    ):
        self._prompt_registry = prompt_registry
        self._skill_registry = skill_registry
        self._logger = logger

    def select(
        self, prompt_name: str | None = None, skill_name: str | None = None
    ) -> str:
        self._load_registries()

        if skill_name:
            skill_prompt = self._get_skill_prompt(skill_name)
            if skill_prompt:
                return skill_prompt

        if prompt_name:
            named_prompt = self._get_named_prompt(prompt_name)
            if named_prompt:
                return named_prompt

        return self._get_default_prompt()

    def _load_registries(self) -> None:
        self._prompt_registry.load()
        self._skill_registry.load()

    def _get_skill_prompt(self, skill_name: str) -> str | None:
        skill = self._skill_registry.get(skill_name)
        if skill and skill.prompt:
            self._logger.info(f"Using skill: {skill_name}")
            return skill.prompt
        self._logger.warning(f"Skill not found or has no prompt: {skill_name}")
        return None

    def _get_named_prompt(self, prompt_name: str) -> str | None:
        prompt = self._prompt_registry.get(prompt_name)
        if prompt:
            self._logger.info(f"Using prompt: {prompt_name}")
            return prompt.prompt
        self._logger.warning(f"Prompt not found: {prompt_name}")
        return None

    def _get_default_prompt(self) -> str:
        default_prompt = self._prompt_registry.get("default")
        if default_prompt:
            self._logger.info("Using default prompt")
            return default_prompt.prompt
        return "Проанализируй документы и создай краткое саммари."
