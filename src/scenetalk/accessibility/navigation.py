"""Navigation helper for describing paths and obstacles."""

from __future__ import annotations

from scenetalk.models import (
    ImageScene, ObjectDetection, ObjectCategory, BoundingBox,
)


# Object categories that are typically obstacles
OBSTACLE_CATEGORIES = {
    ObjectCategory.FURNITURE,
    ObjectCategory.VEHICLE,
    ObjectCategory.BUILDING,
}

# Objects that are path-related
PATH_OBJECTS = {"sidewalk", "road", "path", "stairs", "ramp", "door", "gate", "corridor"}


class NavigationHelper:
    """Describes paths, obstacles, and navigation-relevant features."""

    def describe_obstacles(self, scene: ImageScene) -> list[str]:
        """Identify and describe potential obstacles in the scene."""
        hints: list[str] = []
        for obj in scene.objects:
            if obj.category in OBSTACLE_CATEGORIES or obj.label in OBSTACLE_CATEGORIES:
                pos = self._position_description(obj.bbox)
                hints.append(f"Obstacle: {obj.label} located {pos}.")
        return hints

    def describe_paths(self, scene: ImageScene) -> list[str]:
        """Describe any visible paths or walkable areas."""
        hints: list[str] = []
        for obj in scene.objects:
            if obj.label.lower() in PATH_OBJECTS:
                pos = self._position_description(obj.bbox)
                hints.append(f"Path element: {obj.label} visible {pos}.")

        if not hints:
            # Infer walkable space from absence of obstacles in lower region
            lower_obstacles = [
                o for o in scene.objects
                if o.bbox.center_y > 0.6 and o.category in OBSTACLE_CATEGORIES
            ]
            if not lower_obstacles:
                hints.append("The lower portion of the scene appears clear for navigation.")
            else:
                hints.append("The lower portion has obstacles that may block movement.")

        return hints

    def generate_navigation_hints(self, scene: ImageScene) -> list[str]:
        """Generate comprehensive navigation hints for the scene."""
        hints: list[str] = []

        # General scene assessment
        if not scene.objects:
            return ["The scene appears clear with no identifiable objects or obstacles."]

        # People detection
        people = [o for o in scene.objects if o.category == ObjectCategory.PERSON]
        if people:
            hints.append(f"There {'is' if len(people) == 1 else 'are'} {len(people)} "
                         f"{'person' if len(people) == 1 else 'people'} in the scene.")

        # Obstacles
        hints.extend(self.describe_obstacles(scene))

        # Paths
        hints.extend(self.describe_paths(scene))

        # Proximity warnings for large objects
        for obj in scene.objects:
            if obj.bbox.area > 0.2:
                pos = self._position_description(obj.bbox)
                hints.append(f"Large object ({obj.label}) occupies significant space {pos}.")

        return hints if hints else ["The scene has no notable navigation features."]

    @staticmethod
    def _position_description(bbox: BoundingBox) -> str:
        """Convert bounding box position to a natural description."""
        cx, cy = bbox.center_x, bbox.center_y
        parts: list[str] = []

        if cx < 0.33:
            parts.append("to the left")
        elif cx > 0.66:
            parts.append("to the right")
        else:
            parts.append("in the center")

        if cy < 0.33:
            parts.append("in the upper area")
        elif cy > 0.66:
            parts.append("in the lower area")

        return ", ".join(parts) if parts else "in the scene"
