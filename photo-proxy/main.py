from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
import aiohttp
import random
import asyncio
from typing import List, Dict
import logging
import os
import json
from nextcloud_client import NextcloudClient
from dotenv import load_dotenv
import traceback
from status_page import generate_status_page

# Configure logging with timestamp
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Starting Photo Proxy application...")

# Load configuration
logger.info("Loading configuration...")
config_file = "/data/options.json"
if os.path.exists(config_file):
    with open(config_file) as f:
        config = json.load(f)
    logger.info("Loaded configuration from options.json")
else:
    # Fallback to environment variables for development
    load_dotenv()
    config = {
        "nextcloud_url": os.getenv("NEXTCLOUD_URL", ""),
        "nextcloud_username": os.getenv("NEXTCLOUD_USERNAME", ""),
        "nextcloud_password": os.getenv("NEXTCLOUD_PASSWORD", ""),
        "nextcloud_dirs": os.getenv("NEXTCLOUD_DIRS", "Pictures")
    }
    logger.info("Loaded configuration from environment variables")

app = FastAPI(title="Photo Proxy")

# Nextcloud configuration
NEXTCLOUD_URL = config.get("nextcloud_url")
NEXTCLOUD_USERNAME = config.get("nextcloud_username")
NEXTCLOUD_PASSWORD = config.get("nextcloud_password")
NEXTCLOUD_DIRS = config.get("nextcloud_dirs", "Pictures").split(",")

# Initialize Nextcloud client only if URL is set
nextcloud_client = None
if NEXTCLOUD_URL and NEXTCLOUD_USERNAME and NEXTCLOUD_PASSWORD:
    logger.info("Nextcloud integration enabled")
    logger.info(f"Nextcloud directories to scan: {NEXTCLOUD_DIRS}")
    nextcloud_client = NextcloudClient(
        url=NEXTCLOUD_URL,
        username=NEXTCLOUD_USERNAME,
        password=NEXTCLOUD_PASSWORD
    )
else:
    logger.error("Nextcloud integration disabled - missing credentials")
    raise RuntimeError("Nextcloud credentials are required")

# Global state for /next endpoint
_current_index = 0
_all_images = []

async def get_nextcloud_images() -> List[Dict]:
    """Get list of images from configured Nextcloud folders."""
    if not nextcloud_client:
        logger.error("Nextcloud integration is not enabled")
        return []

    try:
        all_images = []
        for folder in NEXTCLOUD_DIRS:
            logger.info(f"Scanning Nextcloud folder: {folder}")
            images = nextcloud_client.list_pictures(folder.strip())
            logger.info(f"Found {len(images)} images in {folder}")
            all_images.extend(images)
        logger.info(f"Total Nextcloud images loaded: {len(all_images)}")
        return all_images
    except Exception as e:
        logger.error(f"Error fetching Nextcloud images: {str(e)}")
        return []

async def update_image_list():
    """Update the global list of all available images."""
    global _all_images
    _all_images = await get_nextcloud_images()
    logger.info(f"Updated total images available: {len(_all_images)}")

@app.get("/", response_class=HTMLResponse)
async def status_page():
    """Display a status page with information about the service."""
    images = await get_nextcloud_images()
    return generate_status_page(
        images=images,
        nextcloud_url=NEXTCLOUD_URL,
        nextcloud_username=NEXTCLOUD_USERNAME,
        nextcloud_dirs=NEXTCLOUD_DIRS
    )

@app.get("/random")
async def get_random_image():
    """Serve a random image from Nextcloud."""
    logger.info("Received request for random image")

    # Get all available images
    images = await get_nextcloud_images()
    logger.info(f"Total images available: {len(images)}")

    if not images:
        logger.error("No images found in Nextcloud")
        return Response(content="No images found in Nextcloud", status_code=500)

    # Randomly select an image
    image = random.choice(images)
    logger.info(f"Selected image: {image['name']}")

    # Fetch the image
    logger.debug(f"Fetching image content: {image['name']}")
    image_content, content_type = nextcloud_client.fetch_file_content(image["url"])

    if image_content is None:
        logger.error(f"Failed to fetch image: {image['name']}")
        return Response(content="Failed to fetch image", status_code=500)

    logger.info(f"Successfully fetched image: {image['name']}")
    return StreamingResponse(
        content=iter([image_content]),
        media_type=content_type
    )

@app.get("/next")
async def get_next_image():
    """Serve the next image in sequence from Nextcloud."""
    global _current_index
    logger.info("Received request for next image")

    # Update image list if needed
    if not _all_images:
        await update_image_list()

    if not _all_images:
        logger.error("No images found in Nextcloud")
        return Response(content="No images found in Nextcloud", status_code=500)

    # Get the next image in sequence
    image = _all_images[_current_index]
    logger.info(f"Selected image {_current_index + 1}/{len(_all_images)}: {image['name']}")

    # Fetch the image
    logger.debug(f"Fetching image content: {image['name']}")
    image_content, content_type = nextcloud_client.fetch_file_content(image["url"])

    if image_content is None:
        logger.error(f"Failed to fetch image: {image['name']}")
        return Response(content="Failed to fetch image", status_code=500)

    # Update the index for next time
    _current_index = (_current_index + 1) % len(_all_images)
    logger.info(f"Successfully fetched image: {image['name']}")

    return StreamingResponse(
        content=iter([image_content]),
        media_type=content_type
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    logger.info("Starting server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8181)