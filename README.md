# Novel Writing Agent 📚✨

An intelligent agent for creative novel writing powered by Claude and the Anthropic SDK. This agent can generate story outlines, create compelling characters, write complete chapters, and produce full-length novels with coherent narratives.

## Features

🎭 **Character Creation**: Generate deep, multi-dimensional characters with rich backstories, personalities, and motivations

📖 **Story Outlining**: Create comprehensive story outlines with plot structure, themes, and character arcs

✍️ **Chapter Writing**: Write engaging chapters with vivid descriptions, compelling dialogue, and strong pacing

🎨 **Multiple Genres**: Support for various genres including fantasy, sci-fi, mystery, romance, thriller, and more

🔄 **Narrative Continuity**: Maintains consistency across chapters and character development

💾 **Export Options**: Save novels in readable text format

🎯 **Interactive Mode**: Work with the agent interactively to craft your story step by step

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
- Save your work

### Python API

Use the agent programmatically:

```python
from novel_agent.agent import NovelWritingAgent

# Initialize the agent
agent = NovelWritingAgent()

# Create a complete novel
novel = agent.create_novel(
    genre="fantasy",
    premise="A young mage discovers a forbidden spell that could save or destroy the world",
    num_chapters=10,
    themes=["power", "responsibility", "sacrifice"]
)

# Save the novel
agent.save_novel(novel)
```

## Examples

The `examples/` directory contains several demonstration scripts:

### Basic Usage
```bash
python examples/basic_usage.py
```
Creates a short sci-fi story with 3 chapters.

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

#### `create_story_outline(genre, premise, themes=None, num_chapters=10)`

Create a comprehensive story outline.

**Parameters:**
- `genre` (str): The genre of the story (e.g., "fantasy", "sci-fi", "mystery")
- `premise` (str): The basic premise or concept of the story
- `themes` (List[str], optional): List of themes to explore
- `num_chapters` (int, optional): Target number of chapters (default: 10)

**Returns:** `StoryOutline` object

**Example:**
```python
outline = agent.create_story_outline(
    genre="fantasy",
    premise="A thief must steal a magical artifact to save their city",
    themes=["redemption", "loyalty"],
    num_chapters=12
)
```

#### `create_character(name, role, story_context="")`

Create a detailed character.

**Parameters:**
- `name` (str): Character's name
- `role` (str): Character's role ("main", "supporting", "minor")
- `story_context` (str, optional): Context about the story

**Returns:** `Character` object

**Example:**
```python
character = agent.create_character(
    name="Elena Ravenwood",
    role="main",
    story_context="A fantasy story about magical thieves"
)
```

#### `write_chapter(chapter_number, chapter_title, outline, previous_chapters_summary="", target_words=2000)`

Write a complete chapter.

**Parameters:**
- `chapter_number` (int): The chapter number
- `chapter_title` (str): The chapter title
- `outline` (StoryOutline): The story outline
- `previous_chapters_summary` (str, optional): Summary of previous chapters
- `target_words` (int, optional): Target word count (default: 2000)

**Returns:** `Chapter` object

#### `create_novel(genre, premise, num_chapters=5, themes=None)`

Create a complete novel from start to finish.

**Parameters:**
- `genre` (str): The genre of the novel
- `premise` (str): The premise or concept
- `num_chapters` (int, optional): Number of chapters (default: 5)
- `themes` (List[str], optional): Themes to explore

**Returns:** `Novel` object

**Example:**
```python
novel = agent.create_novel(
    genre="mystery",
    premise="A detective must solve a murder in a locked room",
    num_chapters=8,
    themes=["justice", "truth", "deception"]
)
```

#### `save_novel(novel, filename=None)`

Save the novel to a file.

**Parameters:**
- `novel` (Novel): The novel to save
- `filename` (str, optional): Output filename (auto-generated if not provided)

**Returns:** Path to the saved file

#### `edit_content(content, edit_instructions)`

Edit and refine content.

**Parameters:**
- `content` (str): The content to edit
- `edit_instructions` (str): Specific editing instructions

**Returns:** Edited content as string

## Data Models

### StoryOutline
```python
class StoryOutline(BaseModel):
    title: str
    genre: str
    premise: str
    themes: List[str]
    setting: str
    plot_points: List[str]
    characters: List[Character]
```

### Character
```python
class Character(BaseModel):
    name: str
    description: str
    role: str  # "main", "supporting", "minor"
    personality: Optional[str]
    background: Optional[str]
    motivations: Optional[str]
```

### Chapter
```python
class Chapter(BaseModel):
    number: int
    title: str
    content: str
    summary: Optional[str]
    word_count: int
```

### Novel
```python
class Novel(BaseModel):
    outline: StoryOutline
    chapters: List[Chapter]

    @property
    def total_word_count(self) -> int:
        # Returns total word count of all chapters
```

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

## Advanced Usage

### Custom Temperature and Tokens

```python
from novel_agent.config import AgentConfig

config = AgentConfig()
config.temperature = 0.9  # More creative
config.max_tokens = 8192  # Longer outputs

agent = NovelWritingAgent(config)
```

### Editing Existing Content

```python
chapter_content = "Your chapter content here..."

edited = agent.edit_content(
    content=chapter_content,
    edit_instructions="Make the dialogue more natural and add more sensory details"
)
```

### Building Novels Incrementally

```python
from novel_agent.models import Novel

# Create outline
outline = agent.create_story_outline(
    genre="thriller",
    premise="A conspiracy unfolds in the highest levels of government"
)

# Create novel object
novel = Novel(outline=outline)

# Write chapters one at a time
for i in range(1, 6):
    chapter = agent.write_chapter(
        chapter_number=i,
        chapter_title=f"Chapter {i}",
        outline=outline,
        previous_chapters_summary=get_summary(novel)
    )
    novel.add_chapter(chapter)

    # Save after each chapter
    agent.save_novel(novel)
```

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

### Chapters are too short/long

Adjust the `target_words` parameter:
```python
chapter = agent.write_chapter(
    chapter_number=1,
    chapter_title="The Beginning",
    outline=outline,
    target_words=3000  # Longer chapter
)
```

### Output is too similar/repetitive

Increase the temperature:
```python
config = AgentConfig()
config.temperature = 0.9
agent = NovelWritingAgent(config)
```

## Project Structure

```
novel-agent/
├── src/
│   └── novel_agent/
│       ├── __init__.py
│       ├── main.py              # CLI entry point
│       ├── agent.py             # Core agent implementation
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

- Built with [Anthropic's Claude](https://www.anthropic.com/)
- Powered by the Anthropic Python SDK

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Happy Writing! 📚✨**
