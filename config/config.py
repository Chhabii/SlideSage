from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    # Input/Output settings
    input_dir: str = "input"
    output_dir: str = "output"
    
    # LLM settings
    ollama_url: str = "http://localhost:11434"
    model_name: str = "gemma3:4b"
    
    # Processing flags
    desc_images: bool = True  # Whether to generate image descriptions
    force_ocr: bool = True    # Whether to force OCR on all text
    output_format: str = "markdown"  # Output format (markdown, html, etc.)
    langs: str = "en"         # Language for processing
    
    # Path settings
    @property
    def input_path(self) -> Path:
        return Path(self.input_dir)
    
    @property
    def output_path(self) -> Path:
        return Path(self.output_dir)
    
    def ensure_dirs_exist(self):
        """Ensure all required directories exist"""
        self.input_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)

# Default configuration
default_config = Config() 