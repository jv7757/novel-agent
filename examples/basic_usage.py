#!/usr/bin/env python3
"""
Basic usage example for the Novel Writing Agent

This example demonstrates how to:
1. Create a story outline
2. Write individual chapters
3. Save the complete novel
"""

import sys
from pathlib import Path

# Add parent directory to path to import novel_agent
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from novel_agent.agent import NovelWritingAgent
from novel_agent.config import AgentConfig


def main():
    """Basic usage example"""

    # Initialize the agent
    print("Initializing Novel Writing Agent...")
    config = AgentConfig()
    agent = NovelWritingAgent(config)

    # Define the story parameters
    genre = "science fiction"
    premise = "In the year 2157, humanity discovers an ancient alien artifact on Mars that contains a message about Earth's future."
    themes = ["exploration", "first contact", "humanity's destiny"]
    num_chapters = 3  # Short story for demonstration

    print(f"\nCreating a {genre} novel...")
    print(f"Premise: {premise}")
    print(f"Themes: {', '.join(themes)}")
    print(f"Chapters: {num_chapters}\n")

    # Create the complete novel
    novel = agent.create_novel(
        genre=genre,
        premise=premise,
        num_chapters=num_chapters,
        themes=themes
    )

    # Save the novel
    filepath = agent.save_novel(novel)

    print(f"\n{'='*60}")
    print(f"Novel created successfully!")
    print(f"Title: {novel.outline.title}")
    print(f"Chapters: {len(novel.chapters)}")
    print(f"Total words: {novel.total_word_count}")
    print(f"Saved to: {filepath}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
