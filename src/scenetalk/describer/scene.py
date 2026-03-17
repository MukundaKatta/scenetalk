"""Scene description generation."""

from __future__ import annotations

from scenetalk.models import (
    ImageScene, SceneDescription, ObjectDetection, Atmosphere,
)
from scenetalk.describer.spatial import SpatialAnalyzer


class SceneDescriber:
    """Generates detailed natural-language scene descriptions from image features."""

    def __init__(self) -> None:
        self._spatial = SpatialAnalyzer()

    def describe(self, scene: ImageScene) -> SceneDescription:
        """Generate a full multi-layered description of the scene."""
        overview = self._generate_overview(scene)
        obj_descs = self._describe_objects(scene.objects)
        spatial = self._spatial.describe_layout(scene.objects)
        atmosphere = self._describe_atmosphere(scene.atmosphere)
        narrative = self._build_narrative(overview, obj_descs, spatial, atmosphere)

        return SceneDescription(
            overview=overview,
            object_descriptions=obj_descs,
            spatial_description=spatial,
            atmosphere_description=atmosphere,
            detailed_narrative=narrative,
        )

    def _generate_overview(self, scene: ImageScene) -> str:
        """Create a high-level overview of the scene."""
        n_objects = len(scene.objects)
        if n_objects == 0:
            return "An empty scene with no identifiable objects."

        categories = list({obj.category.value for obj in scene.objects})
        scene_type = scene.scene_type or "scene"

        if n_objects == 1:
            obj = scene.objects[0]
            return f"A {scene_type} containing a single {obj.label}."

        cat_str = ", ".join(categories[:3])
        return f"A {scene_type} with {n_objects} objects including {cat_str} elements."

    def _describe_objects(self, objects: list[ObjectDetection]) -> list[str]:
        """Generate individual descriptions for each detected object."""
        descriptions: list[str] = []
        for obj in objects:
            pos = self._spatial.describe_position(obj)
            conf = f" (confidence: {obj.confidence:.0%})"
            attrs = ""
            if obj.attributes:
                attrs = f" It appears to be {', '.join(obj.attributes)}."
            descriptions.append(f"{pos}{conf}{attrs}")
        return descriptions

    def _describe_atmosphere(self, atmosphere: list[Atmosphere]) -> str:
        """Describe the atmosphere/mood of the scene."""
        if not atmosphere:
            return "The atmosphere cannot be determined from the available information."

        descriptions: dict[Atmosphere, str] = {
            Atmosphere.BRIGHT: "The scene is well-lit and bright",
            Atmosphere.DARK: "The scene is dimly lit or dark",
            Atmosphere.WARM: "The scene has warm, inviting tones",
            Atmosphere.COOL: "The scene has cool, muted tones",
            Atmosphere.BUSY: "The scene appears busy and active",
            Atmosphere.CALM: "The scene appears calm and peaceful",
            Atmosphere.INDOOR: "This appears to be an indoor setting",
            Atmosphere.OUTDOOR: "This appears to be an outdoor setting",
        }

        parts = [descriptions.get(a, str(a.value)) for a in atmosphere]
        return ". ".join(parts) + "."

    def _build_narrative(
        self,
        overview: str,
        obj_descs: list[str],
        spatial: str,
        atmosphere: str,
    ) -> str:
        """Build a cohesive narrative combining all descriptions."""
        parts = [overview, atmosphere, spatial]
        if obj_descs:
            parts.append("Looking more closely: " + " ".join(obj_descs[:5]))
        return " ".join(parts)
