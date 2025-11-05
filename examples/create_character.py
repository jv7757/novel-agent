#!/usr/bin/env python3
"""
Example: Create detailed characters using Claude Agent SDK

This example shows how to create individual characters
with rich backstories and motivations.
"""

import sys
import anyio
from pathlib import Path

# Add parent directory to path to import novel_agent
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from novel_agent.agent import NovelWritingAgent


async def main():
    """Create characters example"""

    # Initialize the agent
    print("Initializing Novel Writing Agent with Claude Agent SDK...")
    print()

    agent = NovelWritingAgent()

    # Story context for character creation
    story_context = """
    A cyberpunk thriller set in Neo-Tokyo, 2089.
    Corporations control everything, and hackers fight for freedom in the digital realm.
    """

    # Create multiple characters
    characters_to_create = [
        ("Alex Chen", "main", "A brilliant hacker seeking revenge for their murdered sibling"),
        ("Dr. Sarah Kimura", "supporting", "A rogue AI researcher who holds the key to bringing down the corporations"),
        ("Viktor Volkov", "supporting", "A corporate security chief torn between duty and conscience"),
    ]

    print("Creating characters for a cyberpunk thriller...")
    print(f"Story Context: {story_context.strip()}")
    print()
    print("="*60)
    print()

    for name, role, description in characters_to_create:
        print(f"Creating: {name} ({role})...")
        print(f"Concept: {description}")
        print()

        # Use the agent's create_character method
        # The agent will use the create_character tool
        result = await agent.create_character(
            name=name,
            role=role,
            story_context=f"{story_context}\nCharacter concept: {description}"
        )

        print()
        print("="*60)
        print()

    print("All characters created!")
    print("="*60)
    print()


if __name__ == "__main__":
    anyio.run(main)
