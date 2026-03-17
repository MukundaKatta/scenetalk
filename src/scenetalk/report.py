"""Rich console report for SceneTalk."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from scenetalk.models import ImageScene, SceneDescription


def print_report(
    scene: ImageScene,
    description: SceneDescription,
    console: Console | None = None,
) -> None:
    """Print a formatted scene description report."""
    console = console or Console()

    console.print(Panel("[bold]SceneTalk - Scene Description Report[/bold]", style="blue"))

    # Alt text
    if description.alt_text:
        console.print(Panel(description.alt_text, title="Alt Text", style="green"))

    # Overview
    if description.overview:
        console.print(f"\n[bold]Overview:[/bold] {description.overview}")

    # Objects table
    if scene.objects:
        table = Table(title="Detected Objects", show_lines=True)
        table.add_column("Object", style="cyan")
        table.add_column("Category", style="magenta")
        table.add_column("Confidence", justify="right")
        table.add_column("Position")
        for obj in scene.objects:
            pos = f"({obj.bbox.center_x:.1f}, {obj.bbox.center_y:.1f})"
            table.add_row(obj.label, obj.category.value, f"{obj.confidence:.0%}", pos)
        console.print(table)

    # Object descriptions
    if description.object_descriptions:
        console.print("\n[bold]Object Details:[/bold]")
        for desc in description.object_descriptions:
            console.print(f"  {desc}")

    # Spatial description
    if description.spatial_description:
        console.print(f"\n[bold]Layout:[/bold] {description.spatial_description}")

    # Atmosphere
    if description.atmosphere_description:
        console.print(f"\n[bold]Atmosphere:[/bold] {description.atmosphere_description}")

    # Navigation hints
    if description.navigation_hints:
        console.print("\n[bold]Navigation Hints:[/bold]")
        for hint in description.navigation_hints:
            console.print(f"  [yellow]*[/yellow] {hint}")

    # Full narrative
    if description.detailed_narrative:
        console.print(Panel(description.detailed_narrative, title="Full Narrative", style="dim"))
