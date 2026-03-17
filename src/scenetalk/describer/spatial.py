"""Spatial analysis - describing object positions and relationships."""

from __future__ import annotations

from scenetalk.models import (
    ObjectDetection, SpatialRelation, SpatialRelationship, BoundingBox,
)


class SpatialAnalyzer:
    """Describes positions and relationships between detected objects."""

    def analyze(self, objects: list[ObjectDetection]) -> list[SpatialRelationship]:
        """Determine spatial relationships between all pairs of objects."""
        relationships: list[SpatialRelationship] = []
        for i, obj_a in enumerate(objects):
            for j, obj_b in enumerate(objects):
                if i >= j:
                    continue
                rel = self._determine_relation(obj_a.bbox, obj_b.bbox)
                relationships.append(
                    SpatialRelationship(
                        subject=obj_a.label,
                        relation=rel,
                        reference=obj_b.label,
                    )
                )
        return relationships

    def describe_position(self, obj: ObjectDetection) -> str:
        """Describe the position of an object in the image."""
        cx, cy = obj.bbox.center_x, obj.bbox.center_y

        # Horizontal position
        if cx < 0.33:
            h_pos = "on the left side"
        elif cx > 0.66:
            h_pos = "on the right side"
        else:
            h_pos = "in the center"

        # Vertical position
        if cy < 0.33:
            v_pos = "near the top"
        elif cy > 0.66:
            v_pos = "near the bottom"
        else:
            v_pos = "in the middle"

        # Size
        area = obj.bbox.area
        if area > 0.25:
            size = "large"
        elif area > 0.05:
            size = "medium-sized"
        else:
            size = "small"

        return f"A {size} {obj.label} is {h_pos}, {v_pos} of the image."

    def describe_layout(self, objects: list[ObjectDetection]) -> str:
        """Generate an overall layout description."""
        if not objects:
            return "The scene appears to be empty."

        regions: dict[str, list[str]] = {
            "left": [], "center": [], "right": [],
            "top": [], "bottom": [],
        }

        for obj in objects:
            cx, cy = obj.bbox.center_x, obj.bbox.center_y
            if cx < 0.33:
                regions["left"].append(obj.label)
            elif cx > 0.66:
                regions["right"].append(obj.label)
            else:
                regions["center"].append(obj.label)

            if cy < 0.33:
                regions["top"].append(obj.label)
            elif cy > 0.66:
                regions["bottom"].append(obj.label)

        parts: list[str] = []
        for region, items in regions.items():
            if items:
                item_str = ", ".join(dict.fromkeys(items))  # deduplicate preserving order
                parts.append(f"{item_str} on the {region}")

        return "The scene contains " + "; ".join(parts) + "." if parts else "The scene is empty."

    def _determine_relation(self, a: BoundingBox, b: BoundingBox) -> SpatialRelation:
        """Determine the spatial relation between two bounding boxes."""
        dx = a.center_x - b.center_x
        dy = a.center_y - b.center_y

        # Check containment
        if (a.x >= b.x and a.y >= b.y
                and a.x + a.width <= b.x + b.width
                and a.y + a.height <= b.y + b.height):
            return SpatialRelation.INSIDE

        # Check overlap / adjacency
        if abs(dx) < 0.1 and abs(dy) < 0.1:
            return SpatialRelation.NEAR

        # Predominant direction
        if abs(dx) > abs(dy):
            return SpatialRelation.LEFT_OF if dx < 0 else SpatialRelation.RIGHT_OF
        else:
            return SpatialRelation.ABOVE if dy < 0 else SpatialRelation.BELOW
