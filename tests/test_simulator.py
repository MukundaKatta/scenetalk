"""Tests for scene simulator."""

import pytest

from scenetalk.simulator import SceneSimulator


def test_available_templates():
    templates = SceneSimulator.available_templates()
    assert "park" in templates
    assert "office" in templates
    assert "street" in templates
    assert "kitchen" in templates


def test_from_template_park():
    scene = SceneSimulator.from_template("park")
    assert scene.scene_type == "outdoor park"
    assert len(scene.objects) > 0
    assert len(scene.atmosphere) > 0


def test_from_template_office():
    scene = SceneSimulator.from_template("office")
    assert scene.scene_type == "indoor office"
    labels = [o.label for o in scene.objects]
    assert "desk" in labels
    assert "laptop" in labels


def test_unknown_template():
    with pytest.raises(ValueError, match="Unknown template"):
        SceneSimulator.from_template("nonexistent")
