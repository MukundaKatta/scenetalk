"""Scene simulator for testing without real images."""

from __future__ import annotations

import random

from scenetalk.models import (
    ImageScene, ObjectDetection, ObjectCategory, BoundingBox, Atmosphere,
)


# Pre-defined scene templates for simulation
SCENE_TEMPLATES: dict[str, dict] = {
    "park": {
        "scene_type": "outdoor park",
        "atmosphere": [Atmosphere.BRIGHT, Atmosphere.OUTDOOR, Atmosphere.CALM],
        "objects": [
            {"label": "tree", "category": ObjectCategory.NATURE,
             "bbox": {"x": 0.0, "y": 0.0, "width": 0.3, "height": 0.7}},
            {"label": "person", "category": ObjectCategory.PERSON,
             "bbox": {"x": 0.4, "y": 0.3, "width": 0.15, "height": 0.4}},
            {"label": "dog", "category": ObjectCategory.ANIMAL,
             "bbox": {"x": 0.6, "y": 0.5, "width": 0.1, "height": 0.1}},
            {"label": "grass", "category": ObjectCategory.NATURE,
             "bbox": {"x": 0.0, "y": 0.7, "width": 1.0, "height": 0.3}},
            {"label": "bird", "category": ObjectCategory.ANIMAL,
             "bbox": {"x": 0.8, "y": 0.1, "width": 0.05, "height": 0.05}},
        ],
    },
    "office": {
        "scene_type": "indoor office",
        "atmosphere": [Atmosphere.INDOOR, Atmosphere.BRIGHT, Atmosphere.CALM],
        "objects": [
            {"label": "desk", "category": ObjectCategory.FURNITURE,
             "bbox": {"x": 0.2, "y": 0.4, "width": 0.6, "height": 0.3}},
            {"label": "chair", "category": ObjectCategory.FURNITURE,
             "bbox": {"x": 0.35, "y": 0.5, "width": 0.2, "height": 0.3}},
            {"label": "laptop", "category": ObjectCategory.ELECTRONICS,
             "bbox": {"x": 0.3, "y": 0.4, "width": 0.15, "height": 0.1}},
            {"label": "monitor", "category": ObjectCategory.ELECTRONICS,
             "bbox": {"x": 0.55, "y": 0.3, "width": 0.15, "height": 0.15}},
            {"label": "person", "category": ObjectCategory.PERSON,
             "bbox": {"x": 0.35, "y": 0.2, "width": 0.2, "height": 0.5}},
            {"label": "lamp", "category": ObjectCategory.FURNITURE,
             "bbox": {"x": 0.8, "y": 0.1, "width": 0.1, "height": 0.25}},
        ],
    },
    "street": {
        "scene_type": "city street",
        "atmosphere": [Atmosphere.OUTDOOR, Atmosphere.BUSY],
        "objects": [
            {"label": "car", "category": ObjectCategory.VEHICLE,
             "bbox": {"x": 0.1, "y": 0.5, "width": 0.25, "height": 0.15}},
            {"label": "car", "category": ObjectCategory.VEHICLE,
             "bbox": {"x": 0.6, "y": 0.45, "width": 0.2, "height": 0.15}},
            {"label": "person", "category": ObjectCategory.PERSON,
             "bbox": {"x": 0.4, "y": 0.3, "width": 0.1, "height": 0.35}},
            {"label": "building", "category": ObjectCategory.BUILDING,
             "bbox": {"x": 0.0, "y": 0.0, "width": 0.35, "height": 0.5}},
            {"label": "building", "category": ObjectCategory.BUILDING,
             "bbox": {"x": 0.65, "y": 0.0, "width": 0.35, "height": 0.45}},
            {"label": "sign", "category": ObjectCategory.OTHER,
             "bbox": {"x": 0.45, "y": 0.15, "width": 0.08, "height": 0.05}},
        ],
    },
    "kitchen": {
        "scene_type": "kitchen",
        "atmosphere": [Atmosphere.INDOOR, Atmosphere.WARM],
        "objects": [
            {"label": "table", "category": ObjectCategory.FURNITURE,
             "bbox": {"x": 0.2, "y": 0.4, "width": 0.6, "height": 0.25}},
            {"label": "cup", "category": ObjectCategory.FOOD,
             "bbox": {"x": 0.3, "y": 0.35, "width": 0.05, "height": 0.08}},
            {"label": "apple", "category": ObjectCategory.FOOD,
             "bbox": {"x": 0.5, "y": 0.38, "width": 0.05, "height": 0.05}},
            {"label": "bottle", "category": ObjectCategory.FOOD,
             "bbox": {"x": 0.65, "y": 0.3, "width": 0.05, "height": 0.12}},
            {"label": "chair", "category": ObjectCategory.FURNITURE,
             "bbox": {"x": 0.1, "y": 0.5, "width": 0.15, "height": 0.3}},
        ],
    },
}


class SceneSimulator:
    """Generates simulated image scenes for testing."""

    @staticmethod
    def from_template(name: str) -> ImageScene:
        """Create a scene from a predefined template."""
        template = SCENE_TEMPLATES.get(name)
        if not template:
            available = ", ".join(SCENE_TEMPLATES.keys())
            raise ValueError(f"Unknown template '{name}'. Available: {available}")

        objects = [
            ObjectDetection(
                label=obj["label"],
                category=obj["category"],
                confidence=round(random.uniform(0.75, 0.99), 3),
                bbox=BoundingBox(**obj["bbox"]),
            )
            for obj in template["objects"]
        ]

        return ImageScene(
            width=640,
            height=480,
            objects=objects,
            atmosphere=template["atmosphere"],
            scene_type=template["scene_type"],
        )

    @staticmethod
    def available_templates() -> list[str]:
        """Return list of available scene templates."""
        return list(SCENE_TEMPLATES.keys())
