"""CLI interface for SceneTalk."""

from __future__ import annotations

import click
from rich.console import Console

from scenetalk.models import DescriptionLevel
from scenetalk.simulator import SceneSimulator
from scenetalk.describer.scene import SceneDescriber
from scenetalk.describer.spatial import SpatialAnalyzer
from scenetalk.accessibility.alt_text import AltTextGenerator
from scenetalk.accessibility.detailed import DetailedDescriber
from scenetalk.accessibility.navigation import NavigationHelper
from scenetalk.report import print_report


@click.group()
def main() -> None:
    """SceneTalk - AI Image Describer for Blind Users."""


@main.command()
@click.argument("template", type=click.Choice(SceneSimulator.available_templates()))
@click.option("--level", "-l", type=click.Choice([l.value for l in DescriptionLevel]),
              default="standard", help="Description detail level.")
def describe(template: str, level: str) -> None:
    """Describe a simulated scene."""
    scene = SceneSimulator.from_template(template)
    detail_level = DescriptionLevel(level)

    describer = DetailedDescriber()
    nav = NavigationHelper()

    description = describer.describe(scene, detail_level)
    description.navigation_hints = nav.generate_navigation_hints(scene)

    # Compute relationships
    spatial = SpatialAnalyzer()
    scene.relationships = spatial.analyze(scene.objects)

    print_report(scene, description)


@main.command()
def templates() -> None:
    """List available scene templates."""
    console = Console()
    console.print("[bold]Available scene templates:[/bold]")
    for name in SceneSimulator.available_templates():
        console.print(f"  - {name}")


@main.command()
@click.argument("template", type=click.Choice(SceneSimulator.available_templates()))
def alt_text(template: str) -> None:
    """Generate just alt text for a simulated scene."""
    scene = SceneSimulator.from_template(template)
    text = AltTextGenerator().generate(scene)
    click.echo(text)


if __name__ == "__main__":
    main()
