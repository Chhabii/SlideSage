# SlideSage

SlideSage is an intelligent presentation analysis tool that extracts and understands content from PowerPoint presentations. It combines advanced PDF parsing with AI-powered image understanding to provide deep insights into your slides.

![slidesage](https://github.com/user-attachments/assets/d7425a79-1a20-4ab9-b0d2-21ad5a67e35f)
## Features

- Convert PPTX files to PDF and extract content
- Extract images from presentations
- Generate AI-powered descriptions for images
- Support for multiple languages
- Configurable processing options

## Prerequisites

- Docker and Docker Compose
- At least 8GB of RAM (for running the LLM)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/chhabii/slidesage.git
   cd slidesage
   ```

2. Run the setup script:
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. Place your PPTX files in the `input` directory

4. Process the files:
   ```bash
   cd docker
   docker-compose exec slidesage python main.py
   ```

5. Find the processed files in the `output` directory

## Configuration

The tool can be configured using command-line arguments:

```bash
python main.py --help
```

Available options:
- `--input-dir`: Directory containing PPTX files (default: "input")
- `--output-dir`: Directory to save processed files (default: "output")
- `--ollama-url`: URL of the Ollama server (default: "http://localhost:11434")
- `--model-name`: Name of the model to use (default: "gemma3:4b")
- `--no-desc-images`: Disable image description generation
- `--no-force-ocr`: Disable forced OCR
- `--output-format`: Output format (choices: "markdown", "html")
- `--langs`: Languages for processing (default: "en")

## Example

1. Place a PPTX file in the `input` directory
2. Run the processing:
   ```bash
   docker-compose exec slidesage python main.py
   ```
3. Check the `output` directory for the processed files:
   - Markdown file with extracted content
   - Images directory with extracted images
   - Metadata with AI-generated descriptions

## Project Structure

```
slidesage/
├── src/                    # Source code
│   ├── parser.py          # PDF parser
│   ├── utils/             # Utility functions
│   └── libre_pptx_to_pdf.py
├── config/                # Configuration
│   └── config.py
├── docker/               # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/              # Utility scripts
│   └── setup.sh
├── input/               # Input directory
├── output/             # Output directory
└── main.py            # Entry point
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
