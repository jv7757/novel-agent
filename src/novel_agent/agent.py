import json
from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import AgentConfig
from .models import Character, StoryOutline, Chapter, Novel

console = Console()


class NovelWritingAgent:
    """
    An intelligent agent for creative novel writing using Claude.

    This agent can:
    - Generate story outlines and plot structures
    - Create compelling characters with depth
    - Write chapters and scenes
    - Edit and refine content
    - Maintain narrative consistency
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize the Novel Writing Agent"""
        self.config = config or AgentConfig()
        self.client = Anthropic(api_key=self.config.api_key)
        self.conversation_history: List[Dict[str, str]] = []
        self.current_novel: Optional[Novel] = None

    def _create_message(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """Create a message using Claude API"""
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=max_tokens or self.config.max_tokens,
            temperature=temperature or self.config.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    def create_story_outline(
        self,
        genre: str,
        premise: str,
        themes: List[str] = None,
        num_chapters: int = 10,
    ) -> StoryOutline:
        """
        Create a comprehensive story outline

        Args:
            genre: The genre of the story (e.g., "fantasy", "sci-fi", "mystery")
            premise: The basic premise or concept of the story
            themes: List of themes to explore in the story
            num_chapters: Target number of chapters

        Returns:
            StoryOutline object with complete story structure
        """
        console.print(f"[bold blue]Creating story outline for {genre} novel...[/bold blue]")

        themes = themes or []
        system_prompt = """You are an expert story architect and novelist. Your task is to create
        detailed, compelling story outlines that have strong narrative structure, interesting characters,
        and engaging plot progression. Focus on creating outlines that are both creative and structurally sound."""

        user_message = f"""Create a detailed story outline with the following specifications:

Genre: {genre}
Premise: {premise}
Themes: {', '.join(themes) if themes else 'Not specified'}
Target Chapters: {num_chapters}

Please provide:
1. A compelling title
2. A detailed setting description
3. 3-5 main characters with names, roles, and brief descriptions
4. {num_chapters} major plot points that form the story arc
5. Key themes to explore

Format your response as a JSON object with the following structure:
{{
    "title": "Story Title",
    "genre": "{genre}",
    "premise": "Expanded premise",
    "setting": "Detailed setting description",
    "themes": ["theme1", "theme2", ...],
    "characters": [
        {{
            "name": "Character Name",
            "role": "main/supporting",
            "description": "Character description",
            "personality": "Personality traits",
            "background": "Background story",
            "motivations": "Character motivations"
        }}
    ],
    "plot_points": ["plot point 1", "plot point 2", ...]
}}"""

        response = self._create_message(system_prompt, user_message)

        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1
            json_str = response[start_idx:end_idx]
            outline_data = json.loads(json_str)

            # Create StoryOutline object
            characters = [Character(**char) for char in outline_data.get("characters", [])]
            outline = StoryOutline(
                title=outline_data["title"],
                genre=outline_data["genre"],
                premise=outline_data["premise"],
                setting=outline_data["setting"],
                themes=outline_data.get("themes", []),
                plot_points=outline_data.get("plot_points", []),
                characters=characters,
            )

            console.print(f"[bold green]✓ Created outline: '{outline.title}'[/bold green]")
            return outline

        except (json.JSONDecodeError, KeyError) as e:
            console.print(f"[bold red]Error parsing outline: {e}[/bold red]")
            raise

    def create_character(
        self,
        name: str,
        role: str,
        story_context: str = "",
    ) -> Character:
        """
        Create a detailed character

        Args:
            name: Character's name
            role: Character's role (main, supporting, minor)
            story_context: Context about the story for better character creation

        Returns:
            Character object with full details
        """
        console.print(f"[bold blue]Creating character: {name}...[/bold blue]")

        system_prompt = """You are an expert character designer for novels. Create deep,
        multi-dimensional characters with realistic personalities, compelling backgrounds,
        and clear motivations that drive their actions in the story."""

        user_message = f"""Create a detailed character with the following:

Name: {name}
Role: {role}
Story Context: {story_context}

Provide:
1. A vivid physical and personality description
2. A compelling background story
3. Clear motivations and goals
4. Personality traits and quirks

Format your response as JSON:
{{
    "name": "{name}",
    "role": "{role}",
    "description": "Physical and personality description",
    "personality": "Detailed personality traits",
    "background": "Background story",
    "motivations": "Motivations and goals"
}}"""

        response = self._create_message(system_prompt, user_message)

        try:
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1
            json_str = response[start_idx:end_idx]
            char_data = json.loads(json_str)
            character = Character(**char_data)

            console.print(f"[bold green]✓ Created character: {name}[/bold green]")
            return character

        except (json.JSONDecodeError, KeyError) as e:
            console.print(f"[bold red]Error parsing character: {e}[/bold red]")
            raise

    def write_chapter(
        self,
        chapter_number: int,
        chapter_title: str,
        outline: StoryOutline,
        previous_chapters_summary: str = "",
        target_words: int = 2000,
    ) -> Chapter:
        """
        Write a complete chapter

        Args:
            chapter_number: The chapter number
            chapter_title: The chapter title
            outline: The story outline
            previous_chapters_summary: Summary of previous chapters for continuity
            target_words: Target word count for the chapter

        Returns:
            Chapter object with complete content
        """
        console.print(f"[bold blue]Writing Chapter {chapter_number}: {chapter_title}...[/bold blue]")

        system_prompt = """You are a masterful novelist with expertise in creative writing.
        Write engaging, well-paced chapters with vivid descriptions, compelling dialogue,
        and strong character development. Maintain consistency with the story's tone, style,
        and established plot points."""

        # Get relevant plot point
        plot_point = ""
        if chapter_number <= len(outline.plot_points):
            plot_point = outline.plot_points[chapter_number - 1]

        user_message = f"""Write Chapter {chapter_number} of the novel with the following details:

Title: {outline.title}
Genre: {outline.genre}
Setting: {outline.setting}
Themes: {', '.join(outline.themes)}

Chapter Title: {chapter_title}
Plot Point for this Chapter: {plot_point}

Characters:
{self._format_characters(outline.characters)}

Previous Story Summary:
{previous_chapters_summary if previous_chapters_summary else "This is the first chapter."}

Requirements:
- Target length: approximately {target_words} words
- Include vivid descriptions and engaging dialogue
- Advance the plot meaningfully
- Develop characters through actions and interactions
- Maintain consistency with the story's tone and style
- End with a compelling hook for the next chapter

Write the complete chapter content now:"""

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Writing chapter {chapter_number}...", total=None)
            content = self._create_message(
                system_prompt,
                user_message,
                max_tokens=4096,
            )
            progress.update(task, completed=True)

        chapter = Chapter(
            number=chapter_number,
            title=chapter_title,
            content=content,
            summary=f"Summary for chapter {chapter_number}",
        )

        console.print(
            f"[bold green]✓ Completed Chapter {chapter_number} "
            f"({chapter.word_count} words)[/bold green]"
        )

        return chapter

    def edit_content(
        self,
        content: str,
        edit_instructions: str,
    ) -> str:
        """
        Edit and refine content based on instructions

        Args:
            content: The content to edit
            edit_instructions: Specific editing instructions

        Returns:
            Edited content
        """
        console.print("[bold blue]Editing content...[/bold blue]")

        system_prompt = """You are an expert editor specializing in fiction.
        Refine prose, improve pacing, enhance descriptions, and strengthen dialogue
        while maintaining the author's voice and intent."""

        user_message = f"""Edit the following content according to these instructions:

Instructions: {edit_instructions}

Content to edit:
{content}

Provide the edited version:"""

        edited = self._create_message(system_prompt, user_message)

        console.print("[bold green]✓ Content edited[/bold green]")
        return edited

    def create_novel(
        self,
        genre: str,
        premise: str,
        num_chapters: int = 5,
        themes: List[str] = None,
    ) -> Novel:
        """
        Create a complete novel from start to finish

        Args:
            genre: The genre of the novel
            premise: The premise or concept
            num_chapters: Number of chapters to write
            themes: Themes to explore

        Returns:
            Complete Novel object
        """
        console.print(f"[bold magenta]Starting novel creation process...[/bold magenta]\n")

        # Step 1: Create outline
        outline = self.create_story_outline(genre, premise, themes, num_chapters)
        console.print()

        # Step 2: Create the novel
        novel = Novel(outline=outline)
        self.current_novel = novel

        # Step 3: Write chapters
        previous_summary = ""
        for i in range(1, num_chapters + 1):
            chapter_title = f"Chapter {i}"
            if i <= len(outline.plot_points):
                # Use plot point as chapter inspiration
                plot_point = outline.plot_points[i - 1]
                chapter_title = f"Chapter {i}: {plot_point[:50]}..."

            chapter = self.write_chapter(
                chapter_number=i,
                chapter_title=chapter_title,
                outline=outline,
                previous_chapters_summary=previous_summary,
            )

            novel.add_chapter(chapter)

            # Update summary for next chapter
            previous_summary += f"\nChapter {i}: {chapter.content[:500]}..."

            console.print()

        console.print(
            f"[bold magenta]✓ Novel complete! Total words: {novel.total_word_count}[/bold magenta]\n"
        )

        return novel

    def save_novel(self, novel: Novel, filename: Optional[str] = None):
        """Save the novel to a file"""
        if not filename:
            # Generate filename from title
            safe_title = "".join(
                c for c in novel.outline.title if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            filename = f"{safe_title.replace(' ', '_')}.txt"

        filepath = self.config.output_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{novel.outline.title}\n")
            f.write(f"{'=' * len(novel.outline.title)}\n\n")
            f.write(f"Genre: {novel.outline.genre}\n")
            f.write(f"Premise: {novel.outline.premise}\n\n")

            f.write("Characters:\n")
            for char in novel.outline.characters:
                f.write(f"\n- {char.name} ({char.role}): {char.description}\n")

            f.write("\n" + "=" * 80 + "\n\n")

            for chapter in novel.chapters:
                f.write(f"\n\n{chapter.title}\n")
                f.write(f"{'-' * len(chapter.title)}\n\n")
                f.write(f"{chapter.content}\n")

            f.write(f"\n\n{'=' * 80}\n")
            f.write(f"Total Word Count: {novel.total_word_count}\n")

        console.print(f"[bold green]✓ Novel saved to: {filepath}[/bold green]")
        return filepath

    def _format_characters(self, characters: List[Character]) -> str:
        """Format characters for prompt"""
        result = []
        for char in characters:
            result.append(f"- {char.name} ({char.role}): {char.description}")
        return "\n".join(result)

    def interactive_mode(self):
        """Start an interactive writing session"""
        console.print("[bold magenta]Welcome to Novel Writing Agent - Interactive Mode[/bold magenta]\n")
        console.print("Commands:")
        console.print("  'outline' - Create a new story outline")
        console.print("  'chapter' - Write a chapter")
        console.print("  'character' - Create a character")
        console.print("  'novel' - Create a complete novel")
        console.print("  'save' - Save current novel")
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
                    themes_input = console.input("Themes (comma-separated): ")
                    themes = [t.strip() for t in themes_input.split(",") if t.strip()]

                    outline = self.create_story_outline(genre, premise, themes)
                    self.current_novel = Novel(outline=outline)
                    console.print(f"\n[green]Created outline: {outline.title}[/green]\n")

                elif command == "novel":
                    genre = console.input("Genre: ")
                    premise = console.input("Premise: ")
                    num_chapters = int(console.input("Number of chapters (default 5): ") or "5")
                    themes_input = console.input("Themes (comma-separated, optional): ")
                    themes = [t.strip() for t in themes_input.split(",") if t.strip()] or None

                    novel = self.create_novel(genre, premise, num_chapters, themes)
                    self.save_novel(novel)

                elif command == "save":
                    if self.current_novel:
                        self.save_novel(self.current_novel)
                    else:
                        console.print("[red]No novel to save. Create one first![/red]")

                else:
                    console.print(f"[red]Unknown command: {command}[/red]")

            except KeyboardInterrupt:
                console.print("\n[bold yellow]Interrupted. Type 'exit' to quit.[/bold yellow]")
            except Exception as e:
                console.print(f"[bold red]Error: {e}[/bold red]")
