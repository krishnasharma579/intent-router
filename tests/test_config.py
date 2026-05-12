import importlib

import pytest


def _reload_config_module():
    import core.config as config_module

    return importlib.reload(config_module)


def test_config_uses_consistent_default_model_name(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.delenv("MODEL_NAME", raising=False)
    monkeypatch.delenv("ROUTER_TEMPERATURE", raising=False)

    config = _reload_config_module()

    assert config.settings.MODEL_NAME == config.DEFAULT_MODEL_NAME


def test_invalid_router_temperature_raises_clear_error(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("ROUTER_TEMPERATURE", "hot")

    with pytest.raises(ValueError, match="Invalid ROUTER_TEMPERATURE value"):
        _reload_config_module()
