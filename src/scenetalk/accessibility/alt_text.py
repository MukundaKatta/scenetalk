"""Alt text generation for images."""

from __future__ import annotations

from scenetalk.models import ImageScene, ObjectDetection


class AltTextGenerator:
    """Creates concise alt text suitable for screen readers."""

    MAX_ALT_LENGTH = 125  # Recommended max for alt text

    def generate(self, scene: ImageScene) -> str:
        """Generate concise alt text for the scene."""
        if not scene.objects:
            return "An image with no identifiable content."

        # Group objects by label
        counts: dict[str, int] = {}
        for obj in scene.objects:
            counts[obj.label] = counts.get(obj.label, 0) + 1

        # Build description
        parts: list[str] = []
        for label, count in sorted(counts.items(), key=lambda x: -x[1]):
            if count > 1:
                parts.append(f"{count} {label}s")
            else:
                parts.append(f"a {label}")

        scene_prefix = f"{scene.scene_type} with " if scene.scene_type else "Image showing "
        text = scene_prefix + self._join_list(parts)

        # Truncate if too long
        if len(text) > self.MAX_ALT_LENGTH:
            text = text[: self.MAX_ALT_LENGTH - 3].rsplit(" ", 1)[0] + "..."

        return text

    def generate_from_objects(self, objects: list[ObjectDetection]) -> str:
        """Generate alt text from a list of detected objects."""
        scene = ImageScene(objects=objects)
        return self.generate(scene)

    @staticmethod
    def _join_list(items: list[str]) -> str:
        """Join items with commas and 'and'."""
        if not items:
            return ""
        if len(items) == 1:
            return items[0]
        if len(items) == 2:
            return f"{items[0]} and {items[1]}"
        return ", ".join(items[:-1]) + f", and {items[-1]}"
