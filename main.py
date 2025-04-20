import argparse
import time
from pathlib import Path
from src.parser import MarkerPdfParser
from src.utils.multimodal_llm import MultimodalLLM
from src.utils.generate_metadata import generate_metadata
from src.libre_pptx_to_pdf import convert_pptx_to_pdf
from config.config import Config, default_config

def process_pptx(pptx_path: Path, config: Config) -> bool:
    """Process a single PPTX file"""
    file_base = pptx_path.stem
    pdf_path = convert_pptx_to_pdf(str(pptx_path))
    
    # Create output directory structure
    file_output_dir = config.output_path / file_base
    file_output_dir.mkdir(parents=True, exist_ok=True)
    
    image_dir = file_output_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize parser and process the file
    parser = MarkerPdfParser()
    result = parser.parse(
        file_path=str(pdf_path),
        output_format=config.output_format,
        langs=config.langs,
        extracted_image_dir=str(image_dir),
        force_ocr=config.force_ocr,
    )
    
    if not result["success"]:
        print(f"Error processing {pptx_path.name}: {result.get('error')}")
        return False
    
    # Save images and update markdown content
    markdown_content = result["content"]
    if "images" in result:
        for img_name, img_obj in result["images"].items():
            img_path = image_dir / img_name
            img_obj.save(str(img_path))
            markdown_content = markdown_content.replace(
                f"![]({img_name})", 
                f"![](images/{img_name})"
            )
    
    # Save markdown content
    markdown_path = file_output_dir / f"{file_base}.md"
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    # Generate metadata if enabled
    if config.desc_images:
        multimodal_llm = MultimodalLLM(
            model_name=config.model_name,
            base_url=config.ollama_url
        )
        generate_metadata(str(markdown_path), multimodal_llm)
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Process PPTX files and extract content")
    
    # Input/Output settings
    parser.add_argument("--input-dir", default=default_config.input_dir,
                       help="Directory containing PPTX files")
    parser.add_argument("--output-dir", default=default_config.output_dir,
                       help="Directory to save processed files")
    
    # LLM settings
    parser.add_argument("--ollama-url", default=default_config.ollama_url,
                       help="URL of the Ollama server")
    parser.add_argument("--model-name", default=default_config.model_name,
                       help="Name of the model to use")
    
    # Processing flags
    parser.add_argument("--no-desc-images", action="store_true",
                       help="Disable image description generation")
    parser.add_argument("--no-force-ocr", action="store_true",
                       help="Disable forced OCR")
    parser.add_argument("--output-format", default=default_config.output_format,
                       choices=["markdown", "html"],
                       help="Output format for processed files")
    parser.add_argument("--langs", default=default_config.langs,
                       help="Languages for processing")
    
    args = parser.parse_args()
    
    # Create configuration from arguments
    config = Config(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        ollama_url=args.ollama_url,
        model_name=args.model_name,
        desc_images=not args.no_desc_images,
        force_ocr=not args.no_force_ocr,
        output_format=args.output_format,
        langs=args.langs
    )
    
    # Ensure directories exist
    config.ensure_dirs_exist()
    
    # Process files
    start_time = time.time()
    processed_count = 0
    error_count = 0
    
    for pptx_path in Path(config.input_dir).glob("*.pptx"):
        if process_pptx(pptx_path, config):
            processed_count += 1
        else:
            error_count += 1
    
    # Print summary
    print(f"\nProcessing complete!")
    print(f"Processed files: {processed_count}")
    print(f"Errors: {error_count}")
    print(f"Total time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
