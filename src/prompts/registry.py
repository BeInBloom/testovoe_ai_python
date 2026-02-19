from pathlib import Path
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel


class PromptConfig(BaseModel):
    name: str
    description: str
    prompt: str


class PromptRegistry:
    def __init__(self, prompts_path: str):
        self._prompts_path = Path(prompts_path)
        self._prompts: Dict[str, PromptConfig] = {}

    def load(self) -> None:
        if not self._prompts_path.exists():
            return

        for file_path in self._find_yaml_files():
            self._load_single_file(file_path)

    def _find_yaml_files(self) -> List[Path]:
        return list(self._prompts_path.glob("*.yaml")) + list(
            self._prompts_path.glob("*.yml")
        )

    def _load_single_file(self, file_path: Path) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            config = self._create_config(data, file_path)
            self._prompts[config.name] = config
        except Exception:
            # TODO: Logger should be here, but avoid coupling for now or add to __init__
            pass

    def _create_config(self, data: Dict, file_path: Path) -> PromptConfig:
        return PromptConfig(
            name=data.get("name", file_path.stem),
            description=data.get("description", ""),
            prompt=data.get("prompt", ""),
        )

    def get(self, name: str) -> Optional[PromptConfig]:
        return self._prompts.get(name)

    def list_prompts(self) -> Dict[str, PromptConfig]:
        return self._prompts.copy()
