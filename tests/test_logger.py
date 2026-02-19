import pytest
from src.core.logger import Logger

def test_logger_level_change():
    l = Logger(name="test", level="INFO")
    assert l._level == "INFO"
    
    l.set_level("DEBUG")
    assert l._level == "DEBUG"

def test_logger_singleton_configuration():
    # Проверяем что статический флаг работает
    l1 = Logger(name="l1", level="INFO")
    initial_configured = Logger._configured
    
    l2 = Logger(name="l2", level="DEBUG")
    assert Logger._configured == True
    assert initial_configured == True
