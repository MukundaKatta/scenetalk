"""Tests for spatial analysis."""

from scenetalk.describer.spatial import SpatialAnalyzer
from scenetalk.models import ObjectDetection, ObjectCategory, BoundingBox, SpatialRelation


def _make_obj(label: str, x: float, y: float, w: float = 0.1, h: float = 0.1) -> ObjectDetection:
    return ObjectDetection(
        label=label,
        category=ObjectCategory.OTHER,
        confidence=0.9,
        bbox=BoundingBox(x=x, y=y, width=w, height=h),
    )


def test_left_right_relation():
    a = _make_obj("cup", 0.1, 0.5)
    b = _make_obj("bottle", 0.8, 0.5)
    rels = SpatialAnalyzer().analyze([a, b])
    assert len(rels) == 1
    assert rels[0].relation == SpatialRelation.LEFT_OF


def test_above_below_relation():
    a = _make_obj("bird", 0.5, 0.1)
    b = _make_obj("cat", 0.5, 0.8)
    rels = SpatialAnalyzer().analyze([a, b])
    assert rels[0].relation == SpatialRelation.ABOVE


def test_describe_position():
    obj = _make_obj("lamp", 0.8, 0.1, 0.05, 0.05)
    desc = SpatialAnalyzer().describe_position(obj)
    assert "right" in desc.lower()
    assert "top" in desc.lower()


def test_describe_layout():
    objects = [_make_obj("dog", 0.1, 0.5), _make_obj("cat", 0.8, 0.5)]
    layout = SpatialAnalyzer().describe_layout(objects)
    assert "dog" in layout
    assert "cat" in layout


def test_empty_layout():
    layout = SpatialAnalyzer().describe_layout([])
    assert "empty" in layout.lower()
