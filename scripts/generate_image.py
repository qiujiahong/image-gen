#!/usr/bin/env python3
"""
AI Image Generation Script
Uses Gemini Flash Image model via Google Generative AI protocol
"""
import os
import sys
import json
import base64
import httpx
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("IMAGE_GEN_API_KEY", "")
BASE_URL = os.environ.get("GEMINI_BASE_URL") or os.environ.get("IMAGE_GEN_BASE_URL", "https://api.xheai.cc/v1beta")
DEFAULT_MODEL = os.environ.get("GEMINI_IMAGE_MODEL") or os.environ.get("GEMINI_MODEL") or "nano-banana-2"

def generate_image(prompt: str, model: str = DEFAULT_MODEL, output_path: str = None) -> str:
    """Generate image from text prompt"""
    
    if not API_KEY:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    url = f"{BASE_URL.rstrip('/')}/models/{model}:generateContent"
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
            "responseMimeType": "text/plain"
        }
    }
    
    print(f"Generating image with model: {model}", file=sys.stderr)
    print(f"Prompt: {prompt[:100]}...", file=sys.stderr)
    
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
    except Exception as e:
        print(f"ERROR: API call failed: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Extract image from response
    parts = result.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    
    image_data = None
    text_response = ""
    
    for part in parts:
        if "inlineData" in part:
            image_data = part["inlineData"]
        elif "text" in part:
            text_response = part["text"]
    
    if not image_data:
        print(f"No image in response. Text: {text_response}", file=sys.stderr)
        sys.exit(1)
    
    # Decode and save image
    img_bytes = base64.b64decode(image_data["data"])
    mime_type = image_data.get("mimeType", "image/png")
    ext = mime_type.split("/")[-1] if "/" in mime_type else "png"
    
    if output_path:
        out_file = Path(output_path)
    else:
        out_file = Path.cwd() / f"generated_image.{ext}"
    
    out_file.write_bytes(img_bytes)
    print(f"Image saved to: {out_file}", file=sys.stderr)
    
    # Return path for consumption
    print(str(out_file))
    return str(out_file)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate image with Gemini Flash Image")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help="Model to use")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()
    
    generate_image(args.prompt, args.model, args.output)
