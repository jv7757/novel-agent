#!/usr/bin/env python3
"""
Main entry point for the Novel Writing Agent using Claude Agent SDK
"""

import sys
import argparse
import anyio
from pathlib import Path
from rich.console import Console

from .agent import NovelWritingAgent
from .config import AgentConfig

console = Console()


async def run_interactive(agent: NovelWritingAgent):
    """Run interactive mode"""
    await agent.interactive_mode()


async def run_create_novel(
    agent: NovelWritingAgent,
    genre: str,
    premise: str,
    num_chapters: int,
    themes: list = None
):
    """Create a novel from command line arguments"""
    console.print("[bold magenta]Novel Writing Agent (Claude Agent SDK)[/bold magenta]\n")

    result = await agent.create_novel(
        genre=genre,
        premise=premise,
        num_chapters=num_chapters,
        themes=themes,
    )

    console.print(f"\n[bold green]✓ Novel creation process complete![/bold green]\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Novel Writing Agent - An intelligent agent for creative writing powered by Claude Agent SDK"
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Start interactive mode",
    )
    parser.add_argument(
        "--genre",
        "-g",
        type=str,
        help="Genre of the novel (e.g., fantasy, sci-fi, mystery)",
    )
    parser.add_argument(
        "--premise",
        "-p",
        type=str,
        help="Premise or concept for the novel",
    )
    parser.add_argument(
        "--chapters",
        "-c",
        type=int,
        default=5,
        help="Number of chapters to write (default: 5)",
    )
    parser.add_argument(
        "--themes",
        "-t",
        type=str,
        help="Comma-separated list of themes",
    )

    args = parser.parse_args()

    try:
        config = AgentConfig()
        agent = NovelWritingAgent(config)

        if args.interactive:
            # Start interactive mode
            anyio.run(run_interactive, agent)

        elif args.genre and args.premise:
            # Create a novel from command line arguments
            themes = None
            if args.themes:
                themes = [t.strip() for t in args.themes.split(",")]

            anyio.run(
                run_create_novel,
                agent,
                args.genre,
                args.premise,
                args.chapters,
                themes
            )

        else:
            # Show help if no valid arguments
            parser.print_help()
            console.print("\n[yellow]Tip: Use --interactive for interactive mode[/yellow]")
            console.print("[yellow]     Or provide --genre and --premise to generate a novel[/yellow]\n")
            console.print("[cyan]Examples:[/cyan]")
            console.print("  python -m src.novel_agent.main --interactive")
            console.print('  python -m src.novel_agent.main -g "fantasy" -p "A young wizard discovers..." -c 3\n')

    except ValueError as e:
        console.print(f"[bold red]Configuration Error: {e}[/bold red]")
        console.print("\n[yellow]Please ensure ANTHROPIC_API_KEY is set in your .env file[/yellow]")
        sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Interrupted by user[/bold yellow]")
        sys.exit(0)

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
