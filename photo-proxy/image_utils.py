from io import BytesIO
from PIL import Image
import piexif
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def handle_exif_rotation(image: Image.Image) -> Image.Image:
    """
    Handle EXIF rotation data in the image.

    Args:
        image: PIL Image object

    Returns:
        Rotated PIL Image object if EXIF data indicates rotation needed
    """
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

    return image

def crop_portrait_to_square(image: Image.Image) -> Image.Image:
    """
    Crop a portrait image to a square aspect ratio by center cropping.

    Args:
        image: PIL Image object

    Returns:
        Cropped PIL Image object if portrait orientation, otherwise original image
    """
    width, height = image.size
    if height > width:  # Portrait orientation
        # Calculate crop box (center crop)
        left = 0
        top = (height - width) // 2
        right = width
        bottom = top + width
        image = image.crop((left, top, right, bottom))
        logger.debug(f"Cropped portrait image to square {width}x{width}")
    return image

def convert_to_landscape_3_2(image: Image.Image) -> Image.Image:
    """
    Convert an image to 3:2 landscape format with black bars if needed.
    If the image is portrait, it will first be cropped to a square and then
    placed in the center of a 3:2 landscape canvas with black bars.

    Args:
        image: PIL Image object

    Returns:
        PIL Image object in 3:2 landscape format
    """
    width, height = image.size

    # If portrait, first crop to square
    if height > width:
        image = crop_portrait_to_square(image)
        width = image.size[0]  # Update width after cropping
    else:
        return image

    # Calculate target dimensions for 3:2 aspect ratio
    target_height = width  # Keep the original width
    target_width = int(target_height * 1.5)  # 3:2 aspect ratio

    # Create new black image with 3:2 aspect ratio
    new_image = Image.new('RGB', (target_width, target_height), (0, 0, 0))

    # Calculate position to paste the original image (center)
    paste_x = (target_width - width) // 2
    paste_y = 0

    # Paste the original image onto the black background
    new_image.paste(image, (paste_x, paste_y))
    logger.debug(f"Converted image to 3:2 landscape format {target_width}x{target_height}")

    return new_image

def convert_to_jpeg(image: Image.Image, quality: int = 85) -> Image.Image:
    """
    Convert an image to JPEG format if needed.

    Args:
        image: PIL Image object
        quality: JPEG quality (1-100)

    Returns:
        Converted PIL Image object
    """
    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGB')
    return image

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
        crop_portrait_to_square: Whether to crop portrait images to 3:2 landscape format

    Returns:
        Processed image data in bytes
    """
    try:
        # Open image from bytes
        image = Image.open(BytesIO(image_data))

        # Get original format
        original_format = image.format.lower()

        # Handle EXIF rotation
        image = handle_exif_rotation(image)

        # Scale image if max_size is specified
        if max_size:
            image = scale_image(image, max_size)

        # Convert portrait images to 3:2 landscape if requested
        if crop_portrait_to_square:
            image = convert_to_landscape_3_2(image)

        # Convert to JPEG if requested
        if convert_to_jpg:
            image = convert_to_jpeg(image, quality)

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