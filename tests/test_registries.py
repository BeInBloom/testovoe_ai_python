import pytest
import yaml
import toml
from pathlib import Path
from src.prompts.registry import PromptRegistry
from src.skills.registry import SkillRegistry
from src.core.logger import Logger

@pytest.fixture
def logger():
    return Logger(name="test", level="DEBUG")

def test_prompt_registry_load_valid(tmp_path):
    # Создаем временный YAML
    prompt_file = tmp_path / "test.yaml"
    data = {
        "name": "test_prompt",
        "description": "Test Desc",
        "prompt": "Test Content"
    }
    prompt_file.write_text(yaml.dump(data))
    
    registry = PromptRegistry(str(tmp_path))
    registry.load()
    
    prompt = registry.get("test_prompt")
    assert prompt is not None
    assert prompt.prompt == "Test Content"

def test_prompt_registry_load_corrupted(tmp_path):
    # Файл с битым YAML
    bad_file = tmp_path / "bad.yaml"
    bad_file.write_text("name: : : :")
    
    registry = PromptRegistry(str(tmp_path))
    # Не должно падать, должно просто пропустить файл (согласно текущей реализации)
    registry.load()
    assert len(registry.list_prompts()) == 0

def test_skill_registry_load_toml(tmp_path, logger):
    skill_file = tmp_path / "skill.toml"
    data = {
        "name": "toml_skill",
        "description": "TOML Desc",
        "prompt": "TOML Prompt"
    }
    skill_file.write_text(toml.dumps(data))
    
    registry = SkillRegistry(str(tmp_path), logger)
    registry.load()
    
    skill = registry.get("toml_skill")
    assert skill is not None
    assert skill.prompt == "TOML Prompt"

def test_skill_registry_empty_dir(tmp_path, logger):
    registry = SkillRegistry(str(tmp_path / "non_existent"), logger)
    registry.load() # Не должно падать
    assert len(registry.list_skills()) == 0
