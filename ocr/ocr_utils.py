import os
import logging
import base64
import json
from typing import List, Dict, Any
from groq import Groq  # Using the Groq client

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def encode_image(image_path: str) -> str:
    """
    Encode the image file to base64 string
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string of the image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_receipt_with_groq(image_path: str) -> List[Dict[str, Any]]:
    """
    Process a receipt image with Groq API to extract item data including carbon footprint
    
    Args:
        image_path: Path to the receipt image file
        
    Returns:
        List of dictionaries containing item details with carbon footprint
    """
    try:
        # Check if image exists
        if not os.path.exists(image_path):
            logging.error(f"Image file not found: {image_path}")
            return []
        
        # API key - replace with environment variable in production
        api_key = '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'
        if not api_key:
            logging.error("No Groq API key available")
            return []
        
        # Encode image to base64
        base64_image = encode_image(image_path)
        
        # Initialize Groq client
        client = Groq(api_key=api_key)
        
        # Create chat completion with image
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """
                        Extract the following information from this receipt image:
                        1. Item names
                        2. Quantities
                        3. Categories (food, electronics, etc.)
                        
                        For each item, estimate a carbon footprint value (in kg CO₂e).
                        
                        Return the data in JSON format like this:
                        [
                            {
                                "item_name": "Item name",
                                "carbon_footprint": estimated_carbon_footprint_value,
                                "quantity": quantity_value,
                                "category": "Category"
                            },
                            ...
                        ]
                        """},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        
        # Extract the response content
        response_text = chat_completion.choices[0].message.content
        
        # Improved JSON extraction
        try:
            # First attempt direct JSON parsing
            receipt_data = json.loads(response_text)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from the text
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                receipt_data = json.loads(json_str)
            else:
                logging.error(f"Could not extract valid JSON from response: {response_text}")
                return []
            
        logging.info(f"Successfully extracted receipt data: {receipt_data}")
        return receipt_data
        
    except Exception as e:
        logging.error(f"Error processing receipt with Groq API: {e}")
        return []