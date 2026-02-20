from pathlib import Path
from typing import Any

import toml
import yaml

from src.core.logger import Logger


class SkillConfig:
    def __init__(
        self,
        name: str,
        description: str,
        module: str,
        class_name: str,
        config: dict[str, Any],
        prompt: str | None = None,
    ):
        self.name = name
        self.description = description
        self.module = module
        self.class_name = class_name
        self.config = config
        self.prompt = prompt


class SkillRegistry:
    def __init__(self, skills_path: str, logger: Logger):
        self._skills_path = Path(skills_path)
        self._logger = logger
        self._skills: dict[str, SkillConfig] = {}

    def load(self) -> None:
        self._logger.info(f"Loading skills from {self._skills_path}")
        if not self._skills_path.exists():
            return

        self._load_from_format("*.yaml", self._load_yaml_file)
        self._load_from_format("*.yml", self._load_yaml_file)
        self._load_from_format("*.toml", self._load_toml_file)

        self._logger.info(f"Loaded {len(self._skills)} skill(s)")

    def _load_from_format(self, pattern: str, loader_func: Any) -> None:
        for file_path in self._skills_path.glob(pattern):
            loader_func(file_path)

    def _load_yaml_file(self, file_path: Path) -> None:
        with open(file_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self._add_skill(data, file_path)

    def _load_toml_file(self, file_path: Path) -> None:
        with open(file_path, encoding="utf-8") as f:
            data = toml.load(f)
        self._add_skill(data, file_path)

    def _add_skill(self, data: dict, file_path: Path) -> None:
        config = SkillConfig(
            name=data.get("name", file_path.stem),
            description=data.get("description", ""),
            module=data.get("module", "src.skills"),
            class_name=data.get("class", f"{file_path.stem.capitalize()}Skill"),
            config=data.get("config", {}),
            prompt=data.get("prompt"),
        )
        self._skills[config.name] = config

    def get(self, name: str) -> SkillConfig | None:
        return self._skills.get(name)

    def list_skills(self) -> dict[str, SkillConfig]:
        return self._skills.copy()
