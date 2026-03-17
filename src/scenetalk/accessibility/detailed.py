"""Detailed layered descriptions for accessibility."""

from __future__ import annotations

from scenetalk.models import ImageScene, SceneDescription, DescriptionLevel
from scenetalk.describer.scene import SceneDescriber
from scenetalk.accessibility.alt_text import AltTextGenerator


class DetailedDescriber:
    """Generates layered descriptions: overview, objects, spatial, atmosphere."""

    def __init__(self) -> None:
        self._scene_describer = SceneDescriber()
        self._alt_gen = AltTextGenerator()

    def describe(self, scene: ImageScene, level: DescriptionLevel = DescriptionLevel.STANDARD) -> SceneDescription:
        """Generate a description at the requested detail level."""
        full = self._scene_describer.describe(scene)
        full.alt_text = self._alt_gen.generate(scene)

        if level == DescriptionLevel.BRIEF:
            return SceneDescription(
                overview=full.overview,
                alt_text=full.alt_text,
            )
        elif level == DescriptionLevel.STANDARD:
            return SceneDescription(
                overview=full.overview,
                object_descriptions=full.object_descriptions[:5],
                spatial_description=full.spatial_description,
                alt_text=full.alt_text,
            )
        else:  # DETAILED
            return full

    def describe_layer(self, scene: ImageScene, layer: str) -> str:
        """Get a specific description layer.

        Layers: overview, objects, spatial, atmosphere
        """
        full = self._scene_describer.describe(scene)
        layers = {
            "overview": full.overview,
            "objects": " ".join(full.object_descriptions),
            "spatial": full.spatial_description,
            "atmosphere": full.atmosphere_description,
        }
        return layers.get(layer, f"Unknown layer: {layer}")
