import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class AgentConfig:
    """Configuration for the Novel Writing Agent"""

    # API Configuration
    api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model: str = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "4096"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.8"))

    # Output Configuration
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", "generated_stories"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def __post_init__(self):
        """Ensure output directory exists"""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is required. "
                "Please set it in your .env file or environment variables."
            )
