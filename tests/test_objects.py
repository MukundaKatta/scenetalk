"""Tests for object detection."""

import torch

from scenetalk.describer.objects import ObjectDetector, SimpleCNN


def test_cnn_forward_pass():
    model = SimpleCNN(num_classes=10)
    x = torch.randn(1, 3, 64, 64)
    out = model(x)
    assert out.shape == (1, 10)


def test_detect_from_objects():
    detector = ObjectDetector()
    objects = [
        {"label": "dog", "confidence": 0.95, "bbox": {"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.3}},
        {"label": "cat", "confidence": 0.88, "bbox": {"x": 0.5, "y": 0.5, "width": 0.2, "height": 0.2}},
    ]
    detections = detector.detect_from_objects(objects)
    assert len(detections) == 2
    assert detections[0].label == "dog"
    assert detections[0].confidence == 0.95


def test_detect_from_tensor():
    detector = ObjectDetector()
    image = torch.randn(1, 3, 64, 64)
    detections = detector.detect_from_tensor(image, threshold=0.0)
    # Should return up to 10 detections
    assert len(detections) <= 10
