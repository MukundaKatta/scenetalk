"""Tests for scene description."""

from scenetalk.describer.scene import SceneDescriber
from scenetalk.models import ImageScene, ObjectDetection, ObjectCategory, BoundingBox, Atmosphere


def _make_scene() -> ImageScene:
    return ImageScene(
        width=640,
        height=480,
        scene_type="park",
        atmosphere=[Atmosphere.BRIGHT, Atmosphere.OUTDOOR],
        objects=[
            ObjectDetection(
                label="person", category=ObjectCategory.PERSON, confidence=0.95,
                bbox=BoundingBox(x=0.3, y=0.2, width=0.2, height=0.5),
            ),
            ObjectDetection(
                label="dog", category=ObjectCategory.ANIMAL, confidence=0.9,
                bbox=BoundingBox(x=0.6, y=0.5, width=0.15, height=0.15),
            ),
        ],
    )


def test_describe_generates_all_layers():
    scene = _make_scene()
    desc = SceneDescriber().describe(scene)
    assert desc.overview
    assert len(desc.object_descriptions) == 2
    assert desc.spatial_description
    assert desc.atmosphere_description
    assert desc.detailed_narrative


def test_empty_scene():
    scene = ImageScene()
    desc = SceneDescriber().describe(scene)
    assert "empty" in desc.overview.lower()


def test_atmosphere_description():
    scene = _make_scene()
    desc = SceneDescriber().describe(scene)
    assert "bright" in desc.atmosphere_description.lower()
    assert "outdoor" in desc.atmosphere_description.lower()
