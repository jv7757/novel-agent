#!/usr/bin/env python3
"""
Main entry point for the Novel Writing Agent
"""

import sys
import argparse
from pathlib import Path
from rich.console import Console

from .agent import NovelWritingAgent
from .config import AgentConfig

console = Console()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Novel Writing Agent - An intelligent agent for creative writing"
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
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output filename for the novel",
    )

    args = parser.parse_args()

    try:
        config = AgentConfig()
        agent = NovelWritingAgent(config)

        if args.interactive:
            # Start interactive mode
            agent.interactive_mode()

        elif args.genre and args.premise:
            # Create a novel from command line arguments
            console.print("[bold magenta]Novel Writing Agent[/bold magenta]\n")

            themes = None
            if args.themes:
                themes = [t.strip() for t in args.themes.split(",")]

            novel = agent.create_novel(
                genre=args.genre,
                premise=args.premise,
                num_chapters=args.chapters,
                themes=themes,
            )

            # Save the novel
            filepath = agent.save_novel(novel, args.output)

            console.print(f"\n[bold green]✓ Novel created successfully![/bold green]")
            console.print(f"[bold green]  Title: {novel.outline.title}[/bold green]")
            console.print(f"[bold green]  Chapters: {len(novel.chapters)}[/bold green]")
            console.print(f"[bold green]  Words: {novel.total_word_count}[/bold green]")
            console.print(f"[bold green]  File: {filepath}[/bold green]\n")

        else:
            # Show help if no valid arguments
            parser.print_help()
            console.print("\n[yellow]Tip: Use --interactive for interactive mode[/yellow]")
            console.print("[yellow]     Or provide --genre and --premise to generate a novel[/yellow]\n")

    except ValueError as e:
        console.print(f"[bold red]Configuration Error: {e}[/bold red]")
        console.print("\n[yellow]Please ensure ANTHROPIC_API_KEY is set in your .env file[/yellow]")
        sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Interrupted by user[/bold yellow]")
        sys.exit(0)

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
