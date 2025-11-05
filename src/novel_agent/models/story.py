from typing import List, Optional
from pydantic import BaseModel, Field


class Character(BaseModel):
    """Represents a character in the story"""
    name: str
    description: str
    role: str = "supporting"  # main, supporting, minor
    personality: Optional[str] = None
    background: Optional[str] = None
    motivations: Optional[str] = None


class StoryOutline(BaseModel):
    """Represents the outline of a story"""
    title: str
    genre: str
    premise: str
    themes: List[str] = Field(default_factory=list)
    setting: str
    target_length: str = "medium"  # short, medium, long
    plot_points: List[str] = Field(default_factory=list)
    characters: List[Character] = Field(default_factory=list)


class Chapter(BaseModel):
    """Represents a chapter in the novel"""
    number: int
    title: str
    summary: Optional[str] = None
    content: str
    word_count: int = 0

    def __init__(self, **data):
        super().__init__(**data)
        if not self.word_count and self.content:
            self.word_count = len(self.content.split())


class Novel(BaseModel):
    """Represents a complete novel"""
    outline: StoryOutline
    chapters: List[Chapter] = Field(default_factory=list)

    @property
    def total_word_count(self) -> int:
        """Calculate total word count of all chapters"""
        return sum(chapter.word_count for chapter in self.chapters)

    def add_chapter(self, chapter: Chapter):
        """Add a chapter to the novel"""
        self.chapters.append(chapter)

    def get_chapter(self, number: int) -> Optional[Chapter]:
        """Get a chapter by its number"""
        for chapter in self.chapters:
            if chapter.number == number:
                return chapter
        return None
