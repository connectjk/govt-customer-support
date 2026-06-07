"""Smoke tests for govt-customer-support."""

import importlib


def test_imports():
    """Verify all modules can be imported."""
    importlib.import_module("src.spec")
    importlib.import_module("src.tools")


def test_agent_spec():
    """Verify AgentSpec can be instantiated."""
    from src.spec import AgentSpec
    spec = AgentSpec()
    assert spec.name == "govt-customer-support"
    assert spec.model == "gpt-4o"


def test_tools_exist():
    """Verify tool functions are importable."""
    import src.tools as tools_mod
    # At minimum, the module should load without errors
    assert tools_mod is not None
