import time
from typing import Dict, Any, Optional
import os


class MarkerPdfParser:
    def __init__(self):
        """Initialize the parser and load models once"""
        try:
            from marker.models import create_model_dict
            self.artifact_dict = create_model_dict()
        except ImportError as e:
            raise ImportError(f"Required module not found: {str(e)}. Install with: pip install marker-pdf")

    def parse(
        self,
        file_path: str,
        output_format: str = "markdown",
        extracted_image_dir: Optional[str] = None,
        **kwargs,
    ):
        """
        Parse PDF document using either Marker API or local conversion.

        Args:
            file_path: Path to the PDF file
            output_format: Desired output format (default: "markdown")
            extracted_image_dir: Directory to save extracted images
            **kwargs: Additional parameters for the specific parsing 

        Returns:
            Dictionary containing parsed content and metadata
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        
        result = self.parse_locally(
                file_path, 
                output_format, 
                extracted_image_dir=extracted_image_dir,
                **kwargs
            )
        return result

    def parse_locally(
        self,
        file_path: str,
        output_format: str = "markdown",
        langs: Optional[str] = None,
        force_ocr: bool = False,
        extracted_image_dir: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Parse PDF using local Marker library"""
        try:
            from marker.converters.pdf import PdfConverter
            from marker.output import text_from_rendered

            config = {
                "output_format": output_format,
                "force_ocr": force_ocr,
                "langs": langs.split(",") if langs else ["en"],
                "paginate_output": True,
            }
            
            # Configure image extraction if directory is specified
            if extracted_image_dir:
                config["save_images"] = True
                config["image_dir"] = extracted_image_dir
                os.makedirs(extracted_image_dir, exist_ok=True)
                            
            converter = PdfConverter(artifact_dict=self.artifact_dict, config=config)
            rendered = converter(file_path)

            if output_format.lower() == "markdown":
                content, markdown, images = text_from_rendered(rendered)
                return {
                    "success": True,
                    "content": content,
                    "markdown": markdown,
                    "images": images
                }
            else:
                return {
                    "success": False,
                    "error": f"Unsupported local output format: {output_format}. Only markdown is supported locally.",
                }

        except Exception as e:
            return {"success": False, "error": f"Error during local parsing: {str(e)}"}
        