from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
import random
import asyncio
from typing import List, Dict, Optional
import logging
import os
import json
from nextcloud_client import NextcloudClient
from dotenv import load_dotenv
import traceback
from status_page import generate_status_page
from image_utils import process_image
from slideshow_page import generate_slideshow_page

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        password=NEXTCLOUD_PASSWORD,
        directories=NEXTCLOUD_DIRS
    )
else:
    logger.error("Nextcloud integration disabled - missing credentials")
    raise RuntimeError("Nextcloud credentials are required")

# Global state for /next endpoint
_current_index = 0
_all_images = []

# Get image processing settings from environment
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", "1920"))
JPG_QUALITY = int(os.getenv("JPG_QUALITY", "85"))
CONVERT_TO_JPG = os.getenv("CONVERT_TO_JPG", "true").lower() == "true"

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
    """Serve the status page."""
    try:
        images = nextcloud_client.list_pictures()
        return HTMLResponse(generate_status_page(
            images=images,
            nextcloud_url=NEXTCLOUD_URL,
            nextcloud_username=NEXTCLOUD_USERNAME,
            nextcloud_dirs=NEXTCLOUD_DIRS,
            max_image_size=MAX_IMAGE_SIZE,
            jpg_quality=JPG_QUALITY,
            convert_to_jpg=CONVERT_TO_JPG
        ))
    except Exception as e:
        logger.error(f"Error generating status page: {e}")
        raise HTTPException(status_code=500, detail="Error generating status page")

@app.get("/random")
async def get_random_image():
    """Get a random image from Nextcloud."""
    try:
        images = nextcloud_client.list_pictures()
        if not images:
            raise HTTPException(status_code=404, detail="No images found")

        selected_image = random.choice(images)
        logger.info(f"Selected random image: {selected_image['name']}")

        # Fetch image data
        image_data = nextcloud_client.get_image(selected_image["path"])

        # Process image
        processed_data = process_image(
            image_data=image_data,
            max_size=MAX_IMAGE_SIZE,
            quality=JPG_QUALITY,
            convert_to_jpg=CONVERT_TO_JPG
        )

        return Response(
            content=processed_data,
            media_type="image/jpeg" if CONVERT_TO_JPG else "image/png"
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error fetching random image: {e}")
        raise HTTPException(status_code=500, detail="Error fetching image")

@app.get("/next")
async def get_next_image():
    """Get the next image in sequence."""
    try:
        images = nextcloud_client.list_pictures()
        if not images:
            raise HTTPException(status_code=404, detail="No images found")

        # Get the next image (implementation depends on your sequence logic)
        selected_image = images[0]  # For now, just get the first image
        logger.info(f"Selected next image: {selected_image['name']}")

        # Fetch image data
        image_data = nextcloud_client.get_image(selected_image["path"])

        # Process image
        processed_data = process_image(
            image_data=image_data,
            max_size=MAX_IMAGE_SIZE,
            quality=JPG_QUALITY,
            convert_to_jpg=CONVERT_TO_JPG
        )

        return Response(
            content=processed_data,
            media_type="image/jpeg" if CONVERT_TO_JPG else "image/png"
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error fetching next image: {e}")
        raise HTTPException(status_code=500, detail="Error fetching image")

@app.get("/slideshow", response_class=HTMLResponse)
async def slideshow():
    """Serve the slideshow page."""
    return generate_slideshow_page()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    logger.info("Starting server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8181)