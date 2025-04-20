import base64
import json
from pathlib import Path
from typing import Dict, List, Optional
import requests
import os
import ollama

class MultimodalLLM:
    def __init__(self, model_name: str = "gemma3:4b", base_url: str = "http://localhost:11434"):
        """
        Initialize the MultimodalLLM with Ollama configuration.
        
        Args:
            model_name: Name of the model to use (default: "gemma3:4b")
            base_url: Base URL for Ollama API (default: "http://localhost:11434")
        """
        self.model_name = model_name
        self.base_url = base_url
        self.client = ollama.Client()
        
    def _encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 string.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded string of the image
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    def describe_image(self, image_path: str, prompt: str = None) -> Optional[str]:
        """
        Send image to Ollama and get description.
        
        Args:
            image_path: Path to the image file
            prompt: Custom prompt to use (optional)
            
        Returns:
            Generated description or None if failed
        """
        if not Path(image_path).exists():
            print(f"Image not found: {image_path}")
            return None
            
        try:
            image_base64 = self._encode_image(image_path)
            
            # Default prompt if none provided
            if prompt is None:
                prompt = "Describe this image in one clear sentence."
            
            # Create message with image in the correct format
            message = {
                "role": "user",
                "content": prompt,
                "images": [image_base64]
            }
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [message],
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract content from response
            return result.get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"Error describing image {image_path}: {str(e)}")
            return None
        
    def batch_describe_images(self, image_paths: List[str]) -> Dict[str, str]:
        """
        Generate descriptions for multiple images in a batch.
        
        Args:
            image_paths: List of paths to images
            
        Returns:
            Dictionary mapping image paths to their descriptions
        """
        descriptions = {}
        for image_path in image_paths:
            if not os.path.exists(image_path):
                print(f"Image not found: {image_path}")
                continue
                
            try:
                response = self.client.generate(
                    model=self.model_name,
                    prompt="Describe this image exactly in one sentence without any preamble or additional text",
                    images=[image_path]
                )
                descriptions[image_path] = response['response'].strip()
            except Exception as e:
                print(f"Error describing image {image_path}: {str(e)}")
                descriptions[image_path] = ""
                
        return descriptions

    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate text based on the given prompt.
        
        Args:
            prompt: The text prompt to generate a response for
            max_tokens: Maximum number of tokens to generate (default: 500)
            
        Returns:
            Generated text response
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            return result['message']['content'].strip()
        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return ""

    def test_connection(self) -> bool:
        """Test basic connection to Ollama"""
        try:
            # Simple test request
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": "Hello!"}],
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            print("Successfully connected to Ollama")
            print("Test response:", result.get("message", {}).get("content", "")[:50] + "...")
            return True
        except Exception as e:
            print(f"Error connecting to Ollama: {str(e)}")
            return False