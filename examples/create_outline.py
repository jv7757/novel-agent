#!/usr/bin/env python3
"""
Example: Create a detailed story outline using Claude Agent SDK

This example shows how to create a comprehensive story outline
without writing the full novel.
"""

import sys
import anyio
from pathlib import Path

# Add parent directory to path to import novel_agent
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from novel_agent.agent import NovelWritingAgent
from novel_agent.config import AgentConfig


async def main():
    """Create a story outline example"""

    # Initialize the agent
    print("Initializing Novel Writing Agent with Claude Agent SDK...")
    print()

    agent = NovelWritingAgent()

    # Define story parameters
    genre = "fantasy"
    premise = "A young librarian discovers she can enter the worlds of the books she reads, but each visit changes the stories forever."
    themes = ["power of stories", "responsibility", "reality vs fiction"]
    num_chapters = 12

    print(f"Creating story outline...")
    print(f"Genre: {genre}")
    print(f"Premise: {premise}")
    print(f"Themes: {', '.join(themes)}")
    print(f"Target Chapters: {num_chapters}")
    print()
    print("="*60)
    print()

    # Create the outline using the agent
    # The agent will use the create_story_outline tool
    result = await agent.create_story_outline(
        genre=genre,
        premise=premise,
        themes=themes,
        num_chapters=num_chapters
    )

    print()
    print("="*60)
    print("Story outline creation completed!")
    print("="*60)
    print()


if __name__ == "__main__":
    anyio.run(main)
