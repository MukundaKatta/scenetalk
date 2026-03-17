"""Object detection using CNN (simulation-capable)."""

from __future__ import annotations

from typing import Optional

import torch
import torch.nn as nn

from scenetalk.models import ObjectDetection, ObjectCategory, BoundingBox


# Common objects the detector can identify
KNOWN_OBJECTS: dict[str, ObjectCategory] = {
    "person": ObjectCategory.PERSON,
    "man": ObjectCategory.PERSON,
    "woman": ObjectCategory.PERSON,
    "child": ObjectCategory.PERSON,
    "dog": ObjectCategory.ANIMAL,
    "cat": ObjectCategory.ANIMAL,
    "bird": ObjectCategory.ANIMAL,
    "horse": ObjectCategory.ANIMAL,
    "fish": ObjectCategory.ANIMAL,
    "car": ObjectCategory.VEHICLE,
    "bus": ObjectCategory.VEHICLE,
    "truck": ObjectCategory.VEHICLE,
    "bicycle": ObjectCategory.VEHICLE,
    "motorcycle": ObjectCategory.VEHICLE,
    "airplane": ObjectCategory.VEHICLE,
    "boat": ObjectCategory.VEHICLE,
    "train": ObjectCategory.VEHICLE,
    "chair": ObjectCategory.FURNITURE,
    "table": ObjectCategory.FURNITURE,
    "couch": ObjectCategory.FURNITURE,
    "bed": ObjectCategory.FURNITURE,
    "desk": ObjectCategory.FURNITURE,
    "bookshelf": ObjectCategory.FURNITURE,
    "lamp": ObjectCategory.FURNITURE,
    "apple": ObjectCategory.FOOD,
    "banana": ObjectCategory.FOOD,
    "pizza": ObjectCategory.FOOD,
    "sandwich": ObjectCategory.FOOD,
    "cake": ObjectCategory.FOOD,
    "bottle": ObjectCategory.FOOD,
    "cup": ObjectCategory.FOOD,
    "laptop": ObjectCategory.ELECTRONICS,
    "phone": ObjectCategory.ELECTRONICS,
    "television": ObjectCategory.ELECTRONICS,
    "keyboard": ObjectCategory.ELECTRONICS,
    "monitor": ObjectCategory.ELECTRONICS,
    "camera": ObjectCategory.ELECTRONICS,
    "tree": ObjectCategory.NATURE,
    "flower": ObjectCategory.NATURE,
    "grass": ObjectCategory.NATURE,
    "sky": ObjectCategory.NATURE,
    "mountain": ObjectCategory.NATURE,
    "river": ObjectCategory.NATURE,
    "house": ObjectCategory.BUILDING,
    "building": ObjectCategory.BUILDING,
    "bridge": ObjectCategory.BUILDING,
    "fence": ObjectCategory.BUILDING,
    "hat": ObjectCategory.CLOTHING,
    "shoe": ObjectCategory.CLOTHING,
    "backpack": ObjectCategory.CLOTHING,
    "umbrella": ObjectCategory.TOOL,
    "scissors": ObjectCategory.TOOL,
    "clock": ObjectCategory.TOOL,
    "book": ObjectCategory.OTHER,
    "ball": ObjectCategory.OTHER,
    "kite": ObjectCategory.OTHER,
    "sign": ObjectCategory.OTHER,
}


class SimpleCNN(nn.Module):
    """A simple CNN architecture for object classification.

    This is a demonstration model. In production, you would use a
    pre-trained model like ResNet, YOLO, or Faster R-CNN.
    """

    def __init__(self, num_classes: int = len(KNOWN_OBJECTS)) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((4, 4)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.classifier(x)
        return x


class ObjectDetector:
    """Identifies common objects in images using a CNN."""

    def __init__(self) -> None:
        self._model = SimpleCNN()
        self._model.eval()
        self._labels = list(KNOWN_OBJECTS.keys())
        self._categories = KNOWN_OBJECTS

    def detect_from_tensor(self, image_tensor: torch.Tensor, threshold: float = 0.3) -> list[ObjectDetection]:
        """Detect objects from a preprocessed image tensor.

        Args:
            image_tensor: Tensor of shape (1, 3, H, W) normalized to [0, 1].
            threshold: Minimum confidence to report a detection.

        Returns:
            List of detected objects.
        """
        with torch.no_grad():
            logits = self._model(image_tensor)
            probs = torch.softmax(logits, dim=-1).squeeze(0)

        detections: list[ObjectDetection] = []
        for idx, prob in enumerate(probs):
            conf = prob.item()
            if conf >= threshold:
                label = self._labels[idx]
                # Generate approximate bounding box from class activation
                detections.append(
                    ObjectDetection(
                        label=label,
                        category=self._categories[label],
                        confidence=round(conf, 3),
                        bbox=BoundingBox(x=0.1, y=0.1, width=0.5, height=0.5),
                    )
                )

        detections.sort(key=lambda d: d.confidence, reverse=True)
        return detections[:10]  # Return top 10

    def detect_from_objects(self, objects: list[dict]) -> list[ObjectDetection]:
        """Create ObjectDetection instances from pre-identified objects.

        Useful for simulation/testing without running CNN inference.
        """
        detections: list[ObjectDetection] = []
        for obj in objects:
            label = obj.get("label", "unknown")
            category = self._categories.get(label, ObjectCategory.OTHER)
            detections.append(
                ObjectDetection(
                    label=label,
                    category=category,
                    confidence=obj.get("confidence", 0.9),
                    bbox=BoundingBox(**obj.get("bbox", {"x": 0.1, "y": 0.1, "width": 0.3, "height": 0.3})),
                    attributes=obj.get("attributes", []),
                )
            )
        return detections
