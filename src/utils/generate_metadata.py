import json
import os
from datetime import datetime
import re
from typing import List, Dict, Any

def extract_slide_content(markdown_content: str) -> List[Dict[str, Any]]:
    # Split content by page separators
    slides = re.split(r'\n\n{\d+}------------------------------------------------\n\n', markdown_content)
    slides = [slide.strip() for slide in slides if slide.strip()]
    
    slide_data = []
    for i, slide in enumerate(slides):
        # Extract all text content and images
        lines = slide.split('\n')
        description_lines = []
        images = []
        
        for line in lines:
            # Check for image references
            if line.startswith('![') or line.startswith('![](images/'):
                image_path = re.search(r'\((.*?)\)', line).group(1)
                images.append({
                    "path": image_path,
                    "description": ""  # Will be filled by LLM later
                })
            # Collect all non-image lines as description, preserving markdown formatting
            # Skip the page separator line if it exists
            elif line.strip() and not line.startswith('{') and not line.startswith('#'):
                description_lines.append(line)
        
        # Join all description lines with newlines to preserve markdown structure
        description = '\n'.join(description_lines)
        
        slide_data.append({
            "slide_number": i,
            "description": description,
            "desc_summary": "",  # Will be filled by LLM later
            "images": images
        })
    
    return slide_data

def generate_summary(text: str, multimodal_llm) -> str:
    """
    Generate a summary of the given text using the LLM.
    
    Args:
        text: The text to summarize
        multimodal_llm: MultimodalLLM instance for generating summaries
    
    Returns:
        Generated summary as a string
    """
    prompt = f"""Summarize in exactly one sentence without any preamble or additional text: {text}"""
    
    try:
        summary = multimodal_llm.generate_text(prompt)
        return summary.strip()
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return ""

def generate_metadata(markdown_file_path: str, multimodal_llm=None) -> str:
    """
    Generate metadata JSON from markdown file and optionally generate image descriptions and summaries using LLM.
    
    Args:
        markdown_file_path: Path to the markdown file
        multimodal_llm: Optional MultimodalLLM instance for generating descriptions and summaries
    
    Returns:
        Path to the generated metadata JSON file
    """
    # Read the markdown file
    with open(markdown_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract slide data
    slides = extract_slide_content(content)
    
    # Create metadata structure
    metadata = {
        "source_file": os.path.basename(markdown_file_path),
        "parsed_at": datetime.now().isoformat(),
        "slide_count": len(slides),
        "slides": slides
    }
    
    # Write to JSON file
    output_path = os.path.join(
        os.path.dirname(markdown_file_path),
        os.path.splitext(os.path.basename(markdown_file_path))[0] + '_metadata.json'
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # If LLM is provided, generate descriptions for all images and summaries for all slides
    if multimodal_llm:
        # First, generate summaries for all slides
        for slide in slides:
            if slide["description"].strip():  # Only generate summary if there's content
                slide["desc_summary"] = generate_summary(slide["description"], multimodal_llm)
        
        # Then, generate descriptions for all images
        image_paths = []
        for slide in slides:
            for img in slide["images"]:
                full_path = os.path.join(os.path.dirname(markdown_file_path), img["path"])
                image_paths.append(full_path)
        
        if image_paths:
            descriptions = multimodal_llm.batch_describe_images(image_paths)
            
            # Update metadata with descriptions
            for slide in slides:
                for img in slide["images"]:
                    full_path = os.path.join(os.path.dirname(markdown_file_path), img["path"])
                    if full_path in descriptions:
                        img["description"] = descriptions[full_path]
        
        # Write updated metadata with both summaries and image descriptions
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return output_path

# if __name__ == "__main__":
#     # Example usage
#     markdown_file = "output/Storage Nepal/Storage Nepal.md"
#     output_file = generate_metadata(markdown_file)
#     print(f"Metadata generated and saved to: {output_file}") 