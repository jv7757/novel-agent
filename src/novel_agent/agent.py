"""
Novel Writing Agent using Claude Agent SDK
"""

import json
import anyio
from pathlib import Path
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from claude_agent_sdk import (
    query,
    create_sdk_mcp_server,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)

from .config import AgentConfig
from .models import Character, StoryOutline, Chapter, Novel
from .tools.story_tools import NOVEL_WRITING_TOOLS

console = Console()


class NovelWritingAgent:
    """
    An intelligent agent for creative novel writing using Claude Agent SDK.

    This agent leverages Claude's advanced capabilities through custom tools:
    - Generate story outlines with plot structure and themes
    - Create compelling characters with depth
    - Write chapters with narrative continuity
    - Save and manage novel content
    - Provide writing tips and guidance
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize the Novel Writing Agent"""
        self.config = config or AgentConfig()
        self.current_novel: Optional[Novel] = None

        # Create MCP server with custom tools
        self.mcp_server = create_sdk_mcp_server(
            name="novel-writing-tools",
            version="1.0.0",
            tools=NOVEL_WRITING_TOOLS,
        )

        # Configure agent options
        self.agent_options = ClaudeAgentOptions(
            system_prompt=self._get_system_prompt(),
            mcp_servers={"novel-writing": self.mcp_server},
            allowed_tools=[
                "create_story_outline",
                "create_character",
                "write_chapter",
                "save_story_content",
                "get_writing_tips",
            ],
            max_turns=50,  # Allow longer conversations for novel creation
        )

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the novel writing agent"""
        return """You are an expert novelist and creative writing assistant. You help users create compelling novels with:

- Rich, multi-dimensional characters
- Engaging plot structures
- Vivid descriptions and natural dialogue
- Strong narrative pacing
- Thematic depth

When creating novels:
1. Start by understanding the user's vision (genre, premise, themes)
2. Create a comprehensive outline with plot points and characters
3. Write each chapter with care, maintaining consistency
4. Use literary techniques like showing vs telling, sensory details, and subtext
5. Ensure each chapter ends with a hook to keep readers engaged

You have access to specialized tools for:
- create_story_outline: Generate complete story structures
- create_character: Develop detailed characters
- write_chapter: Write full chapters with narrative flow
- save_story_content: Save work to files
- get_writing_tips: Get writing guidance

Always strive for quality over quantity. Make every word count."""

    async def create_novel(
        self,
        genre: str,
        premise: str,
        num_chapters: int = 5,
        themes: Optional[List[str]] = None,
    ) -> str:
        """
        Create a complete novel using the agent.

        Args:
            genre: The genre of the novel
            premise: The premise or concept
            num_chapters: Number of chapters to write
            themes: List of themes to explore

        Returns:
            Path to the saved novel file
        """
        console.print(f"[bold magenta]Starting novel creation with Claude Agent SDK...[/bold magenta]\n")

        themes_str = ", ".join(themes) if themes else "exploration, conflict, growth"

        prompt = f"""I want to write a {genre} novel. Here are the details:

Premise: {premise}
Number of Chapters: {num_chapters}
Themes: {themes_str}

Please help me create this novel by:
1. First, create a detailed story outline using the create_story_outline tool
2. Then, write all {num_chapters} chapters one by one using the write_chapter tool
3. Finally, save the complete novel to a file using save_story_content tool

Let's create something amazing!"""

        result_text = []
        total_cost = 0.0

        console.print("[bold blue]Querying Claude Agent...[/bold blue]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Creating novel...", total=None)

            async for message in query(prompt=prompt, options=self.agent_options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            console.print(f"[cyan]{block.text}[/cyan]\n")
                            result_text.append(block.text)

                elif isinstance(message, ResultMessage):
                    if message.total_cost_usd > 0:
                        total_cost = message.total_cost_usd
                        console.print(f"[yellow]Cost: ${total_cost:.4f}[/yellow]")

            progress.update(task, completed=True)

        console.print(f"\n[bold green]✓ Novel creation complete![/bold green]")
        console.print(f"[bold green]Total cost: ${total_cost:.4f}[/bold green]\n")

        return "\n".join(result_text)

    async def create_story_outline(
        self,
        genre: str,
        premise: str,
        themes: Optional[List[str]] = None,
        num_chapters: int = 10,
    ) -> str:
        """
        Create a comprehensive story outline.

        Args:
            genre: The genre of the story
            premise: The basic premise
            themes: List of themes
            num_chapters: Target number of chapters

        Returns:
            The outline as text
        """
        console.print(f"[bold blue]Creating story outline for {genre} novel...[/bold blue]\n")

        themes_str = ", ".join(themes) if themes else ""

        prompt = f"""Create a detailed story outline for a {genre} novel with:

Premise: {premise}
Themes: {themes_str}
Number of Chapters: {num_chapters}

Use the create_story_outline tool to generate a comprehensive outline with characters, plot points, and story structure."""

        result_text = []

        async for message in query(prompt=prompt, options=self.agent_options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        console.print(f"[cyan]{block.text}[/cyan]\n")
                        result_text.append(block.text)

        return "\n".join(result_text)

    async def create_character(
        self,
        name: str,
        role: str,
        story_context: str = "",
    ) -> str:
        """
        Create a detailed character.

        Args:
            name: Character's name
            role: Character's role (main, supporting, minor)
            story_context: Context about the story

        Returns:
            Character description as text
        """
        console.print(f"[bold blue]Creating character: {name}...[/bold blue]\n")

        prompt = f"""Create a detailed character named "{name}" with the role "{role}".

Story Context: {story_context}

Use the create_character tool to generate a complete character profile with background, personality, and motivations."""

        result_text = []

        async for message in query(prompt=prompt, options=self.agent_options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        console.print(f"[cyan]{block.text}[/cyan]\n")
                        result_text.append(block.text)

        return "\n".join(result_text)

    async def write_chapter(
        self,
        chapter_number: int,
        chapter_title: str,
        plot_point: str,
        story_context: str = "",
        target_words: int = 2000,
    ) -> str:
        """
        Write a complete chapter.

        Args:
            chapter_number: The chapter number
            chapter_title: The chapter title
            plot_point: The main plot point for this chapter
            story_context: Context about the story
            target_words: Target word count

        Returns:
            The chapter content
        """
        console.print(f"[bold blue]Writing Chapter {chapter_number}: {chapter_title}...[/bold blue]\n")

        prompt = f"""Write Chapter {chapter_number} titled "{chapter_title}".

Plot Point: {plot_point}
Story Context: {story_context}
Target Length: {target_words} words

Use the write_chapter tool to create an engaging chapter with vivid descriptions, natural dialogue, and strong pacing."""

        result_text = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Writing chapter {chapter_number}...", total=None)

            async for message in query(prompt=prompt, options=self.agent_options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            console.print(f"[cyan]{block.text}[/cyan]\n")
                            result_text.append(block.text)

            progress.update(task, completed=True)

        return "\n".join(result_text)

    async def interactive_mode(self):
        """Start an interactive writing session"""
        console.print("[bold magenta]Welcome to Novel Writing Agent - Interactive Mode[/bold magenta]\n")
        console.print("Commands:")
        console.print("  'outline' - Create a new story outline")
        console.print("  'chapter' - Write a chapter")
        console.print("  'character' - Create a character")
        console.print("  'novel' - Create a complete novel")
        console.print("  'tips' - Get writing tips")
        console.print("  'custom' - Send a custom prompt")
        console.print("  'exit' - Exit interactive mode\n")

        while True:
            try:
                command = console.input("[bold cyan]> [/bold cyan]").strip().lower()

                if command == "exit":
                    console.print("[bold yellow]Goodbye![/bold yellow]")
                    break

                elif command == "outline":
                    genre = console.input("Genre: ")
                    premise = console.input("Premise: ")
                    num_chapters = int(console.input("Number of chapters (default 10): ") or "10")
                    themes_input = console.input("Themes (comma-separated): ")
                    themes = [t.strip() for t in themes_input.split(",") if t.strip()] if themes_input else None

                    await self.create_story_outline(genre, premise, themes, num_chapters)

                elif command == "character":
                    name = console.input("Character name: ")
                    role = console.input("Role (main/supporting/minor): ")
                    context = console.input("Story context: ")

                    await self.create_character(name, role, context)

                elif command == "novel":
                    genre = console.input("Genre: ")
                    premise = console.input("Premise: ")
                    num_chapters = int(console.input("Number of chapters (default 5): ") or "5")
                    themes_input = console.input("Themes (comma-separated): ")
                    themes = [t.strip() for t in themes_input.split(",") if t.strip()] if themes_input else None

                    await self.create_novel(genre, premise, num_chapters, themes)

                elif command == "tips":
                    topic = console.input("Topic (dialogue/description/plot/character/pacing): ")
                    prompt = f"Please use the get_writing_tips tool to get tips about: {topic}"

                    async for message in query(prompt=prompt, options=self.agent_options):
                        if isinstance(message, AssistantMessage):
                            for block in message.content:
                                if isinstance(block, TextBlock):
                                    console.print(f"[cyan]{block.text}[/cyan]\n")

                elif command == "custom":
                    custom_prompt = console.input("Enter your prompt: ")

                    async for message in query(prompt=custom_prompt, options=self.agent_options):
                        if isinstance(message, AssistantMessage):
                            for block in message.content:
                                if isinstance(block, TextBlock):
                                    console.print(f"[cyan]{block.text}[/cyan]\n")

                else:
                    console.print(f"[red]Unknown command: {command}[/red]")

            except KeyboardInterrupt:
                console.print("\n[bold yellow]Interrupted. Type 'exit' to quit.[/bold yellow]")
            except Exception as e:
                console.print(f"[bold red]Error: {e}[/bold red]")
                import traceback
                traceback.print_exc()


def run_novel_agent():
    """Convenience function to run the agent"""
    agent = NovelWritingAgent()
    return agent
