"""
Custom tools for the Novel Writing Agent using claude-agent-sdk
"""

import json
from typing import Dict, Any, List, Optional
from claude_agent_sdk import tool
from ..models import Character, StoryOutline, Chapter


# Global state to track the current novel being created
_current_outline: Optional[StoryOutline] = None
_current_chapters: List[Chapter] = []


@tool(
    "create_story_outline",
    "Create a comprehensive story outline with plot structure, characters, and themes",
    {
        "genre": str,
        "premise": str,
        "themes": str,  # comma-separated
        "num_chapters": int,
    }
)
async def create_story_outline_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a detailed story outline for a novel.

    This tool generates:
    - A compelling title
    - Detailed setting description
    - Main characters with roles and descriptions
    - Major plot points for each chapter
    - Key themes to explore

    Returns a JSON structure with all story elements.
    """
    global _current_outline

    genre = args["genre"]
    premise = args["premise"]
    themes_str = args.get("themes", "")
    num_chapters = args.get("num_chapters", 10)

    themes = [t.strip() for t in themes_str.split(",")] if themes_str else []

    # Build the prompt for outline creation
    prompt = f"""Create a detailed story outline with these specifications:

Genre: {genre}
Premise: {premise}
Themes: {', '.join(themes) if themes else 'Not specified'}
Target Chapters: {num_chapters}

Please provide a complete outline in JSON format with:
1. title - A compelling story title
2. genre - The genre
3. premise - An expanded premise (2-3 sentences)
4. setting - Detailed setting description
5. themes - List of themes to explore
6. characters - List of 3-5 main characters, each with:
   - name: Character name
   - role: "main", "supporting", or "minor"
   - description: Physical and personality description
   - personality: Detailed personality traits
   - background: Background story
   - motivations: Character motivations and goals
7. plot_points - List of {num_chapters} major plot points, one for each chapter

Format your response as a valid JSON object."""

    # Return a prompt for Claude to execute
    return {
        "content": [
            {
                "type": "text",
                "text": f"""I need to create a story outline. Please generate a detailed outline with the following structure in JSON format:

{prompt}

Make it creative, engaging, and well-structured."""
            }
        ]
    }


@tool(
    "create_character",
    "Create a detailed character with background, personality, and motivations",
    {
        "name": str,
        "role": str,  # main, supporting, minor
        "story_context": str,
    }
)
async def create_character_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a deep, multi-dimensional character for the story.

    Generates:
    - Physical and personality description
    - Background story
    - Motivations and goals
    - Personality traits and quirks
    """
    name = args["name"]
    role = args["role"]
    story_context = args.get("story_context", "")

    prompt = f"""Create a detailed character with these details:

Name: {name}
Role: {role}
Story Context: {story_context}

Please provide a complete character profile in JSON format with:
- name: "{name}"
- role: "{role}"
- description: Physical appearance and personality overview
- personality: Detailed personality traits, quirks, and mannerisms
- background: Complete background story explaining their past
- motivations: What drives them, their goals and desires

Make the character feel real, complex, and interesting. Include specific details that make them memorable."""

    return {
        "content": [
            {
                "type": "text",
                "text": f"""I need to create a character for my story. Please generate:

{prompt}

Provide the response as a valid JSON object."""
            }
        ]
    }


@tool(
    "write_chapter",
    "Write a complete chapter of the novel with engaging narrative",
    {
        "chapter_number": int,
        "chapter_title": str,
        "plot_point": str,
        "story_context": str,
        "target_words": int,
    }
)
async def write_chapter_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Write a complete chapter with vivid descriptions, dialogue, and plot progression.

    The chapter will:
    - Advance the plot meaningfully
    - Develop characters through actions and interactions
    - Include engaging dialogue and descriptions
    - Maintain narrative consistency
    - End with a hook for the next chapter
    """
    chapter_number = args["chapter_number"]
    chapter_title = args["chapter_title"]
    plot_point = args["plot_point"]
    story_context = args.get("story_context", "")
    target_words = args.get("target_words", 2000)

    prompt = f"""Write Chapter {chapter_number}: {chapter_title}

Story Context:
{story_context}

This Chapter's Plot Point:
{plot_point}

Requirements:
- Target length: approximately {target_words} words
- Include vivid descriptions and sensory details
- Write engaging, natural dialogue
- Show character development through actions
- Maintain the story's tone and pacing
- End with a compelling hook for the next chapter

Write the complete chapter now. Focus on showing rather than telling, and make the reader feel immersed in the story."""

    return {
        "content": [
            {
                "type": "text",
                "text": f"""Please write this chapter:

{prompt}

Write it in a literary style with proper narrative flow."""
            }
        ]
    }


@tool(
    "save_story_content",
    "Save story content (outline, chapter, or complete novel) to a file",
    {
        "filename": str,
        "content": str,
        "content_type": str,  # "outline", "chapter", "novel"
    }
)
async def save_story_content_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save story content to a file in the generated_stories directory.
    """
    import os
    from pathlib import Path

    filename = args["filename"]
    content = args["content"]
    content_type = args.get("content_type", "novel")

    # Ensure output directory exists
    output_dir = Path("generated_stories")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create filepath
    filepath = output_dir / filename

    # Write content
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "content": [
            {
                "type": "text",
                "text": f"Successfully saved {content_type} to {filepath}"
            }
        ]
    }


@tool(
    "get_writing_tips",
    "Get writing tips and guidance for creative writing",
    {
        "topic": str,  # e.g., "dialogue", "description", "plot", "character"
    }
)
async def get_writing_tips_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Provide writing tips and best practices for novel writing.
    """
    topic = args["topic"]

    tips_db = {
        "dialogue": """
Tips for Writing Great Dialogue:
1. Make it sound natural - people interrupt, use contractions, and don't speak in perfect sentences
2. Use subtext - characters often don't say exactly what they mean
3. Give each character a unique voice
4. Avoid exposition dumps - don't use dialogue just to convey information
5. Include action beats between dialogue to show emotion and movement
        """,
        "description": """
Tips for Vivid Descriptions:
1. Use specific, concrete details rather than general statements
2. Engage all five senses, not just sight
3. Choose strong, precise verbs and nouns over adjectives and adverbs
4. Show through action and detail rather than telling
5. Use metaphors and similes that fit the story's tone
6. Don't over-describe - select the most important details
        """,
        "plot": """
Tips for Strong Plot Development:
1. Start with conflict - every scene needs tension
2. Raise the stakes progressively
3. Use cause and effect - each event should lead to the next
4. Include setbacks and complications
5. Build to a satisfying climax
6. Tie up loose ends but leave some mystery
        """,
        "character": """
Tips for Character Development:
1. Give characters clear motivations and goals
2. Create internal conflicts, not just external ones
3. Show growth and change over the story
4. Use specific details to make characters memorable
5. Reveal character through actions, not just description
6. Make characters flawed and relatable
        """,
        "pacing": """
Tips for Good Pacing:
1. Vary sentence and paragraph length
2. Balance action scenes with quieter moments
3. End chapters with hooks to keep readers engaged
4. Cut unnecessary scenes that don't advance plot or character
5. Use shorter sentences for tension, longer for reflection
        """
    }

    tips = tips_db.get(topic.lower(), f"No specific tips found for '{topic}'. Try: dialogue, description, plot, character, or pacing.")

    return {
        "content": [
            {
                "type": "text",
                "text": tips
            }
        ]
    }


# Export all tools
NOVEL_WRITING_TOOLS = [
    create_story_outline_tool,
    create_character_tool,
    write_chapter_tool,
    save_story_content_tool,
    get_writing_tips_tool,
]
