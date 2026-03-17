"""Data models for SceneTalk."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ObjectCategory(str, Enum):
    PERSON = "person"
    ANIMAL = "animal"
    VEHICLE = "vehicle"
    FURNITURE = "furniture"
    FOOD = "food"
    ELECTRONICS = "electronics"
    NATURE = "nature"
    BUILDING = "building"
    CLOTHING = "clothing"
    TOOL = "tool"
    OTHER = "other"


class SpatialRelation(str, Enum):
    LEFT_OF = "left of"
    RIGHT_OF = "right of"
    ABOVE = "above"
    BELOW = "below"
    IN_FRONT_OF = "in front of"
    BEHIND = "behind"
    NEXT_TO = "next to"
    INSIDE = "inside"
    ON_TOP_OF = "on top of"
    NEAR = "near"
    FAR_FROM = "far from"
    CENTER = "center"


class Atmosphere(str, Enum):
    BRIGHT = "bright"
    DARK = "dark"
    WARM = "warm"
    COOL = "cool"
    BUSY = "busy"
    CALM = "calm"
    INDOOR = "indoor"
    OUTDOOR = "outdoor"


class BoundingBox(BaseModel):
    """Bounding box for a detected object."""

    x: float = Field(ge=0.0, le=1.0, description="Left edge (0-1)")
    y: float = Field(ge=0.0, le=1.0, description="Top edge (0-1)")
    width: float = Field(ge=0.0, le=1.0)
    height: float = Field(ge=0.0, le=1.0)

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2

    @property
    def area(self) -> float:
        return self.width * self.height


class ObjectDetection(BaseModel):
    """A detected object in an image."""

    label: str
    category: ObjectCategory
    confidence: float = Field(ge=0.0, le=1.0)
    bbox: BoundingBox
    attributes: list[str] = Field(default_factory=list)


class SpatialRelationship(BaseModel):
    """Spatial relationship between two objects."""

    subject: str
    relation: SpatialRelation
    reference: str


class ImageScene(BaseModel):
    """Complete scene information for an image."""

    width: int = 0
    height: int = 0
    objects: list[ObjectDetection] = Field(default_factory=list)
    relationships: list[SpatialRelationship] = Field(default_factory=list)
    atmosphere: list[Atmosphere] = Field(default_factory=list)
    scene_type: str = ""


class SceneDescription(BaseModel):
    """Multi-layered scene description for accessibility."""

    overview: str = ""
    object_descriptions: list[str] = Field(default_factory=list)
    spatial_description: str = ""
    atmosphere_description: str = ""
    alt_text: str = ""
    detailed_narrative: str = ""
    navigation_hints: list[str] = Field(default_factory=list)


class DescriptionLevel(str, Enum):
    BRIEF = "brief"
    STANDARD = "standard"
    DETAILED = "detailed"
