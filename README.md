# Novel Writing Agent 📚✨

An intelligent agent for creative novel writing powered by **Claude Agent SDK** (`claude-agent-sdk-python`). This agent uses custom tools and the Model Context Protocol (MCP) to generate story outlines, create compelling characters, write complete chapters, and produce full-length novels with coherent narratives.

## Features

🎭 **Character Creation**: Generate deep, multi-dimensional characters with rich backstories, personalities, and motivations

📖 **Story Outlining**: Create comprehensive story outlines with plot structure, themes, and character arcs

✍️ **Chapter Writing**: Write engaging chapters with vivid descriptions, compelling dialogue, and strong pacing

🎨 **Multiple Genres**: Support for various genres including fantasy, sci-fi, mystery, romance, thriller, and more

🔄 **Narrative Continuity**: Maintains consistency across chapters and character development

💾 **Export Options**: Save novels in readable text format

🎯 **Interactive Mode**: Work with the agent interactively to craft your story step by step

🛠️ **Custom Tools**: Built with `@tool` decorator and MCP server for extensible functionality

## Technology Stack

This project is built using:
- **[claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python)** - Anthropic's official Python SDK for building agents
- **Custom Tools** - Specialized tools for novel writing using the `@tool` decorator
- **MCP (Model Context Protocol)** - In-process MCP server for better performance
- **Async/Await** - Full async support for efficient API calls

## Installation

### Prerequisites

- Python 3.9 or higher
- Anthropic API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/novel-agent.git
cd novel-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. (Optional) Install in development mode:
```bash
pip install -e .
```

## Quick Start

### Command Line Usage

Generate a complete novel with a single command:

```bash
python -m src.novel_agent.main \
  --genre "science fiction" \
  --premise "Humanity discovers faster-than-light travel but finds the galaxy already inhabited" \
  --chapters 5 \
  --themes "exploration,first contact,ethics"
```

### Interactive Mode

Start an interactive writing session:

```bash
python -m src.novel_agent.main --interactive
```

In interactive mode, you can:
- Create story outlines
- Write individual chapters
- Generate characters
- Create complete novels
- Get writing tips
- Send custom prompts

### Python API

Use the agent programmatically:

```python
import anyio
from novel_agent.agent import NovelWritingAgent

async def main():
    # Initialize the agent
    agent = NovelWritingAgent()

    # Create a complete novel
    result = await agent.create_novel(
        genre="fantasy",
        premise="A young mage discovers a forbidden spell that could save or destroy the world",
        num_chapters=10,
        themes=["power", "responsibility", "sacrifice"]
    )

# Run the async function
anyio.run(main)
```

## Architecture

### Custom Tools

The agent uses custom tools defined with the `@tool` decorator from claude-agent-sdk:

```python
from claude_agent_sdk import tool

@tool(
    "create_story_outline",
    "Create a comprehensive story outline with plot structure, characters, and themes",
    {
        "genre": str,
        "premise": str,
        "themes": str,
        "num_chapters": int,
    }
)
async def create_story_outline_tool(args):
    # Tool implementation
    pass
```

Available tools:
- `create_story_outline` - Generate complete story structures
- `create_character` - Develop detailed characters
- `write_chapter` - Write full chapters with narrative flow
- `save_story_content` - Save work to files
- `get_writing_tips` - Get writing guidance

### MCP Server

Tools are packaged into an in-process MCP server for high performance:

```python
from claude_agent_sdk import create_sdk_mcp_server

server = create_sdk_mcp_server(
    name="novel-writing-tools",
    version="1.0.0",
    tools=[
        create_story_outline_tool,
        create_character_tool,
        write_chapter_tool,
        save_story_content_tool,
        get_writing_tips_tool,
    ],
)
```

### Agent Configuration

The agent is configured with `ClaudeAgentOptions`:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    system_prompt="You are an expert novelist...",
    mcp_servers={"novel-writing": server},
    allowed_tools=["create_story_outline", "create_character", ...],
    max_turns=50,
)
```

## Examples

The `examples/` directory contains several demonstration scripts:

### Basic Usage
```bash
python examples/basic_usage.py
```
Creates a short sci-fi story with 3 chapters using the agent's tools.

### Create Outline
```bash
python examples/create_outline.py
```
Generates a detailed story outline without writing the full novel.

### Create Characters
```bash
python examples/create_character.py
```
Creates multiple characters with detailed backgrounds and motivations.

## API Reference

### NovelWritingAgent

The main class for interacting with the novel writing system.

#### `__init__(config=None)`

Initialize the agent with custom tools and MCP server.

**Parameters:**
- `config` (AgentConfig, optional): Configuration object

#### `async create_novel(genre, premise, num_chapters=5, themes=None)`

Create a complete novel from start to finish.

**Parameters:**
- `genre` (str): The genre of the novel
- `premise` (str): The premise or concept
- `num_chapters` (int, optional): Number of chapters (default: 5)
- `themes` (List[str], optional): Themes to explore

**Returns:** str - Result text from the agent

**Example:**
```python
result = await agent.create_novel(
    genre="mystery",
    premise="A detective must solve a murder in a locked room",
    num_chapters=8,
    themes=["justice", "truth", "deception"]
)
```

#### `async create_story_outline(genre, premise, themes=None, num_chapters=10)`

Create a comprehensive story outline.

**Parameters:**
- `genre` (str): The genre of the story
- `premise` (str): The basic premise
- `themes` (List[str], optional): List of themes
- `num_chapters` (int, optional): Target number of chapters (default: 10)

**Returns:** str - The outline as text

#### `async create_character(name, role, story_context="")`

Create a detailed character.

**Parameters:**
- `name` (str): Character's name
- `role` (str): Character's role ("main", "supporting", "minor")
- `story_context` (str, optional): Context about the story

**Returns:** str - Character description

#### `async write_chapter(chapter_number, chapter_title, plot_point, story_context="", target_words=2000)`

Write a complete chapter.

**Parameters:**
- `chapter_number` (int): The chapter number
- `chapter_title` (str): The chapter title
- `plot_point` (str): The main plot point for this chapter
- `story_context` (str, optional): Context about the story
- `target_words` (int, optional): Target word count (default: 2000)

**Returns:** str - The chapter content

#### `async interactive_mode()`

Start an interactive writing session with the agent.

## Configuration

Configuration is managed through environment variables in the `.env` file:

```env
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional
MODEL_NAME=claude-sonnet-4-20250514
MAX_TOKENS=4096
TEMPERATURE=0.8
OUTPUT_DIR=generated_stories
LOG_LEVEL=INFO
```

### Configuration Options

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
- `MODEL_NAME`: Claude model to use (default: claude-sonnet-4-20250514)
- `MAX_TOKENS`: Maximum tokens per request (default: 4096)
- `TEMPERATURE`: Creativity level 0-1 (default: 0.8)
- `OUTPUT_DIR`: Directory for generated novels (default: generated_stories)
- `LOG_LEVEL`: Logging level (default: INFO)

## How It Works

1. **Tool Definition**: Custom tools are defined using the `@tool` decorator from claude-agent-sdk
2. **MCP Server**: Tools are packaged into an in-process MCP server for high performance
3. **Agent Initialization**: The `NovelWritingAgent` creates an agent with these tools
4. **Query Execution**: When you call agent methods, they use `query()` to interact with Claude
5. **Tool Invocation**: Claude autonomously decides when to use tools based on the prompt
6. **Result Streaming**: Results stream back asynchronously as they're generated

## Tips for Best Results

1. **Be Specific with Premises**: The more detailed your premise, the better the output
   - ✅ "A detective with amnesia must solve their own attempted murder"
   - ❌ "A detective story"

2. **Choose Appropriate Themes**: Select 2-4 themes that complement your story

3. **Adjust Temperature**:
   - Lower (0.6-0.7) for more consistent, structured writing
   - Higher (0.8-0.9) for more creative, varied output

4. **Start Small**: Begin with 3-5 chapters to test your story concept

5. **Use Interactive Mode**: For fine control over the creative process

## Troubleshooting

### "Configuration Error: ANTHROPIC_API_KEY is required"

Make sure you've created a `.env` file with your API key:
```bash
cp .env.example .env
# Edit .env and add your key
```

### Import errors with claude_agent_sdk

Ensure you've installed the correct package:
```bash
pip install claude-agent-sdk
```

### Async errors

All agent methods are async. Make sure to use `await` and run with `anyio.run()`:
```python
import anyio

async def main():
    agent = NovelWritingAgent()
    await agent.create_novel(...)

anyio.run(main)
```

## Project Structure

```
novel-agent/
├── src/
│   └── novel_agent/
│       ├── __init__.py
│       ├── main.py              # CLI entry point
│       ├── agent.py             # Core agent with SDK integration
│       ├── tools/               # Custom tools
│       │   ├── __init__.py
│       │   └── story_tools.py   # @tool decorated functions
│       ├── models/              # Data models
│       │   ├── __init__.py
│       │   └── story.py
│       └── config/              # Configuration
│           ├── __init__.py
│           └── settings.py
├── examples/                    # Example scripts
│   ├── basic_usage.py
│   ├── create_outline.py
│   └── create_character.py
├── tests/                       # Unit tests
├── generated_stories/           # Output directory
├── requirements.txt             # Dependencies
├── pyproject.toml              # Project configuration
├── .env.example                # Example environment variables
└── README.md                   # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Anthropic's Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)
- Powered by [Claude](https://www.anthropic.com/)

## Resources

- [Claude Agent SDK Documentation](https://github.com/anthropics/claude-agent-sdk-python)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Anthropic API Documentation](https://docs.anthropic.com/)

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Happy Writing! 📚✨**

*Built with claude-agent-sdk-python - Anthropic's official Python SDK for building agents with Claude.*
