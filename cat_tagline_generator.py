#!/usr/bin/env python3
"""
Cat Tagline Generator

This script demonstrates a complete AI pipeline that:
1. Fetches random cat images from the Cat As A Service API
2. Uses OpenAI's GPT-4 Vision to analyze and describe the images
3. Generates funny, meme-worthy taglines based on the descriptions

This is a great example of:
- API integration (REST API calls)
- AI/ML workflows (Vision AI + Text Generation)
- Error handling and user feedback
- Object-oriented programming in Python
"""

# ============================================================================
# IMPORTS SECTION
# ============================================================================
# Standard library imports - these come with Python
import os          # For environment variables and file operations
import base64      # For encoding images to base64 (required by OpenAI Vision)
import io          # For handling byte streams (image data)
from typing import Optional, Dict, Any  # Type hints for better code documentation

# Third-party imports - these need to be installed via pip
import requests           # For making HTTP requests to the cat API
from dotenv import load_dotenv  # For loading environment variables from .env file
from openai import OpenAI       # Official OpenAI Python client
from PIL import Image           # Python Imaging Library for image processing

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================
# Load environment variables from .env file
# This allows us to keep sensitive information (like API keys) out of our code
load_dotenv()

# ============================================================================
# MAIN CLASS DEFINITION
# ============================================================================
class CatTaglineGenerator:
    """
    A class that orchestrates the entire cat tagline generation pipeline.

    This class encapsulates all the functionality needed to:
    - Fetch random cat images from an API
    - Analyze images using AI
    - Generate funny taglines
    - Handle errors gracefully

    Using a class allows us to maintain state (like API clients) and
    organize related functionality together.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Cat Tagline Generator with required API clients and configuration.

        This constructor:
        1. Retrieves the OpenAI API key from parameter or environment variables
        2. Sets up the OpenAI client for making API calls
        3. Configures the Cat API endpoint

        Args:
            api_key: Optional OpenAI API key. If not provided, will try to load from environment variables.

        Raises:
            ValueError: If OPENAI_API_KEY is not found in environment variables or provided as parameter
        """
        # Get API key from parameter or environment variables
        if api_key:
            # Use provided API key
            self.api_key = api_key
        else:
            # Try to get from environment variables (for local development)
            self.api_key = os.getenv('OPENAI_API_KEY')

        # Fail fast if API key is missing - better to crash early than later
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required. Provide it as a parameter or set the environment variable.")

        # Initialize OpenAI client - this handles authentication and API communication
        self.client = OpenAI(api_key=self.api_key)

        # Store the base URL for the Cat As A Service API
        # This API provides free random cat images - no authentication required!
        self.cataas_base_url = "https://cataas.com"

    def fetch_random_cat_image(self) -> Optional[bytes]:
        """
        Fetch a random cat image from the Cat As A Service API.

        This method demonstrates:
        - Making HTTP GET requests
        - Error handling with try/except
        - Timeout configuration for network requests
        - Returning raw image data as bytes

        Returns:
            bytes: The raw image data if successful, None if failed

        Technical Notes:
        - We use a 10-second timeout to prevent hanging
        - response.raise_for_status() raises an exception for HTTP error codes
        - We return the raw bytes so we can both save and process the image
        """
        try:
            # Make HTTP GET request to fetch a random cat image
            # The /cat endpoint returns a random cat image each time
            response = requests.get(f"{self.cataas_base_url}/cat", timeout=10)

            # Raise an exception if the HTTP request failed (4xx or 5xx status codes)
            response.raise_for_status()

            # Provide user feedback with file size info
            print(f"✅ Successfully fetched cat image ({len(response.content)} bytes)")

            # Return the raw image data as bytes
            return response.content

        except requests.RequestException as e:
            # Catch all requests-related exceptions (network errors, timeouts, etc.)
            print(f"❌ Error fetching cat image: {e}")
            return None  # Return None to indicate failure

    def save_image_locally(self, image_data: bytes, filename: str = "current_cat.jpg") -> str:
        """
        Save the fetched image data to a local file.

        This method demonstrates:
        - Working with binary data (image bytes)
        - Using Pillow (PIL) for image validation and saving
        - Default parameter values
        - Error handling with re-raising exceptions

        Args:
            image_data: Raw image bytes from the API
            filename: Name for the saved file (defaults to "current_cat.jpg")

        Returns:
            str: The filepath where the image was saved

        Raises:
            Exception: Re-raises any exception that occurs during image processing

        Technical Notes:
        - io.BytesIO() creates a file-like object from bytes
        - PIL.Image.open() validates that the data is actually a valid image
        - We re-raise exceptions so calling code can handle them appropriately
        """
        try:
            # Create a file-like object from the raw bytes
            # This allows Pillow to read the image data as if it were a file
            image_buffer = io.BytesIO(image_data)

            # Open and validate the image using Pillow
            # This will raise an exception if the data isn't a valid image
            image = Image.open(image_buffer)

            # Save the image to disk
            # Pillow automatically determines the format from the filename extension
            image.save(filename)

            # Provide user feedback
            print(f"💾 Saved image as {filename}")

            return filename

        except Exception as e:
            # Log the error for debugging
            print(f"❌ Error saving image: {e}")
            # Re-raise the exception so the calling code knows something went wrong
            raise

    def describe_image(self, image_data: bytes) -> Optional[str]:
        """
        Use OpenAI's GPT-4 Vision model to analyze and describe the cat image.

        This method demonstrates:
        - Working with OpenAI's Vision API
        - Base64 encoding (required for sending images to the API)
        - Structured API requests with multiple content types
        - Prompt engineering for better results

        Args:
            image_data: Raw image bytes to analyze

        Returns:
            str: AI-generated description of the image, or None if failed

        Technical Notes:
        - Images must be base64-encoded to send to OpenAI's API
        - We use the "gpt-4o-mini" model for cost-effectiveness
        - The prompt is carefully crafted to get useful descriptions
        - We limit response to 300 tokens to control costs
        """
        try:
            # Convert image bytes to base64 string
            # This is required by OpenAI's API for image uploads
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Make API call to OpenAI's Vision model
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective vision model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                # Text part of the message - our instructions to the AI
                                "type": "text",
                                "text": "Please describe this cat image in detail. Focus on the cat's appearance, pose, expression, surroundings, and any notable or amusing features. Be descriptive but concise."
                            },
                            {
                                # Image part of the message - the actual cat photo
                                "type": "image_url",
                                "image_url": {
                                    # Data URL format: data:image/jpeg;base64,<base64_data>
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300  # Limit response length to control costs
            )

            # Extract the description from the API response
            description = response.choices[0].message.content

            # Provide user feedback
            print(f"🔍 Image description: {description}")

            return description

        except Exception as e:
            # Handle any API errors (authentication, rate limits, etc.)
            print(f"❌ Error describing image: {e}")
            return None

    def generate_funny_tagline(self, image_description: str) -> Optional[str]:
        """
        Generate a funny, meme-worthy tagline based on the image description.

        This method demonstrates:
        - Using OpenAI's text generation capabilities
        - System/user message structure for better prompt engineering
        - Temperature parameter for controlling creativity
        - Different model usage patterns

        Args:
            image_description: AI-generated description of the cat image

        Returns:
            str: Funny tagline, or None if generation failed

        Technical Notes:
        - We use "system" message to set the AI's role and style
        - Higher temperature (0.9) increases creativity and randomness
        - We limit tokens to 100 since taglines should be short
        - The prompt is designed to encourage puns and internet humor
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Same model for consistency
                messages=[
                    {
                        # System message defines the AI's role and behavior
                        "role": "system",
                        "content": "You are a witty copywriter who creates hilarious, clever taglines for cat photos. Your taglines should be punny, relatable, and capture the essence of internet cat humor. Keep them under 20 words and make them memorable."
                    },
                    {
                        # User message provides the specific task and context
                        "role": "user",
                        "content": f"Based on this cat image description, create a funny tagline:\n\n{image_description}\n\nMake it punny and internet-cat-meme worthy!"
                    }
                ],
                max_tokens=100,      # Taglines should be short
                temperature=0.9      # Higher creativity for humor
            )

            # Extract and clean the tagline
            tagline = response.choices[0].message.content.strip()

            # Provide user feedback
            print(f"😸 Generated tagline: {tagline}")

            return tagline

        except Exception as e:
            # Handle API errors
            print(f"❌ Error generating tagline: {e}")
            return None

    def run_full_pipeline(self) -> Dict[str, Any]:
        """
        Execute the complete cat tagline generation pipeline.

        This method orchestrates all the individual steps:
        1. Fetch a random cat image
        2. Save it locally
        3. Analyze image with AI
        4. Generate a funny tagline

        This demonstrates:
        - Pipeline/workflow design patterns
        - Error handling at each step
        - Returning structured results
        - Fail-fast error handling

        Returns:
            dict: Results containing:
                - image_path: Where the image was saved
                - description: AI description of the image
                - tagline: Generated funny tagline
                - success: Boolean indicating if pipeline completed
                - error: Error message if something failed

        Design Notes:
        - Each step can fail independently
        - We stop the pipeline at the first failure
        - Results are returned in a consistent format
        - This makes it easy to use from other code (like the web interface)
        """
        print("🐱 Starting Cat Tagline Generator...")

        # Step 1: Fetch cat image from API
        # This can fail due to network issues or API problems
        image_data = self.fetch_random_cat_image()
        if not image_data:
            return {"error": "Failed to fetch cat image"}

        # Step 2: Save image locally
        # This can fail due to file system issues or invalid image data
        try:
            image_path = self.save_image_locally(image_data)
        except Exception:
            # We already logged the specific error in save_image_locally()
            return {"error": "Failed to save cat image"}

        # Step 3: Analyze image with AI
        # This can fail due to API issues or invalid image format
        description = self.describe_image(image_data)
        if not description:
            return {"error": "Failed to describe cat image"}

        # Step 4: Generate funny tagline
        # This can fail due to API issues or prompt problems
        tagline = self.generate_funny_tagline(description)
        if not tagline:
            return {"error": "Failed to generate tagline"}

        # Success! Return all results
        return {
            "image_path": image_path,
            "description": description,
            "tagline": tagline,
            "success": True
        }

# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================
def main():
    """
    Main function to run the cat tagline generator from command line.

    This function demonstrates:
    - Command-line application structure
    - Different types of error handling
    - User-friendly output formatting
    - Separation of library code from CLI code

    Error Handling Strategy:
    - ValueError: Configuration issues (missing API key)
    - General Exception: Unexpected errors
    - Pipeline errors: Handled by run_full_pipeline()
    """
    try:
        # Create an instance of our generator class
        generator = CatTaglineGenerator()

        # Run the complete pipeline
        result = generator.run_full_pipeline()

        # Check if the pipeline succeeded
        if result.get("success"):
            # Format and display successful results
            print("\n" + "="*50)
            print("🎉 SUCCESS! Here's your cat content:")
            print("="*50)
            print(f"📸 Image saved as: {result['image_path']}")
            print(f"📝 Description: {result['description']}")
            print(f"🎯 Tagline: {result['tagline']}")
            print("="*50)
        else:
            # Display pipeline error
            print(f"\n❌ Pipeline failed: {result.get('error', 'Unknown error')}")

    except ValueError as e:
        # Handle configuration errors (missing API key)
        print(f"❌ Configuration error: {e}")
        print("💡 Make sure to set your OPENAI_API_KEY in a .env file")

    except Exception as e:
        # Handle any unexpected errors
        print(f"❌ Unexpected error: {e}")

# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================
# This is a Python idiom that allows the script to be:
# 1. Run directly: python cat_tagline_generator.py
# 2. Imported as a module: from cat_tagline_generator import CatTaglineGenerator
if __name__ == "__main__":
    main()