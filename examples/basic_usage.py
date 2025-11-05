#!/usr/bin/env python3
"""
Basic usage example for the Novel Writing Agent with Claude Agent SDK

This example demonstrates how to:
1. Initialize the agent with custom tools
2. Create a complete novel using the agent
3. Leverage Claude Agent SDK's capabilities
"""

import sys
import anyio
from pathlib import Path

# Add parent directory to path to import novel_agent
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from novel_agent.agent import NovelWritingAgent
from novel_agent.config import AgentConfig


async def main():
    """Basic usage example"""

    # Initialize the agent
    print("Initializing Novel Writing Agent with Claude Agent SDK...")
    print("This agent uses custom tools via MCP server for novel writing.\n")

    config = AgentConfig()
    agent = NovelWritingAgent(config)

    # Define the story parameters
    genre = "science fiction"
    premise = "In the year 2157, humanity discovers an ancient alien artifact on Mars that contains a message about Earth's future."
    themes = ["exploration", "first contact", "humanity's destiny"]
    num_chapters = 3  # Short story for demonstration

    print(f"Creating a {genre} novel...")
    print(f"Premise: {premise}")
    print(f"Themes: {', '.join(themes)}")
    print(f"Chapters: {num_chapters}\n")
    print("="*60)
    print()

    # Create the complete novel using the agent
    # The agent will use its tools to:
    # 1. Create a story outline
    # 2. Write each chapter
    # 3. Save the novel to a file
    result = await agent.create_novel(
        genre=genre,
        premise=premise,
        num_chapters=num_chapters,
        themes=themes
    )

    print("\n" + "="*60)
    print("Novel creation process completed!")
    print("Check the generated_stories/ directory for your novel.")
    print("="*60 + "\n")


if __name__ == "__main__":
    anyio.run(main)
