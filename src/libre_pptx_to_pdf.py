from pathlib import Path
import os
import subprocess

def convert_pptx_to_pdf(input_path, output_path=None):
    """
    Convert a PowerPoint file to PDF using LibreOffice.
    
    Args:
        input_path (str): Path to the input PowerPoint file
        output_path (str, optional): Path to save the output PDF file. 
                                   If not provided, will use the same name as input with .pdf extension
    
    Returns:
        str: Path to the generated PDF file
    """
    try:
        # If output path is not specified, create one with the same name but .pdf extension
        if output_path is None:
            output_path = str(Path(input_path).with_suffix('.pdf'))
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert using LibreOffice
        cmd = [
            'libreoffice', '--headless', '--convert-to', 'pdf',
            '--outdir', os.path.dirname(output_path),
            input_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"LibreOffice conversion failed: {result.stderr}")
        
        # Get the actual output path (LibreOffice might modify the filename)
        actual_output = str(Path(os.path.dirname(output_path)) / f"{Path(input_path).stem}.pdf")
        
        return actual_output
        
    except Exception as e:
        raise
    
    
