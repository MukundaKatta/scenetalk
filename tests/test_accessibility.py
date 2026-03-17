"""Tests for accessibility modules."""

from scenetalk.accessibility.alt_text import AltTextGenerator
from scenetalk.accessibility.detailed import DetailedDescriber
from scenetalk.accessibility.navigation import NavigationHelper
from scenetalk.models import (
    ImageScene, ObjectDetection, ObjectCategory, BoundingBox,
    Atmosphere, DescriptionLevel,
)


def _make_scene() -> ImageScene:
    return ImageScene(
        width=640, height=480, scene_type="office",
        atmosphere=[Atmosphere.INDOOR, Atmosphere.BRIGHT],
        objects=[
            ObjectDetection(label="desk", category=ObjectCategory.FURNITURE,
                            confidence=0.9, bbox=BoundingBox(x=0.2, y=0.4, width=0.6, height=0.3)),
            ObjectDetection(label="person", category=ObjectCategory.PERSON,
                            confidence=0.95, bbox=BoundingBox(x=0.35, y=0.2, width=0.2, height=0.5)),
            ObjectDetection(label="laptop", category=ObjectCategory.ELECTRONICS,
                            confidence=0.88, bbox=BoundingBox(x=0.3, y=0.4, width=0.15, height=0.1)),
        ],
    )


def test_alt_text_concise():
    scene = _make_scene()
    text = AltTextGenerator().generate(scene)
    assert len(text) <= 125
    assert "desk" in text or "person" in text


def test_alt_text_empty_scene():
    text = AltTextGenerator().generate(ImageScene())
    assert "no identifiable" in text.lower()


def test_detailed_brief():
    scene = _make_scene()
    desc = DetailedDescriber().describe(scene, DescriptionLevel.BRIEF)
    assert desc.overview
    assert desc.alt_text
    assert not desc.object_descriptions


def test_detailed_standard():
    scene = _make_scene()
    desc = DetailedDescriber().describe(scene, DescriptionLevel.STANDARD)
    assert desc.overview
    assert desc.spatial_description
    assert len(desc.object_descriptions) > 0


def test_detailed_full():
    scene = _make_scene()
    desc = DetailedDescriber().describe(scene, DescriptionLevel.DETAILED)
    assert desc.atmosphere_description
    assert desc.detailed_narrative


def test_navigation_hints():
    scene = _make_scene()
    hints = NavigationHelper().generate_navigation_hints(scene)
    assert len(hints) > 0
    # Should detect the desk as obstacle
    assert any("desk" in h.lower() for h in hints)


def test_navigation_empty_scene():
    hints = NavigationHelper().generate_navigation_hints(ImageScene())
    assert len(hints) == 1
    assert "clear" in hints[0].lower()
