#!/usr/bin/env python3
"""
Example: Create detailed characters

This example shows how to create individual characters
with rich backstories and motivations.
"""

import sys
from pathlib import Path

# Add parent directory to path to import novel_agent
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from novel_agent.agent import NovelWritingAgent


def main():
    """Create characters example"""

    # Initialize the agent
    print("Initializing Novel Writing Agent...\n")
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

    print("Creating characters for a cyberpunk thriller...\n")
    print(f"Story Context: {story_context.strip()}\n")
    print(f"{'='*60}\n")

    created_characters = []

    for name, role, description in characters_to_create:
        print(f"Creating: {name} ({role})...")

        character = agent.create_character(
            name=name,
            role=role,
            story_context=f"{story_context}\nCharacter concept: {description}"
        )

        created_characters.append(character)
        print(f"✓ Created!\n")

    # Display all characters
    print(f"\n{'='*60}")
    print("Characters Created:")
    print(f"{'='*60}\n")

    for char in created_characters:
        print(f"\n{char.name} ({char.role.upper()})")
        print(f"{'-'*40}")
        print(f"\nDescription:")
        print(f"{char.description}\n")

        if char.personality:
            print(f"Personality:")
            print(f"{char.personality}\n")

        if char.background:
            print(f"Background:")
            print(f"{char.background}\n")

        if char.motivations:
            print(f"Motivations:")
            print(f"{char.motivations}\n")

        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
