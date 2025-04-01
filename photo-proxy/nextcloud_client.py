from webdav4.client import Client
import logging
from typing import List, Dict, Optional
import os
import traceback
from urllib.parse import quote, unquote
logger = logging.getLogger(__name__)

class NextcloudClient:
    def __init__(self, url: str, username: str, password: str, directories: List[str] = None):
        """
        Initialize the Nextcloud client.

        Args:
            url: Nextcloud server URL
            username: Nextcloud username
            password: Nextcloud password
            directories: List of directories to scan for images
        """
        self.url = url.rstrip('/')
        self.username = username
        self.password = password
        self.directories = directories or ["Pictures"]
        self.client = Client(
            base_url=self.url,
            auth=(self.username, self.password)
        )
        self._cached_images = {}

    def list_pictures(self, folder: str = None) -> List[Dict]:
        """
        List all pictures in the specified folder.

        Args:
            folder: Specific folder to list (if None, lists all configured folders)

        Returns:
            List of dictionaries containing image information
        """
        try:
            # If a specific folder is requested, check cache first
            if folder and folder in self._cached_images:
                logger.debug(f"Using cached images for folder: {folder}")
                return self._cached_images[folder]

            # Determine which folders to scan
            folders_to_scan = [folder] if folder else self.directories
            all_images = []

            for current_folder in folders_to_scan:
                # Remove leading/trailing slashes and ensure proper path
                current_folder = current_folder.strip('/')
                folder_path = f"/remote.php/dav/files/{self.username}/{current_folder}"

                logger.info(f"Listing files in folder: {current_folder}")
                # Use the correct method for listing files
                files = self.client.ls(folder_path)

                # Filter for image files
                images = [
                    {
                        "name": os.path.basename(file["name"]),
                        "path": file["href"],
                        "size": file.get("content_length", 0),
                        "modified": file.get("modified", ""),
                        "content_type": file.get("content_type", "")
                    }
                    for file in files
                    if file.get("type") == "file" and file["name"].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))
                ]

                logger.info(f"Found {len(images)} images in {current_folder}")
                all_images.extend(images)

                # Cache the results for this folder
                self._cached_images[current_folder] = images

            return all_images

        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error listing pictures: {str(e)}")
            raise

    def get_image(self, path: str) -> bytes:
        """
        Get the content of an image file.

        Args:
            path: Full path to the image file

        Returns:
            Image data as bytes
        """
        try:
            logger.debug(f"Fetching image: {path}")
            # Decode the URL-encoded path
            decoded_path = unquote(path)

            # Use open() for fetching files with the decoded path
            with self.client.open(decoded_path, mode="rb") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error fetching image {path}: {str(e)}")
            raise