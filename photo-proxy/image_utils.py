from io import BytesIO
from PIL import Image
import piexif
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def process_image(
    image_data: bytes,
    max_size: Optional[int] = None,
    quality: int = 85,
    convert_to_jpg: bool = True,
    crop_portrait_to_square: bool = False
) -> bytes:
    """
    Process an image by scaling, rotating based on EXIF, and optionally converting to JPG.

    Args:
        image_data: Raw image data in bytes
        max_size: Maximum width/height for scaling (None for no scaling)
        quality: JPEG quality (1-100)
        convert_to_jpg: Whether to convert the image to JPG format
        crop_portrait_to_square: Whether to crop portrait images to a square aspect ratio

    Returns:
        Processed image data in bytes
    """
    try:
        # Open image from bytes
        image = Image.open(BytesIO(image_data))

        # Get original format
        original_format = image.format.lower()

        # Handle EXIF rotation
        try:
            # Extract EXIF data
            exif_dict = piexif.load(image.info.get("exif", b""))
            if exif_dict and "0th" in exif_dict:
                orientation = exif_dict["0th"].get(piexif.ImageIFD.Orientation)
                if orientation:
                    # Rotate image based on EXIF orientation
                    rotation_angles = {
                        3: 180,
                        6: 270,
                        8: 90
                    }
                    if orientation in rotation_angles:
                        image = image.rotate(rotation_angles[orientation], expand=True)
                        logger.debug(f"Rotated image by {rotation_angles[orientation]} degrees based on EXIF data")
        except Exception as e:
            logger.warning(f"Failed to process EXIF data: {e}")

        # Scale image if max_size is specified
        if max_size:
            image = scale_image(image, max_size)

        # Crop portrait images to square if requested
        if crop_portrait_to_square:
            width, height = image.size
            if height > width:  # Portrait orientation
                # Calculate crop box (center crop)
                left = 0
                top = (height - width) // 2
                right = width
                bottom = top + width
                image = image.crop((left, top, right, bottom))
                logger.debug(f"Cropped portrait image to square {width}x{width}")

        # Convert to RGB if needed (for JPG conversion)
        if convert_to_jpg and image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGB')

        # Prepare output
        output = BytesIO()

        if convert_to_jpg:
            # Save as JPG
            image.save(output, format='JPEG', quality=quality, optimize=True)
            logger.debug(f"Converted image to JPG with quality {quality}")
        else:
            # Save in original format
            image.save(output, format=original_format)

        return output.getvalue()

    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise

def scale_image(image: Image.Image, max_size: int) -> Image.Image:
    """
    Scale an image to fit within max_size while maintaining aspect ratio.

    Args:
        image: PIL Image object
        max_size: Maximum width/height

    Returns:
        Scaled PIL Image object
    """
    # Get current dimensions
    width, height = image.size

    # Calculate scaling factor
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))

    # Scale image
    scaled_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    logger.debug(f"Scaled image from {width}x{height} to {new_width}x{new_height}")

    return scaled_image

def get_image_dimensions(image_data: bytes) -> Tuple[int, int]:
    """
    Get the dimensions of an image from its data.

    Args:
        image_data: Raw image data in bytes

    Returns:
        Tuple of (width, height)
    """
    with Image.open(BytesIO(image_data)) as img:
        return img.size