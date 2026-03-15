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
from urllib.parse import urlparse

API_KEY = os.environ.get("IMAGE_GEN_GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("IMAGE_GEN_API_KEY", "")
BASE_URL = os.environ.get("IMAGE_GEN_GEMINI_BASE_URL") or os.environ.get("GEMINI_BASE_URL") or os.environ.get("IMAGE_GEN_BASE_URL", "https://api.xheai.cc/v1beta")
DEFAULT_MODEL = os.environ.get("IMAGE_GEN_GEMINI_IMAGE_MODEL") or os.environ.get("IMAGE_GEN_GEMINI_MODEL") or os.environ.get("GEMINI_IMAGE_MODEL") or os.environ.get("GEMINI_MODEL") or "nano-banana-2"

def _guess_extension_from_url(url: str) -> str:
    path = urlparse(url).path
    suffix = Path(path).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        return suffix.lstrip(".")
    return "png"


def _resolve_output_path(output_path: str | None, ext: str) -> Path:
    if output_path:
        out_file = Path(output_path)
        if not out_file.suffix:
            out_file = out_file.with_suffix(f".{ext}")
        return out_file
    return Path.cwd() / f"generated_image.{ext}"


def generate_image(prompt: str, model: str = DEFAULT_MODEL, output_path: str = None) -> str:
    """Generate image from text prompt"""

    if not API_KEY:
        print("ERROR: IMAGE_GEN_GEMINI_API_KEY not set", file=sys.stderr)
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
        with httpx.Client(timeout=120.0, follow_redirects=True) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Format 1: Gemini native response with inlineData
            parts = result.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            image_data = None
            text_response = ""

            for part in parts:
                if "inlineData" in part:
                    image_data = part["inlineData"]
                elif "text" in part:
                    text_response = part["text"]

            if image_data:
                img_bytes = base64.b64decode(image_data["data"])
                mime_type = image_data.get("mimeType", "image/png")
                ext = mime_type.split("/")[-1] if "/" in mime_type else "png"
                out_file = _resolve_output_path(output_path, ext)
                out_file.write_bytes(img_bytes)
                print(f"Image saved to: {out_file}", file=sys.stderr)
                print(str(out_file))
                return str(out_file)

            # Format 2: proxy response with image URL in data[0].url
            data = result.get("data") or []
            image_url = None
            if data and isinstance(data[0], dict):
                image_url = data[0].get("url") or data[0].get("b64_json")

            if image_url:
                if image_url.startswith("http://") or image_url.startswith("https://"):
                    img_resp = client.get(image_url)
                    img_resp.raise_for_status()
                    img_bytes = img_resp.content
                    ext = _guess_extension_from_url(image_url)
                    out_file = _resolve_output_path(output_path, ext)
                    out_file.write_bytes(img_bytes)
                    print(f"Image downloaded from URL and saved to: {out_file}", file=sys.stderr)
                    print(str(out_file))
                    return str(out_file)

                # Some proxies may return base64 in b64_json
                try:
                    img_bytes = base64.b64decode(image_url)
                    out_file = _resolve_output_path(output_path, "png")
                    out_file.write_bytes(img_bytes)
                    print(f"Image decoded from base64 and saved to: {out_file}", file=sys.stderr)
                    print(str(out_file))
                    return str(out_file)
                except Exception:
                    pass

    except Exception as e:
        print(f"ERROR: API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"No image in response. Raw response: {json.dumps(result, ensure_ascii=False)[:1000]}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate image with Gemini Flash Image")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help="Model to use")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()
    
    generate_image(args.prompt, args.model, args.output)
