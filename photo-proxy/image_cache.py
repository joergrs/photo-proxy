from typing import Dict, Optional, Tuple
import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)

class ImageCache:
    """
    LRU cache for storing processed images.
    Uses OrderedDict to maintain access order and limit size.
    """
    def __init__(self, max_size: int = 500):
        """
        Initialize the cache with a maximum size.

        Args:
            max_size: Maximum number of images to store in the cache
        """
        self.max_size = max_size
        self.cache: OrderedDict[str, Tuple[bytes, str]] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Tuple[bytes, str]]:
        """
        Get an image from the cache.

        Args:
            key: Cache key (typically the image path)

        Returns:
            Tuple of (image_data, content_type) if found, None otherwise
        """
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def put(self, key: str, image_data: bytes, content_type: str) -> None:
        """
        Store an image in the cache.

        Args:
            key: Cache key (typically the image path)
            image_data: Processed image data
            content_type: Content type of the image
        """
        if key in self.cache:
            # Update existing entry
            self.cache.move_to_end(key)
        else:
            # Check if we need to remove oldest entry
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
                logger.debug("Removed oldest entry from image cache")

        self.cache[key] = (image_data, content_type)
        logger.debug(f"Added image to cache: {key} (Cache size: {len(self.cache)})")

    def clear(self) -> None:
        """Clear the cache."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("Cleared image cache")

    def get_size_mb(self) -> float:
        """
        Calculate the total size of the cache in megabytes.

        Returns:
            Size of the cache in MB, rounded to 2 decimal places
        """
        total_bytes = sum(len(data[0]) for data in self.cache.values())
        return round(total_bytes / (1024 * 1024), 2)

    def get_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_ratio": round(self.hits / (self.hits + self.misses) * 100, 2) if (self.hits + self.misses) > 0 else 0,
            "size_mb": self.get_size_mb()
        }