from webdav3.client import Client
import logging
from typing import List, Dict, Optional, Tuple
import os
import tempfile
from io import BytesIO

logger = logging.getLogger(__name__)

class NextcloudClient:
    def __init__(self, url: str, username: str, password: str):
        """Initialize Nextcloud client with credentials."""
        self.url = url.rstrip('/')
        self.username = username
        self.password = password
        options = dict(
            hostname=self.url,
            login=self.username,
            password=self.password,
            protocol='https',
            webdav_root=f'/remote.php/dav/files/{self.username}/',
            verbose=True  # Enable WebDAV client debug logging
        )
        self.client = Client(options)
        self._cached_images = {}

    def list_pictures(self, folder: str = "Pictures") -> List[Dict]:
        """List all pictures in the specified folder."""
        if folder in self._cached_images:
            logger.info(f"Using cached Nextcloud images for folder: {folder}")
            return self._cached_images[folder]

        try:
            # List all files in the folder
            logger.info(f"Listing files in folder: {folder}")
            files = self.client.list(folder)
            logger.info(f"Found {len(files)} files in folder {folder}")

            # Filter for image files
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
            pictures = []

            for file in files:
                full_path = '/'.join([folder, file])
                if os.path.splitext(file)[1].lower() in image_extensions:
                    pictures.append({
                        "name": os.path.basename(file),
                        "path": full_path,
                        "url": f"{self.url}/remote.php/dav/files/{self.username}/{full_path}"
                    })

            self._cached_images[folder] = pictures
            return pictures
        except Exception as e:
            logger.error(f"Error listing pictures from Nextcloud folder {folder}: {str(e)}")
            self._cached_images[folder] = []
            return []

    def get_direct_download_url(self, file_path: str) -> Optional[str]:
        """Get a direct download URL for a file."""
        try:
            return f"{self.url}/remote.php/dav/files/{self.username}/{file_path}"
        except Exception as e:
            logger.error(f"Error getting direct download URL: {str(e)}")
            return None

    def fetch_file_content(self, url: str) -> Tuple[Optional[bytes], Optional[str]]:
        """Fetch file content from Nextcloud URL."""
        try:
            # Extract the path from the URL
            path = url.split(f"{self.url}/remote.php/dav/files/{self.username}/")[1]
            logger.info(f"Fetching file content for path: {path}")
            # Get file content using BytesIO buffer
            buffer = BytesIO()
            self.client.resource(path).write_to(buffer)
            return buffer.getvalue(), "image/jpeg"  # You might want to detect the actual content type
        except Exception as e:
            logger.error(f"Error fetching Nextcloud file: {str(e)}")
            return None, None