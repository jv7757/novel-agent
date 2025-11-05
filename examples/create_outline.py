#!/usr/bin/env python3
"""
Example: Create a detailed story outline

This example shows how to create a comprehensive story outline
without writing the full novel.
"""

import sys
from pathlib import Path
import json

# Add parent directory to path to import novel_agent
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from novel_agent.agent import NovelWritingAgent
from novel_agent.config import AgentConfig


def main():
    """Create a story outline example"""

    # Initialize the agent
    print("Initializing Novel Writing Agent...")
    agent = NovelWritingAgent()

    # Define story parameters
    genre = "fantasy"
    premise = "A young librarian discovers she can enter the worlds of the books she reads, but each visit changes the stories forever."
    themes = ["power of stories", "responsibility", "reality vs fiction"]
    num_chapters = 12

    print(f"\nCreating story outline...")
    print(f"Genre: {genre}")
    print(f"Premise: {premise}\n")

    # Create the outline
    outline = agent.create_story_outline(
        genre=genre,
        premise=premise,
        themes=themes,
        num_chapters=num_chapters
    )

    # Display the outline
    print(f"\n{'='*60}")
    print(f"Story Outline Created!")
    print(f"{'='*60}\n")

    print(f"Title: {outline.title}")
    print(f"Genre: {outline.genre}")
    print(f"\nPremise:")
    print(f"{outline.premise}\n")

    print(f"Setting:")
    print(f"{outline.setting}\n")

    print(f"Themes:")
    for theme in outline.themes:
        print(f"  - {theme}")

    print(f"\nMain Characters:")
    for char in outline.characters:
        print(f"\n  {char.name} ({char.role})")
        print(f"  Description: {char.description}")
        if char.personality:
            print(f"  Personality: {char.personality}")
        if char.motivations:
            print(f"  Motivations: {char.motivations}")

    print(f"\nPlot Points:")
    for i, point in enumerate(outline.plot_points, 1):
        print(f"  {i}. {point}")

    # Save outline to JSON
    output_file = Path("story_outline.json")
    with open(output_file, "w") as f:
        json.dump(outline.model_dump(), f, indent=2)

    print(f"\n{'='*60}")
    print(f"Outline saved to: {output_file}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
